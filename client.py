import slixmpp
import asyncio
import xmpp
import time
from config import WAIT
from aioconsole import ainput
from aioconsole.stream import aprint
from utils import get_login_menu_option, get_status, get_chat_room_option
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET

class Client(slixmpp.ClientXMPP):
	"""
	A client class to manage conections an functionalities
	Atributes:
		jid: string with the JID of the client.
		password: string
		is_remove: boolean to indicate if need to delete the account
	"""
	def __init__(self, jid, password, status, status_message):
		super().__init__(jid, password)
		self.name = jid.split('@')[0]
		self.status = status
		self.status_message = status_message
		self.actual_chat = ''

		# # plugins
		self.register_plugin('xep_0030') # Service Discovery
		self.register_plugin('xep_0199') # Ping
		self.register_plugin('xep_0045') # MUC
		self.register_plugin('xep_0085') # Notifications
		self.register_plugin('xep_0004') # Data Forms
		self.register_plugin('xep_0060') # PubSub


		# events
		self.add_event_handler('session_start', self.start)
		self.add_event_handler('message', self.chat_recived)
		self.add_event_handler('groupchat_message', self.chatroom_message)
		self.add_event_handler('disco_items', self.print_rooms)


	async def start(self, event):
		"""
		Start the client and connect to the server.
		"""
		try:
			self.send_presence(pshow=self.status, pstatus=self.status_message) # send presence to the server
			await self.get_roster() # get the roster
			print('Welcome to the chat')
			# TODO - add the menu logic for user interaction here
			# TODO - move this into a function in utils
			# chat(self)
			connected = True
			while connected:
				option = await get_login_menu_option()
				if option == 1:
					"""
					Get information from specific user
					"""
					print('show info from specific user')
					jid = input('Enter the JID of the user:\n>')
					roster = self.client_roster.groups()
					my_contacts = []
					for group in roster:
						for contact in roster[group]:
							show = 'Avialable'
							status = ''
							conection = self.client_roster.presence(contact)
							contactUserName = contact.split('@')[0]
							if conection.items():
								for answare, presence in conection.items():
									if presence['show']:
										show = presence['show']
									if presence['status']:
										status = presence['status']
							else:
								show = 'Offline'
							my_contacts.append({
								'name': contactUserName,
								'state': show,
								'status': status,
								'user': contact
							})
					if my_contacts:
						for contact in my_contacts:
							if jid == contact['user']:
								print(f'JID >> {contact["user"]}')
								print(f'User name >> {contact["name"]}')
								print(f'State >> {contact["state"]}')
								if contact['state'] != 'Offline':
									print(f'Status >> {contact["status"]}')
								print('===================\n')
					else:
						print('No contacts to show, add some friends!')
					time.sleep(WAIT)
				elif option == 2:
					"""
					Add contact
					"""
					print('==================== Add contact ====================')
					print('Write the JID of the contact: ')
					jid = input('> ')
					if (jid is not None) and (jid != ''):
						self.send_presence_subscription(pto = jid)
						print('Contact request sent')
					else:
						print('Invalid JID')
					time.sleep(WAIT)
				elif option == 3:
					"""
					Show contact's info
					"""
					print('show contacts info')
					roster = self.client_roster.groups()
					my_contacts = []
					for group in roster:
						for contact in roster[group]:
							show = 'Avialable'
							status = ''
							conection = self.client_roster.presence(contact)
							contactUserName = contact.split('@')[0]
							if conection.items():
								for answare, presence in conection.items():
									if presence['show']:
										show = presence['show']
									if presence['status']:
										status = presence['status']
							else:
								show = 'Offline'
							my_contacts.append({
								'name': contactUserName,
								'state': show,
								'status': status,
								'user': contact
							})
					if my_contacts:
						print('Contacts:\n')
						for contact in my_contacts:
							if contact['name'] != self.name:
								print(f'JID >> {contact["user"]}')
								print(f'User name >> {contact["name"]}')
								print(f'State >> {contact["state"]}')
								if contact['state'] != 'Offline':
									print(f'Status >> {contact["status"]}')
								print('===================\n')
					else:
						print('No contacts to show, add some friends!')
					time.sleep(WAIT)
				elif option == 4:
					"""
					Send message to specific user
					"""
					jid = await ainput('Enter the JID of the user:\n>')
					self.actual_chat = jid
					await aprint(f'===================== Welcom to the chat with {jid.split("@")[0]} =====================')
					await aprint('To exit the chat, type "exit" and then press enter')
					chatting = True
					while chatting:
						message = await ainput('> ')
						if message == 'exit':
							chatting = False
							self.actual_chat = ''
						else:
							self.send_message_p_g(jid, message)
							await asyncio.sleep(0.5) # wait 0.5 seconds to make sure the message was sent
				elif option == 5:
					print('send group message')
					"""
					CHAT WITH GROUP
					"""
					option_rooms = get_chat_room_option()
					if option_rooms == 1:
						"""
						Create a new chat room
						"""
						nickName = input('Enter your nick name:\n> ')
						roomName = input('Enter the name of the new room:\n> ')
						roomName = f'{roomName}@conference.alumchat.fun'
						self.create_chat_room(roomName, nickName)
						print(f'===================== Welcom to the chat with {roomName.split("@")[0]} =====================')
						print('To exit the chat, type "exit" and then press enter')
						still_in_room = True
						while still_in_room:
							message = await ainput('> ')
							if message == 'exit':
								still_in_room = False
								# leave the room
								self.exit_room()
							else:
								self.send_message_p_g(roomName, message, "groupchat")
								await asyncio.sleep(0.5)
					elif option_rooms == 2:
						"""
						Join an existing chat room
						"""
						nickName = input('Enter your nick name:\n> ')
						roomjid = input('Enter the JID of the room:\n> ')
						self.join_chat_room(roomjid, nickName)
						print(f'===================== Welcom to the chat with {roomjid.split("@")[0]} =====================')
						print('To exit the chat, type "exit" and then press enter')
						still_in_room = True
						while still_in_room:
							message = await ainput('> ')
							if message == 'exit':
								still_in_room = False
								# leave the room
								self.exit_room()
							else:
								self.send_message_p_g(roomjid, message, "groupchat")
								await asyncio.sleep(0.5)
					elif option_rooms == 3:
						"""
						Show chat rooms
						"""
						try:
							await self.get_rooms()
						except (IqError, IqTimeout):
							print("Error on discovering rooms")
					elif option_rooms == 4:
						"""
						Exit from chat room
						"""
						pass
				elif option == 6:
					"""
					Change status
					"""
					status, status_message = get_status()
					self.status = status
					self.status_message = status_message
					self.send_presence(pshow=self.status, pstatus=self.status_message) # send presence to the server
					await self.get_roster() # get the roster
				elif option == 7:
					"""
					Logout
					"""
					self.send_presence(pshow='Away', pstatus='Logged out') # send presence to the server
					self.disconnect()
					connected = False
					print('Logged out')
		except IqError as err:
			print(f"Error: {err.iq['error']['text']}")
			self.disconnect()
		except IqTimeout:
			print('Error: Server is taking too long to respond')
			self.disconnect()

	def send_message_p_g(self, to, message = '', typeM = "chat"):
		"""
		Send message to a user (private message)
		"""
		# print(f'Sending message to {to}')
		# print(f'Message: {message}')
		self.send_message(
			mto=to,
			mbody=message,
			mtype=typeM
		)
		# print('Message sent succefully')

	async def get_rooms(self):
		"""
		Get all chat rooms
		"""
		print('Getting chat rooms...')
		try:
			await self['xep_0030'].get_items(jid = "conference.alumchat.fun")
		except (IqError, IqTimeout):
			print("There was an error, please try again later")
		# print('Chat rooms retrieved')

	def print_rooms(self, iq):
		"""
		Print the chat rooms received
		"""
		if iq['type'] == 'result':
			print('Rooms available:')
			for room in iq["disco_items"]:
				print(f'{room["name"]}')
				print(f'JID: {room["jid"]}')
				print('=====================')
			time.sleep(WAIT)

	def join_chat_room(self, room, nickName):
		"""
		To join a chat room
		"""
		# set room properties
		self.room = room
		self.nickName = nickName
		print('room', self.room)

		# join and create handlers for rooms
		self['xep_0045'].join_muc(room, nickName, maxhistory=False)
		self.add_event_handler(f"muc::{self.room}::got_online", self.on_join_chatroom)
		self.add_event_handler(f"muc::{self.room}::got_offline", self.on_left_chatroom)

	async def on_join_chatroom(self, presence):
		"""
		When a user joins the chat room
		"""
		await aprint(f'\t{str(presence["muc"]["nick"])} joined the chat room')

	async def on_left_chatroom(self, presence):
		await aprint(f'\t{str(presence["muc"]["nick"])} just left the chat room')

	def exit_room(self):
		self['xep_0045'].leave_muc(self.room, self.nickName)
		# erase data for the room
		self.room = None
		self.nickName = None

	def create_chat_room(self, roomName, nickName):
		"""
		Create new chat room
		"""
		self.room = roomName
		self.nickName = nickName

		# Create
		self['xep_0045'].join_muc(self.room, self.nickName)

		# Event handlers
		self.add_event_handler(f"muc::{self.room}::got_online", self.on_join_chatroom)
		self.add_event_handler(f"muc::{self.room}::got_offline", self.on_left_chatroom)

		try:
			# send the onwner of the room
			query = ET.Element('{http://jabber.org/protocol/muc#owner}query')
			elementType = ET.Element('{jabber:x:data}x', type='submit')
			query.append(elementType)

			iq = self.make_iq_set(query)
			iq['to'] = self.room
			iq['from'] = self.boundjid
			iq.send()
		except Exception:
			print("Room could not be created, try again later")

	async def chatroom_message(self, message=''):
		"""
		Recivea message from a chat room
		"""
		user = message['mucnick']
		is_actual_room = self.room in str(message['from'])
		display_message = f'{user}: {message["body"]}'

		if is_actual_room and user != self.nickName:
			await aprint(display_message)

	async def chat_recived(self, message):
		# await aprint('New message', message)
		if message['type'] == 'chat':
			user = str(message['from']).split('@')[0]
			if user == self.actual_chat.split('@')[0]:
				print(f'{user}: {message["body"]}')
			else:
				print(f'You have a new message from {user}')