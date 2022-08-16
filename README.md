# Proyecto-1-Redes

## Objectives

- Understand the standards of a known and open protocol.
- Understand the basics of asynchronous programming required to solve the
network development needs.

## Difficulties

Get the messages first, because if you have a client with an interface open at the same time as the client in the console, the client with an interface intercepts the messages, so they never reach the console client, so it took me a while to realize the error, since it was not a code error or anything like that. Second, the little documentation that there was to investigate. Finally, sending the files due to the errors that occurred when trying to send and receive the files, due to their format

## Learned lessons
- Understand the standards of an open protocol in order to apply them in the future.
- Understand the basics of asynchronous communication in order to solve network problems.
- To be able to handle in parallel the sending and capturing of data.

## Implemented Features

### Account Management
- Register a new account on the server.
- Sign in with an account.
- Sign out with an account.
- Delete server account.

### Communication
- Show all users/contacts and their status.
- Add a user to contacts.
- Show contact details of a user.
- 1 to 1 communication with any user/contact.
- Participate in group conversations.
- Define presence message.
- Send/receive notifications.
- Send/receive files.

## How to install / Use it

Make sure to install the following libraries:
```
pip install slixmpp
pip install aioconsole
pip install xmpppy
```
Run the client:
```
python3 cliente.py
```

