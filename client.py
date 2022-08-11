import logging
from time import time
from traceback import print_tb
import slixmpp
import asyncio
import xmpp
import time
from config import WAIT, MESSAGE_TYPE
from utils import get_login_menu_option, get_status
from slixmpp.exceptions import IqError, IqTimeout

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

		# # plugins
		self.register_plugin('xep_0030') # Service Discovery
		self.register_plugin('xep_0199') # Ping

		# events
		self.add_event_handler('session_start', self.start)


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
				option = get_login_menu_option()
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
					jid = input('Enter the JID of the user:\n>')
					print(f'===================== Welcom to the chat with {jid.split("@")[0]} =====================')
					print('To exit the chat, type "exit" and then press enter')
					chatting = True
					while chatting:
						message = input('> ')
						if message == 'exit':
							chatting = False
						else:
							self.send_private_message(jid, message)
							await asyncio.sleep(0.5) # wait 0.5 seconds to make sure the message was sent
				elif option == 5:
					print('send group message')
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

	def send_private_message(self, to, message = ''):
		"""
		Send message to a user (private message)
		"""
		# print(f'Sending message to {to}')
		# print(f'Message: {message}')
		self.send_message(
			mto=to,
			mbody=message,
			mtype=MESSAGE_TYPE
		)
		# print('Message sent succefully')