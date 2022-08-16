# 💻 XMPP Client

Simple XMPP Client ussing Python, Slixmpp and xmpppy

## 🛠 Installation requirements

(optional)

1. Create the virtual enviroment ```python -m venv venv```
2. Activate the virtual enviroment ```. venv/Scripts/activate```

(install dependencies)

3. pip install -r requirements.txt

## Running the proyect 🚀

```shell
  python main.py
```

### Useful flags for debugin

- ```-d```: for slixmpp debuggin mode
- ```-q```: for slixmpp only critial error mode


## 📋 Features

This client provides basic chat features throughout the CLI interface.

- [x] Sign Up with a new account.
- [X] Log in with an existent account.
- [X] Log out from an existing account.
- [x] Delete an account from the server.
- [X] Display contants info and state.
- [X] Display information of specific contact.
- [X] Add a new contact.
- [X] Message 1 to 1.
- [X] Chat rooms.
  - [X] View available rooms.
  - [X] Join an exiting chatroom.
  - [X] Create a new chatroom.
- [X] Create presence Message.
- [X] Send/Receive notifications.
- [ ] Send/Receive Files.
