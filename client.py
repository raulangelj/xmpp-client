import logging
from time import time
from traceback import print_tb
import slixmpp
import asyncio
import xmpp
import time
from config import WAIT
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
		# self.register_plugin('xep_0054') # for vmCard (profile)
		# self.register_plugin('xep_0082') # for vmCard (profile)

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
					# jid = input('Enter the JID of the user:\n>')
					# recv = await self.plugin['xep_0054'].get_vcard(
					# 	jid
					# )
					# # print('recv:', recv)
					# # print('search ', recv['vcard_temp']['FN'])
					# # print('search ', recv['from'])
					# # https://slixmpp.readthedocs.io/en/latest/api/plugins/xep_0054.html?highlight=%3CvCard%20xmlns%3D%22vcard-temp%22%20%2F%3E
					# # https://xmpp.org/extensions/xep-0054.html
					# if recv:
					# 	print('==================== Get Profil info ====================')
					# 	print(f'JID >> {recv["from"]}')
					# 	print('reciv', ["vcard_temp"])
					# 	print(f'User name >> {recv["vcard_temp"]["FN"]}')
					# else:
					# 	print('User not found')
					# # roster = self.client_roster.groups()
					# # search_contact = {}
					# # for group in roster:
					# # 	for contact in roster[group]:
					# # 		show = 'Avialable'
					# # 		status = ''
					# # 		conection = self.client_roster.presence(contact)
					# # 		contactUserName = contact.split('@')[0]
					# # 		if contact == jid:
					# # 			if conection.items():
					# # 				for answare, presence in conection.items():
					# # 					if presence['show']:
					# # 						show = presence['show']
					# # 					if presence['status']:
					# # 						status = presence['status']
					# # 			else:
					# # 				show = 'Offline'
					# # 			search_contact = {
					# # 				'name': contactUserName,
					# # 				'state': show,
					# # 				'status': status,
					# # 				'user': contact
					# # 			}
					# # if search_contact:
					# # 	print('==================== Get Profil info ====================')
					# # 	print(f'JID >> {search_contact["user"]}')
					# # 	print(f'User name >> {search_contact["name"]}')
					# # 	print(f'State >> {search_contact["state"]}')
					# # 	print(f'Status >> {search_contact["status"]}')
					# # else:
					# # 	print('User not found in the contacts')
					# # time.sleep(WAIT)
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
					print('send private messsage')
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

	# def get_vcard_callback(self, event):
	# 	"""
	# 	Callback for get_vcard.
	# 	"""
	# 	print('==================== Get Profil info ====================')
	# 	print(f'JID >> {event["from"]}')
	# 	print(f'User name >> {event["vcard_temp"]["FN"]}')
