---
layout: post
title: Reliable rendering of web pages that view concurrently modified data
title_long: true
tags: [Django, Software]
x_audience: |
    Django, Rails, and other backend web frameworks users who are thinking 
        seriously about displaying the freshest information to their 
        visitors, that are using a somewhat complex data model
x_performance: |
    TODO

style: |
    /* Override blockquote to use same font size as body text */
    blockquote { font-size: 16px !important; }
    
    .sequence-diagram-h {
        max-width: 100%;
        max-height: 250px;
    }

---

Any time a backend Django or Rails function calculates something complex from the database to send to the frontend as part of a view, there is a chance the database will be modified concurrently before the view is displayed to the visitor, causing the site visitor to see outdated information.

In many cases displaying stale information is fine. After all refreshing the page will bring the latest information to a visitor who is temporarily seeing stale information. But in other cases showing stale information can be a major problem:

* For example if the stale data is some editable text that is shared with other site visitors and the new visitor tries to edit it, they'll clobber the last set of changes made by the previous visitor! Data loss is not OK.

* Or perhaps the stale information controls whether the visitor is allowed to access a piece of content that they are actively interested in. For example a user may be requesting to join a chat room and is waiting to be let in. Presenting stale access information saying that the visitor is locked out when they really aren't will cause them to wait forever and eventually give up! Abandonment is not OK.

How can we avoid serving stale data to the frontend to avoid such problems? This article presents one technique to both avoid serving stale data from the backend in the first place and repair the stale data quickly after page load if necessary.

Although this article is written from the perspective of a Django developer, the concepts apply to any web page that is rendered dynamically based on data from a database or other data source that is subject to concurrent modification.

## The Problem

Let's start by reviewing the problem: Consider a web page that is templated by a backend server such as Django or Rails which uses information from a database. **If visitor A reads from the database while templating such a page, but visitor B then alters the part of the database that A read, A will see outdated information** when her page finishes loading:

<img alt="Diagram: Visitor A templates a page from database data, while a visitor B makes a concurrent modification to database data" src="/assets/2021/concurrent-rendering/1H-backend-interrupt.svg" class="sequence-diagram-h" />

We want to ensure that A sees the freshest data either immediately or as quickly as possible after initial page load.

<br clear="all" />

## Designing a Solution

How can visitor A detect the change made by visitor B? One idea is to **double-check the freshness of information from the database just before returning information to the frontend**:

<img alt="Diagram: Visitor A makes one extra query to the database just before returning information to the frontend" src="/assets/2021/concurrent-rendering/2H-backend-freshness-check.svg" class="sequence-diagram-h" />

Although such a strategy does narrow the time window in which a race condition could occur, it is still possible that a concurrent modification is made while the templated page is in transit to the frontend:

<img alt="Diagram: Visitor B makes a concurrent modification while data for Visitor A is in transit to the frontend" src="/assets/2021/concurrent-rendering/3H-network-interrupt.svg" class="sequence-diagram-h" />

Another idea is for the frontend to explicitly **double-check the freshness of the information it receives from the backend shortly after it initially renders**. If the frontend happens to be displaying outdated information it can repair its state immediately with the new information from the backend:

<img alt="Diagram: Visitor A's frontend does check for any concurrent modification immediately after rendering the initial information received from the backend" src="/assets/2021/concurrent-rendering/4H-frontend-freshness-check.svg" class="sequence-diagram-h" />

This strategy is almost perfect (for getting the most up-to-date state reliably to the frontend). However there's still a narrow time window in which visitor B can make a modification after visitor A's final request.

<img alt="Diagram: Visitor B makes a change slightly after visitor A's frontend makes a final freshness check" src="/assets/2021/concurrent-rendering/5H-frontend-interrupt.svg" class="sequence-diagram-h" />

What now? To detect these types of concurrent changes it is necessary for the backend to **push any new changes to the frontend in real-time (via WebSocket)** and the frontend needs to be prepared to receive these kinds of updates to its displayed state continuously:

