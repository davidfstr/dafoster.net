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

## Topics and Messages

In a publish-subscribe design, frontend pages subscribe to **topics** that are managed by the backend, by connecting a WebSocket to a `wss://` backend endpoint corresponding to the topic.

The backend sends **messages** to a topic when taking certain actions and those messages are then forwarded on by the topic to all of its subscribers.

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
* Topics such as the User Topic need to *authenticate* its subscribers:
    * In particular the Chat Room Topic will only allow members of the Chat Room to subscribe to it.
    * And the User Topic will only allow its related User to subscribe to it.
* Some Topics choose to forward certain types of messages to only a *subset* of their subscribers. In particular the Chat Room Topic should forward Class Join Request Created messages to the room owner only and not to the other room members.

### Implementation in Django

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

Now let's actually fill out our first consumer, `UserConsumer`, which manages the User Topic:

```
# chat_project/chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from chat.models import ChatRoomJoinRequest
from django.contrib.auth.models import User
import json
from typing import Literal

class UserConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user_group = None
    
    def connect(self) -> None:
        # Authenticate
        if self.user.is_anonymous:
            self.close(code=401)  # Unauthorized
            return
        
        user_id = self.scope['url_route']['kwargs']['user_id']
        
        # Identify requested objects
        try:
            self.requested_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            self.close(code=404)  # Not Found
            return
        
        # Authorize
        if self.requested_user.id != self.user.id:
            self.close(code=403)  # Forbidden
            return
        
        # Join group
        self.user_group = self.user_group_for(user_id)
        async_to_sync(self.channel_layer.group_add)(
            self.user_group,
            self.channel_name
        )
        
        self.accept()

    def disconnect(self, close_code) -> None:
        # Leave group
        if self.user_group is not None:
            async_to_sync(self.channel_layer.group_discard)(
                self.user_group,
                self.channel_name
            )

    # Receive message from page via WebSocket
    def receive(self, text_data) -> None:
        pass
    
    # Send message to group
    @classmethod
    def notify_did_alter_join_request(cls,
            join_request: ChatRoomJoinRequest,
            action: Literal['create', 'admit', 'deny']) -> None:
        async_to_sync(get_channel_layer().group_send)(
            cls.user_group_for(join_request.user_id),
            {
                'type': 'did_alter_join_request',
                'kwargs': {
                    'id': join_request.id,
                    'action': action,
                    'room_id': join_request.room_id,
                }
            }
        )
    
    # Receive message from group
    def did_alter_join_request(self, event) -> None:
        kwargs = event['kwargs']
        
        # Forward message to page via WebSocket
        self.send(text_data=json.dumps({
            'type': 'did_alter_join_request',
            'kwargs': {
                'id': str(kwargs['id']),
                'action': kwargs['action'],
                'room_id': str(kwargs['room_id']),
            }
        }))
    
    # === Group ===
    
    @staticmethod
    def user_group_for(user_id: int) -> str:
        return 'user_%s' % user_id
    
    # === Utility ===
    
    @property
    def user(self) -> User:
        return self.scope['user']
```

When the frontend initiates a WebSocket connection to Django, a consumer wakes up on the backend to manage the socket and attempts to connect to the Channels "group" associated with the topic.

When a new message is posted to the User Topic, via a call to `notify_did_alter_join_request`, that message is first posted to the group, which relays it to all consumers listening to the same group across all backend Django servers. Then each backend consumer, which is one-to-one with a socket connection to a page, will receive the message in `did_alter_join_request` and forward a new message to the frontend through its connected socket.

The `ChatRoomConsumer`, which manages the Chat Room Topic, is written in nearly the same style as the `UserConsumer` above, so I'll won't bother listing its code.

Let's take a look at the frontend code, which opens a socket to the backend and responds to incoming messages from the User Topic:

```
// chat_project/chat/static/chat/sockets.js

/*public*/ function setupUserSocket(userId) {
    new WebSocketClient(
        '/ws/user/' + userId, {
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
        // TODO: Show join request on the User Home Page
        console.log(
            'User socket: Did alter join request: ' + 
            kwargs['action'] + ' ' + kwargs['id']);
    } else {
        console.warn(
            'User socket: Did receive unexpected message type: ' + type);
    }
}
```

> `WebSocketClient` opens and manages a WebSocket, transparently handling connect failures and temporary disconnections, retrying with exponential backoff and jitter. Please substitute your favorite WebSocket management library here.

Now the only piece left is to write some backend code to trigger an event on a `ChatRoomJoinRequest` that is then forwarded to the various sockets:

