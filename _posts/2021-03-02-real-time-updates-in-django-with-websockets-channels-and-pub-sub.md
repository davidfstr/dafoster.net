---
layout: post
title: Real-time updates in Django with WebSockets, Channels, and pub-sub
tags: [Django, Software]
featured: true
x_audience: |
    Django users who are thinking about adding real-time communication
        to their existing web app, or who are curious about WebSockets
        or Channels in general
x_performance: |
    TODO

style: |
    /* Override blockquote to use same font size as body text */
    blockquote { font-size: 16px !important; }

script: |
    /*public*/ function scrollToSubscribeBlock() {
        var subscribeBlock = document.querySelector('#subscribe-block');
        subscribeBlock.querySelector('.subscribe__prompt').style['backgroundColor'] = '#ffff0070';
        subscribeBlock.scrollIntoView({behavior: 'smooth', block: 'start'});
    }

---
It's easy to build a simple chat server in Channels with real-time updates[^channels-chat-tutorial] but it's a bit more complicated to design a system for a more realistic (and complex) data model that has real-time updates. Here, I will show a **publish-subscribe** (or **“pub-sub”**) **pattern** using WebSockets and Channels that can be used by your frontend to watch elements of your backend data model for updates in real-time.

[^channels-chat-tutorial]: The [official Channels tutorial](https://channels.readthedocs.io/en/latest/tutorial/) has a nice example of building a chat server. (Although since I wrote it I may be biased. 😉)

{% capture toc_content %}

* [Topics and Messages](#topics-and-messages)
* [Simple Example: Public Chat Rooms](#public-chat-rooms)
* [Extended Example: Private Chat Rooms](#private-chat-rooms)
* [Implementation in Django](#implementation-in-django)
    * [Models, Consumers, and Routes](#models-consumers-and-routes)
    * [Connect Frontend to Backend](#connect-frontend-to-backend)
    * [Backend Can Send Messages to Frontend](#backend-can-send-messages-to-frontend)
    * [Backend Triggers Event to Send to Frontend](#backend-triggers-event-to-send-to-frontend)
    * [Wiring up the User Home Page](#wiring-up-the-user-home-page)
    * [Review of Implementation](#review-of-implementation)
* [Challenge: Lost events](#lost-events)

{% endcapture %}

<div class="toc">
  {{ toc_content | markdownify }}
</div>

<a name="topics-and-messages"></a>
## Topics and Messages

In a publish-subscribe design, frontend pages subscribe to **topics** that are managed by the backend, by connecting a WebSocket to a `wss://` backend endpoint corresponding to the topic.

The backend sends **messages** to a topic when taking certain actions and those messages are then forwarded on by the topic to all of its subscribers.

<a name="public-chat-rooms"></a>
## Simple Example: Public Chat Rooms

<a href="/assets/2021/pub-sub/chat-app.svg">
    <img alt="Diagram: Chat app: Models, topics, and pages" src="/assets/2021/pub-sub/chat-app.svg" style="max-width: 100%;" />
</a>

In the context of a simple chat app, there exist Chat Rooms and Chat Messages as models in the database. There also exists a frontend Chat Room Page which is populated with the initial set of Chat Messages on page load. This page wants to observe any new Chat Messages created related to the Chat Room it's displaying.

To observe newly created Chat Messages, the Chat Room Page subscribes to a Chat Room Topic by immediately opening a WebSocket to the topic endpoint as soon as its JavaScript starts running. That topic receives messages like

```
{
    'type': 'chat_message_created',
    'kwargs': {
        'id': '42',
        'message': 'Hello world!'
    }
}
```

which the Chat Room Page then also receives and uses to update its local copy of Chat Messages on the page.

<a name="private-chat-rooms"></a>
## Extended Example: Private Chat Rooms

Let's say you wanted to extend your chat app such that each chat room is owned by a particular user and that other users must get permission from that owning user before they are allowed to join the room:

<a href="/assets/2021/pub-sub/extended-chat-app.svg">
    <img alt="Diagram: Extended chat app: Models, topics, and pages" src="/assets/2021/pub-sub/extended-chat-app.svg" style="max-width: 100%;" />
</a>

Now there are Users, each of which has their own User Home Page which lists the set of Chat Rooms they are already members of and all Chat Rooms that they have submitted a request to join. From this page a user can navigate to a chat room or submit a request to join a new room, perhaps by providing some kind of join code associated with the room.

<a href="/assets/2021/pub-sub/user-home-page.svg">
    <img alt="Diagram: User Home Page" src="/assets/2021/pub-sub/user-home-page.svg" style="max-width: 100%;" />
</a>

Additionally the Chat Room Page is extended so that if the person viewing the Chat Room is also the owner of the Chat Room, the page will display not just the list of users already in the room but also a list of users that have created a join request and are waiting to join the room. The owner can then choose to admit a waiting user to the room or to deny a waiting user from entering.

<a href="/assets/2021/pub-sub/chat-room-page.svg">
    <img alt="Diagram: Chat Room Page" src="/assets/2021/pub-sub/chat-room-page.svg" style="max-width: 100%;" />
</a>

Now things are a bit more complicated:

* There is now an additional User Topic that the User Home Page must subscribe to.
* There is a new Chat Room Join Request model to track which rooms a user has requested to join. **Creating** a new request needs to be observed by the Chat Room Page in real-time so that it can display the new waiting user to the room owner. When the owner chooses to **admit** or **deny** the join request, that action needs to be observed in real-time on the User Home Page of the requesting user.
* A single model (Chat Room Join Request) can have various actions applied to it (create, admit, deny) that are observed by *multiple* types of pages.
* Topics need to *authenticate* its subscribers:
    * In particular the Chat Room Topic will only allow members of the Chat Room to subscribe to it.
    * And the User Topic will only allow its related User to subscribe to it.
* Some Topics choose to forward certain types of messages to only a *subset* of their subscribers. In particular the Chat Room Topic should forward Chat Room Join Request messages to the room owner only and not to the other room members.

<a name="implementation-in-django"></a>
## Implementation in Django

<a name="models-consumers-and-routes"></a>
### Models, Consumers, and Routes

Here's a sketch of what an implementation of the above extended chat app might look like in Django with the Channels library.

First we need some models:

```
# django/contrib/auth/models.py

class User(models.Model): ...  # built-in to Django
```

```
# chat_project/chat/models.py
from django.db import models

class ChatRoom(models.Model):
    owner = models.ForeignKey(
        'User', related_name='owned_room_set', on_delete=models.PROTECT)
    title = models.CharField(max_length=50)
    member_set = models.ManyToManyField(
        'User', related_name='joined_room_set', blank=True)

class ChatMessage(models.Model):
    room = models.ForeignKey(
        'ChatRoom', related_name='message_set', on_delete=models.CASCADE)
    sender = models.ForeignKey(
        'User', related_name='message_set' on_delete=models.PROTECT)
    posted = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=200)

class ChatRoomJoinRequest(models.Model):
    user = models.ForeignKey(
        'User', related_name='join_request_set', on_delete=models.CASCADE)
    room = models.ForeignKey(
        'ChatRoom', related_name='join_request_set', on_delete=models.CASCADE)
```

Then we need some topics. In Django Channels the backend object that manages a topic is called a "consumer", so let's create some consumers:

```
# chat_project/main/routing.py
import chat.routing
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns +
            # (add websocket_urlpatterns from more apps here)
            []
        )
    ),
})
```

```
# chat_project/chat/routing.py
from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/user/(?P<user_id>\d+)$', consumers.UserConsumer),
    url(r'^ws/room/(?P<chat_room_id>\d+)$', consumers.ChatRoomConsumer),
]
```

```
# chat_project/chat/consumers.py
from channels.generic.websocket import WebsocketConsumer

class UserConsumer(WebsocketConsumer): ...

class ChatRoomConsumer(WebsocketConsumer): ...
```

<a name="connect-frontend-to-backend"></a>
### Connect Frontend to Backend

Let's subscribe to a topic from the frontend:

```
// chat_project/chat/static/chat/room.js

/*public*/ function setupChatRoomPage() {
    const roomId = ...;
    
    setupChatRoomSocket(roomId);  // create early to avoid missing events
    
    ...
}
```

```
// chat_project/chat/static/chat/sockets.js

/*public*/ function setupChatRoomSocket(roomId) {
    new WebSocketClient(
        '/ws/room/' + roomId, {
            onmessage: function(e) {
                didReceiveChatRoomSocketMessage(JSON.parse(e.data));
            },
        }
    );
}

function didReceiveChatRoomSocketMessage(data) {
    ...
}
```

> `WebSocketClient` opens and manages a WebSocket, transparently handling connect failures and temporary disconnections, retrying with exponential backoff and jitter. Please substitute your favorite WebSocket management library here.

Now let's fill out the consumer on the backend so that it can accept a connection from the frontend:

```
# chat_project/chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from chat.models import ChatRoom
from django.contrib.auth.models import User
import json

class ChatRoomConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user_group = None
    
    def connect(self) -> None:
        # Authenticate
        if self.user.is_anonymous:
            self.close(code=401)  # Unauthorized
            return
        
        room_id = self.scope['url_route']['kwargs']['room_id']
        
        # Identify requested objects
        try:
            self.room = ChatRoom.objects.get(id=room_id)
        except ChatRoom.DoesNotExist:
            self.close(code=404)  # Not Found
            return
        
        # Authorize
        if (self.user.id != self.room.owner_id and 
                self.user not in self.room.member_set.all()):
            self.close(code=403)  # Forbidden
            return
        
        # Join group
        self.room_group = self.room_group_for(room_id)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group,
            self.channel_name
        )
        
        self.accept()
    
    def disconnect(self, close_code) -> None: ...
    
    # === Group ===
    
    @staticmethod
    def room_group_for(room_id: int) -> str:
        return 'room_%s' % room_id
    
    # === Utility ===
    
    @property
    def user(self) -> User:
        return self.scope['user']
```

In a regular Django view:

* We'd normally use the `@login_required` decorator
  to authenticate a user but here we need to do that manually by checking
  `user.is_anonymous` and returning WS 401 Unauthorized manually if the
  user hasn't logged in.

* We'd normally receive parameters from the URL as arguments to the view
  function but here we have to look up the arguments manually from
  `self.scope['url_route']['kwargs']['PARAMETER_NAME']` instead.

* When authorizing we'd normally check properties of `request.user`
  against the room ownership and membership, but here we must check
  `self.user` (which is a shortcut for `self.scope['user']`) instead.
  A failure would normally be reported using an `HttpResponseForbidden`
  but here we must manually return a WS 403 Forbidden code.

At the end of the connection sequence the consumer adds itself to the
Channels "group" for all consumers related to the same room topic.

Upon disconnection the consumer also need to unregister from the group:

```
class ChatRoomConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs) -> None: ...
    
    def connect(self) -> None: ...

    def disconnect(self, close_code) -> None:
        # Leave group
        if self.room_group is not None:
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group,
                self.channel_name
            )
    
    ...
```

This consumer does not expect to *receive* any incoming messages from the frontend; it only expects to *send* messages to the frontend later:

```
class ChatRoomConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs) -> None: ...
    
    def connect(self) -> None: ...
    
    def disconnect(self, close_code) -> None: ...

    # Receive message from page via WebSocket
    def receive(self, text_data) -> None:
        pass
    
    ...
```

<a name="backend-can-send-messages-to-frontend"></a>
### Backend Can Send Messages to Frontend

Okay now we have the frontend connecting to the backend. How about we trigger an event on the backend such that it gets observed by the frontend in real-time?

Let's create a helper method on the consumer that sends an event to all other consumers in the same topic, and forwards it on to the frontend through the consumer's connected socket:

```
# chat_project/chat/consumers.py
...
from chat.models import ChatRoomJoinRequest
from typing import Literal

class ChatRoomConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs) -> None: ...
    
    def connect(self) -> None: ...
    
    def disconnect(self, close_code) -> None: ...
    
    def receive(self, text_data) -> None: ...
    
    # Send message to group
    @classmethod
    def notify_did_alter_join_request(cls,
            join_request: ChatRoomJoinRequest,
            action: Literal['create', 'admit', 'deny']) -> None:
        async_to_sync(get_channel_layer().group_send)(
            cls.room_group_for(join_request.room_id),
            {
                'type': 'did_alter_join_request',
                'kwargs': {
                    'id': join_request.id,
                    'action': action,
                    'requesting_user': {
                        'id': join_request.user_id,
                        'first_name': join_request.user.first_name,
                        'last_name': join_request.user.last_name,
                    } if action == 'create' else None
                }
            }
        )
    
    # Receive message from group
    def did_alter_join_request(self, event) -> None:
        kwargs = event['kwargs']
        
        # Only the room owner may observe join request events so suppress for other users
        if self.user.id == self.room.owner_id:
            # Forward message to page via WebSocket
            self.send(text_data=json.dumps({
                'type': 'did_alter_join_request',
                'kwargs': {
                    'id': str(kwargs['id']),
                    'action': kwargs['action'],
                    'requesting_user': kwargs['requesting_user'],
                }
            }))
```

Notice that only the room *owner* (and not its other *members*) are notified of events related to join-requests, since the room owner is the only one with the ability to admit or deny folks trying to join the room.

Now we need to receive that forwarded event on the frontend:

```
// chat_project/chat/static/chat/sockets.js

/*public*/ function setupChatRoomSocket(roomId) { ... }

function didReceiveChatRoomSocketMessage(data) {
    var type = data['type'];
    var kwargs = data['kwargs'];
    if (type === 'did_alter_join_request') {
        console.log(
            'Chat room socket: Did alter join request: ' + 
            kwargs['action'] + ' ' + kwargs['id']);
        
        if (kwargs['action'] === 'create') {
            // TODO: Create a new row on Chat Room Page in the Members section
        } else if (kwargs['action'] === 'admit') {
            // TODO: Promote the row in the Members section to a full member of
            //       the room, removing the "Deny" and "Allow" buttons
        } else if (kwargs['action'] === 'deny') {
            // TODO: Remove the row in the Members section
        }
    } else {
        console.warn(
            'Chat room socket: Did receive unexpected message type: ' + type);
    }
}
```

We've now carved out a path for events related to join-requests to be forwarded all the way to the frontend in real-time.

<a name="backend-triggers-event-to-send-to-frontend"></a>
### Backend Triggers Event to Send to Frontend

We still need to actually *trigger* the event in the backend by calling <code>ChatRoomConsumer.<wbr/>notify_did_alter_join_request()</code> somewhere.

Let's make a `ChatRoomJoinRequest` model fire a `create` event automatically when it is created by an initial save:

```
# chat_project/chat/models.py

class ChatRoomJoinRequest(models.Model):
    ...  # fields
    
    def save(self, *args, **kwargs) -> None:
        change = self.id is not None  # capture
        super().save(*args, **kwargs)
        if not change:  # add
            self.notify_did_alter('create')
    
    def notify_did_alter(self,
            action: Literal['create', 'admit', 'deny']) -> None:
        from chat.consumers import ChatRoomConsumer  # avoid circular import
        ChatRoomConsumer.notify_did_alter_join_request(self, action)
        
        # NOTE: In the future we'll want to notify the User Home Page here too
        #from chat.consumers import UserConsumer  # avoid circular import
        #UserConsumer.notify_did_alter_join_request(self, action)
```

Now if a `ChatRoomJoinRequest` is created in the Django admin site, its creation should be observed in real-time by the Chat Room Page. Great!

Now let's alter `ChatRoomJoinRequest` such that an **admit** or **deny** action fires an `admit` or `deny` event appropriately. We can temporary add a `status` field to the model, with a "pending", "admitted", or "denied" state, and listen for state changes to determine whether an `admit` or `deny` action has been taken:

```
class ChatRoomJoinRequest(models.Model):
    ...  # original fields
    status = models.CharField(
        max_length=10,
        choices=[
            ('pending', '⏳ Pending'),
            ('admitted', '✅ Admitted'),
            ('denied', '✖️ Denied'),
        ],
        default='pending',
    )
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._initial_status = self.status
    
    def save(self, *args, **kwargs) -> None:
        change = self.id is not None  # capture
        super().save(*args, **kwargs)
        if not change:  # add
            self.notify_did_alter('create')
        else:  # change
            if self.status != self._initial_status:
                if self.status == 'admitted':
                    self.notify_did_alter('admit')
                elif self.status == 'denied':
                    self.notify_did_alter('deny')
    
    def notify_did_alter(self, ...): ...
```

Now if the `status` field of a `ChatRoomJoinRequest` is changed in the Django admin site, the related `admit` or `deny` event should be observed in real-time by the Chat Room Page. Fantastic!

Now *all* actions that can be taken on a `ChatRoomJoinRequest` can be observed by the Chat Room Page in real-time. ✅ But what the User Home Page? It also wants to be notified of events related to join-requests.

<a name="wiring-up-the-user-home-page"></a>
### Wiring up the User Home Page

Recall that the User Home Page also wants to observe events related to `ChatRoomJoinRequest`s so that it can notify a user whether their request to join a room was approved or denied by the room owner, in real-time.

Similar to how the Chat Room Page observes events in real-time, we'll need to create a User Topic that is backed by a frontend socket and a backend consumer that manages that socket (`UserConsumer`).

The code for `setupUserSocket` is in the same pattern as that for `setupChatRoomSocket` so I won't bother listing it.

Ditto for `UserConsumer`, whose code is similar to that for `ChatRoomConsumer`.

Now we need to link `ChatRoomJoinRequest.notify_did_alter` to notify not just the Chat Room Topic of changes, but also the User Topic via <code>UserConsumer.<wbr/>notify_did_alter_join_request</code>:

```
# chat_project/chat/models.py

class ChatRoomJoinRequest(models.Model):
    ...  # fields
    
    def save(self, *args, **kwargs) -> None:
        change = self.id is not None  # capture
        super().save(*args, **kwargs)
        if not change:  # add
            self.notify_did_alter('create')
    
    def notify_did_alter(self,
            action: Literal['create', 'admit', 'deny']) -> None:
        from chat.consumers import ChatRoomConsumer  # avoid circular import
        ChatRoomConsumer.notify_did_alter_join_request(self, action)
        
        from chat.consumers import UserConsumer  # avoid circular import
        UserConsumer.notify_did_alter_join_request(self, action)
```

<a name="review-of-implementation"></a>
### Review of Implementation

Congratulations! You've wired up a non-trivial chat server that can admit and deny requests to join private chat rooms! 🎉

Let's review how a particular sequence of actions might be taken on the backend and observed on the frontend in real-time:

* A staff member logs into the Django admin site and creates a `ChatRoomJoinRequest` object:
    * `ChatRoomJoinRequest.save()` triggers and detects a `create` action.
    * <code>ChatRoomJoinRequest.<wbr/>notify_did_alter()</code> does forward the message to all interested consumers.
    * <code>*Consumer.<wbr/>notify_did_alter_join_request()</code> does forward the message to the Channels group corresponding to the `*` topic (either a Chat Room Topic or a User Topic).
    * <code>*Consumer.<wbr/>did_alter_join_request()</code> for all related consumer instances (on all backend servers) does receive the message, and forwards it on to its connected socket.
    * `didReceive*SocketMessage` on either the Chat Room Page or User Home Page does receive the message, and takes action to update the page immediately. ✅
* The staff member changes the `status` field from its default `⏳ Pending` value to be `✅ Admitted`, and presses the "Save and continue" button on the admin page:
    * `ChatRoomJoinRequest.save()` triggers and detects an `admit` action.
    * *(... same intermediate calls as above ...)*
    * `didReceive*SocketMessage` on either the Chat Room Page or User Home Page does receive the message, and takes action to update the page immediately. ✅
* The staff member does press the "Delete" button on the admin page.
    * The `ChatRoomJoinRequest` model is deleted.

<a name="lost-events"></a>
## Challenge: Lost events

The above implementation does not handle a particular race condition that can occur if an event of interest (such as the creation of a Chat Message) happens *while* a page (like the Chat Room Page) is loading. Imagine:

* User Alice is on the Chat Room Page and has already posted a first message to the room.
* User Bob requests the Chat Room Page from Django, which renders to HTML the current set of Chat Messages in the Chat Room. Bob's Chat Room Page hasn't yet loaded its JavaScript yet...
* Alice posts a second message to the room, which fires a `create` action to every loaded page that is listening to the room. However because Bob's page hasn't finished loading its JavaScript yet, it has not established a socket connection to the backend yet and misses the event.
* Bob's JavaScript finally loads and establishes a socket connection to the backend.
* Alice posts a third message to the room, which get observed by Bob, now that his socket is connected.

By the end of this story Alice has posted three messages to the chat room but Bob only sees the first and third message that Alice posted. Bob missed the second message because it was fired in between when Bob started and finished loading the Chat Room Page.

How can we avoid losing events like this? <a href="javascript:scrollToSubscribeBlock();">Join me next week</a> as I sketch some solutions to this tricky scenario.

Happy coding!

### *Related Articles*

In {% assign tag = 'Django' %}{% include blocks/tag_single %}:

* [Building web apps with Vue and Django - The Ultimate Guide](/articles/2021/02/16/building-web-apps-with-vue-and-django-the-ultimate-guide/) - Planning how to integrate Vue with a new or existing Django app
* [Database clamps](/articles/2021/02/09/database-clamps-deterministic-performance-tests-for-database-dependent-code/) - Writing deterministic performance tests for database-dependent code in Django
* [Tests as Policy Automation](/articles/2021/02/02/tests-as-policy-automation/) - Has ideas for creatively using automated tests to enforce various (non-functional) properties in your Django web app.