<img alt="Diagram: Every time Visitor B makes a change, an update is pushed to Visitor A in real-time, quickly bringing Visitor A's frontend up to date." src="/assets/2021/concurrent-rendering/6H-push-fresh-data-live.svg" class="sequence-diagram-h" />

> **Note:** My last article explains in depth [how to setup such real-time updates over WebSocket in Django using Channels]. In Rails you'd use ActionCable.

[how to setup such real-time updates over WebSocket in Django using Channels]: /articles/2021/03/02/real-time-updates-in-django-with-websockets-channels-and-pub-sub/

Additionally the backend must be prepared to **push even those changes that occur between when the backend templates a view and before the frontend has connected a WebSocket**:

<img alt="Diagram: Changes made by Visitor B are buffered so that when Visitor A's socket connects later the change is still pushed to Visitor A." src="/assets/2021/concurrent-rendering/7H-push-fresh-data-buffered.svg" class="sequence-diagram-h" />

> **Note:** Neither Django's Channels nor Rails' ActionCable provide out-of-the box support for observing events that occur during this critical time period. In the [Implementation](#implementation) section below I outline a technique of tracking the "timepoint" an event was generated at so that it can be buffered and delivered later reliably.

Great! We've got a bulletproof design to quickly observe an accurate up-to-date state on the frontend. But it does seem to be rather complex...

## Alternative Design: No backend templating

It is *possible* to remove the initial logic that templates information initially on the backend and **rely entirely on the WebSocket established after frontend page load to receive both the initial page state and any updates to that state in real-time**. Indeed this is the approach taken by many Single Page Applications (SPAs):

<img alt="Diagram: Backend does not preload any data. Frontend pulls data and changes from backend." src="/assets/2021/concurrent-rendering/8H-push-only.svg" class="sequence-diagram-h" />

However removing backend templating entirely will cause the initial page load to contain no content (beyond an annoying spinner) and raise your time-to-first-render. Content won't be delivered until after JavaScript is loaded - which can take a while on mobile devices - *and* after a socket connection is established, disproportionately slowing the browsing experience of any site visitor who isn't on a high-end device with a fast low-latency internet connection.

I'd like to reach users who are on mobile devices, in rural areas, and from faraway countries where minimizing latency and bandwidth is important to avoid an unacceptable user experience. So we're back to the more complex design with both backend templating and real-time updates...

<a name="implementation"></a>
## Implementation <small>(using Django)</small>

Let's actually sketch our design for reliable rendering in code!

I'll use the [example of a User Home Page that lists a set of associated Chat Rooms] from my last article.

[example of a User Home Page that lists a set of associated Chat Rooms]: /articles/2021/03/02/real-time-updates-in-django-with-websockets-channels-and-pub-sub/#private-chat-rooms

Please review the [User, ChatRoom, and ChatRoomJoinRequest models].

[User, ChatRoom, and ChatRoomJoinRequest models]: /articles/2021/03/02/real-time-updates-in-django-with-websockets-channels-and-pub-sub/#models-consumers-and-routes

Let's define a **cacheable calculation** for the set of available rooms given a particular user:

```
from typing import TypedDict

IntStr = str  # parseable as an int

class RoomInfo(TypedDict):
    id: IntStr
    title: str
    pending: bool

def calculate_chat_room_list(user: User) -> List[RoomInfo]:
    joined_rooms = [
        dict(
            id=str(room.id),
            title=room.title,
            pending=False,
        )
        for room in user.joined_room_set.all()
    ]
    pending_rooms = [
        dict(
            id=str(join_request.room.id),
            title=join_request.room.title,
            pending=True,
        )
        for join_request in ChatRoomJoinRequest.filter(user=user, status='pending')
    ]
    return list(sorted(
        joined_rooms + pending_rooms,
        key=lambda room_info: (room_info['title'], int(room_info['id']))
    ))
```

Then in the backend view function that templates the page's HTML, we'll prepopulate the latest data in that HTML:

```
# chat_project/chat/views.py

@login_required
def user_home_page(request: HttpRequest) -> HttpResponse:
    ...
    
    last_updated = UserConsumer.create_timepoint()  # capture
    chat_room_list = calculate_chat_room_list(request.user)  # capture
    
    return render(request, 'chat/user_home_page.html', dict(
        user_id=str(request.user.id),
        last_updated=last_updated,
        chat_room_list=chat_room_list,
    ))
```

Then on the frontend JavaScript will wake up and establish a WebSocket connection to the backend, to see if any concurrent changes were made to the room list since the version in the HTML was calculated:

```
# chat_project/chat/static/chat/user_home_page.js

/*public*/ function setupUserHomePage() {
    const userId = JSON.parse(
        document.querySelector('#user-id').innerText);
    const lastUpdated = JSON.parse(
        document.querySelector('#last-updated').innerText);
    setupUserSocket(userId, lastUpdated);
}
```

Whenever a user's room join request is updated, the backend must notify the frontend appropriately through the socket by creating, buffering, and forwarding an event stamped with a new **timepoint**[^timepoint]:

[^timepoint]: A *timepoint* represents a point in time relative to a shared clock. If you have a single shared Redis instance which you're already using to forward socket messages, as is the case with Django's default Channels configuration, it is convenient to use Redis's [TIME](https://redis.io/commands/time) command to generate a timepoint, perhaps as part of a [stored procedure](https://redis.io/commands/eval).

```
# chat_project/chat/models.py

class ChatRoomJoinRequest(models.Model):
    ...  # fields
    
    def save(self, *args, **kwargs) -> None: ...
    
    def notify_did_alter(self,
            action: Literal['create', 'admit', 'deny']) -> None:
        ...
        
        from chat.consumers import UserConsumer  # avoid circular import
        UserConsumer.notify_did_alter_join_request(self, action)
```

```
# chat_project/chat/consumers.py

class UserConsumer(WebsocketConsumer):
    ...
    
    # Send message to group
    @classmethod
    def notify_did_alter_join_request(cls,
            join_request: ChatRoomJoinRequest,
            action: Literal['create', 'admit', 'deny']) -> None:
        update_timepoint = cls.create_timepoint()  # capture
        async_to_sync(get_channel_layer().group_send)(
            cls.user_group_for(join_request.user_id),
            {
                'timepoint': update_timepoint,
                'type': 'did_alter_join_request',
                'kwargs': { ... }
            }
        )
```

When the frontend first connects a socket to the backend, the backend will attempt to immediately forward any events that were buffered since the timepoint passed in the connect call:

```
# chat_project/chat/static/chat/sockets.js

/*public*/ function setupUserSocket(userId, lastUpdated) {
    new WebSocketClient(
        '/ws/user/' + userId + '/' + lastUpdated, {
            onmessage: function(e) {
                didReceiveUserSocketMessage(JSON.parse(e.data));
            },
        }
    );
}

function didReceiveUserSocketMessage(data) {
    var type = data['type'];
    var kwargs = data['kwargs'];
    if (type === 'did_alter_join_request') {
        console.log(
            'User socket: Did alter join request: ' + 
            kwargs['action'] + ' ' + kwargs['id']);
        if (kwargs['action'] === 'create') {
            // TODO: Create a new row on User Home Page in the Rooms section
        } else if (kwargs['action'] === 'admit') {
            // TODO: Promote the row in the Rooms section to be a full room,
            //       removing the "Waiting to be admitted" banner
        } else if (kwargs['action'] === 'deny') {
            // TODO: Remove the row in the Rooms section
        }
    } else {
        console.warn(
            'User socket: Did receive unexpected message type: ' + type);
    }
}
```

That's it! Hopefully you found this technique useful for reliably rendering the freshest information to visitors, even in the presence of concurrent modifications.

### *Related Articles*

In {% assign tag = 'Django' %}{% include blocks/tag_single %}:

* [Real-time updates in Django with WebSockets, Channels, and pub-sub](/articles/2021/03/02/real-time-updates-in-django-with-websockets-channels-and-pub-sub/#models-consumers-and-routes)
* [Building web apps with Vue and Django - The Ultimate Guide](/articles/2021/02/16/building-web-apps-with-vue-and-django-the-ultimate-guide/) - Planning how to integrate Vue with a new or existing Django app