```
class ChatRoomJoinRequest(models.Model):
    ...  # fields
    
    def notify_did_alter(self,
            action: Literal['create', 'admit', 'deny']) -> None:
        from chat.consumers import UserConsumer  # avoid circular import
        from chat.consumers import ChatRoomConsumer  # avoid circular import
        UserConsumer.notify_did_alter_join_request(self, action)
        ChatRoomConsumer.notify_did_alter_join_request(self, action)
```

Wonderful. Now if you have a `ChatRoomJoinRequest` then you can call `notify_did_alter` on it to fire an event to all consumers, sockets, and pages that are interested in changes to the model!

Let's make a `ChatRoomJoinRequest` model fire a `create` event automatically when it is created by an initial save:

```
class ChatRoomJoinRequest(models.Model):
    ...  # fields
    
    def save(self, *args, **kwargs) -> None:
        change = self.id is not None  # capture
        super().save(*args, **kwargs)
        if not change:  # add
            self.notify_did_alter('create')
    
    def notify_did_alter(self, ...): ...
```

To alter `ChatRoomJoinRequest` such that an **admit** or **deny** action fires an `admit` or `deny` event appropriately, let's temporary add a `status` field to the model, with a "pending", "admitted", or "denied" state, and listen for state changes to determine whether an `admit` or `deny` action has been taken.

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

That's all the code!

### Review of Implementation

Let's review how a particular sequence of actions might be taken on the backend and observed on the frontend in real-time:

* A staff member logs into the Django admin site and creates a `ChatRoomJoinRequest` object:
    * `ChatRoomJoinRequest.save()` triggers and detects a `create` action.
    * `ChatRoomJoinRequest.notify_did_alter()` does forward the message to all interested consumers.
    * `*Consumer.notify_did_alter_join_request()` does forward the message to the Channels group corresponding to the `*` topic (either a User Topic or a Chat Room Topic).
    * `*Consumer.did_alter_join_request()` for all related consumer instances (on all backend servers) does receive the message, and forwards it on to its connected socket.
    * `didReceiveUserSocketMessage` on either the User Home Page or the Chat Room Page does receive the message, and takes action to update the page immediately. ✅
* The staff member changes the `status` field from its default `⏳ Pending` value to be `✅ Admitted`, and presses the "Save and continue" button on the admin page:
    * `ChatRoomJoinRequest.save()` triggers and detects an `admit` action.
    * *(... same intermediate calls as above ...)*
    * `didReceiveUserSocketMessage` on either the User Home Page or the Chat Room Page does receive the message, and takes action to update the page immediately. ✅
* The staff member does press the "Delete" button on the admin page.
    * The `ChatRoomJoinRequest` model is deleted.

## Challenge: Lost events

The above implementation does not handle a particular race condition that can occur if an event of interest (such as the creation of a Chat Message) happens *while* a page (like the Chat Room Page) is loading. Imagine:

* User Alice is on the Chat Room Page and has already posted a first message to the room.
* User Bob requests the Chat Room Page from Django, which renders to HTML the current set of Chat Messages in the Chat Room. The Chat Room Page hasn't yet loaded its JavaScript yet...
* User Alice posts a second message to the room, which fires a `create` action to every loaded page that is listening to the room. However because user Bob's page hasn't finished loading its JavaScript yet, it has not established a socket connection to the backend yet and misses the event.
* User Bob's JavaScript finally loads and establishes a socket connection to the backend.
* User Alice posts a third message to the room, which get observed by user Bob, now that his socket is connected.

By the end of this story Alice has posted three messages to the chat room but Bob only sees the first and third message that Alice posted. Bob missed the second message because it was fired in between when Bob started and finished loading the Chat Room Page.

How can we avoid losing events like this? <a href="javascript:scrollToSubscribeBlock();">Join me next week</a> as I sketch some solutions to this tricky scenario.

Happy coding!

## *Related Articles*

In {% assign tag = 'Django' %}{% include blocks/tag_single %}:

* [Building web apps with Vue and Django - The Ultimate Guide](/articles/2021/02/16/building-web-apps-with-vue-and-django-the-ultimate-guide/)
* [Database clamps](/articles/2021/02/09/database-clamps-deterministic-performance-tests-for-database-dependent-code/) - Writing deterministic performance tests for database-dependent code in Django
* [Tests as Policy Automation](/articles/2021/02/02/tests-as-policy-automation/) - Has ideas for creatively using automated tests to enforce various (non-functional) properties in your Django web app.
