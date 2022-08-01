import logging
import slixmpp
import asyncio
from utils import get_login_menu_option, chat
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
			self.send_presence(pshow=self.status, pstatus=self.status_message
			) # send presence to the server
			await self.get_roster() # get the roster
			print('Welcome to the chat')
			# TODO - add the menu logic for user interaction here
			# TODO - move this into a function in utils
			# chat(self)
			connected = True
			while connected:
				option = get_login_menu_option()
				if option == 1:
					print('Show contacts')
				elif option == 2:
					print('Add contact')
				elif option == 3:
					print('show contacts info')
				elif option == 4:
					print('send private messsage')
				elif option == 5:
					print('send group message')
				elif option == 6:
					print('change status')
				elif option == 7:
					print('logout')
					self.disconnect()
					connected = False
		except IqError as err:
			print(f"Error: {err.iq['error']['text']}")
			self.disconnect()
		except IqTimeout:
			print('Error: Server is taking too long to respond')
			self.disconnect()


