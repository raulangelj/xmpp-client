import slixmpp
import asyncio
import logging
from slixmpp.exceptions import IqError, IqTimeout

class Client(slixmpp.ClientXMPP):
	def __init__(self, jid, password, create_account=False):
		super().__init__(jid, password)
		self.create_account = create_account
		

		# Plugins
		# self.register_plugin('xep_0030') # Service Discovery
		# self.register_plugin('xep_0004') # Data forms
		# self.register_plugin('xep_0066') # Out-of-band Data
		# self.register_plugin('xep_0045') # Multi-User Chat
		# self.register_plugin('xep_0060') # PubSub
		# self.register_plugin('xep_0199') # XMPP Ping
		# self.register_plugin('xep_0071') # XHTML
		# self.register_plugin('xep_0133') # Service administration
		# self.register_plugin('xep_0065') # Sockss bytestreams
		# self.register_plugin('xep_0085') # Notifications
		# self.register_plugin('xep_0128') # service discovery
		# self.register_plugin('xep_0054') # for vmCard (profile)
		# self.register_plugin('xep_0082') # for vmCard (profile)
		# self.register_plugin('xep_0077') # In-band Registration
		# self.register_plugin('xep_0363') # Files
		self.register_plugin('xep_0030') # Service Discovery
		self.register_plugin('xep_0004') # Data forms
		self.register_plugin('xep_0066') # Out-of-band Data
		self.register_plugin('xep_0077') # In-band Registration		
		# Force registration when sending stanza
		self['xep_0077'].force_registration = True

		# forece registration when sending stanza
		# self['xep_0077'].force_registration = True

		# Event handlers
		
		# # Event for maganage conection
		# self.connected_event = asyncio.Event()
		# self.presences_received = asyncio.Event()

		self.add_event_handler("session_start", self.start)
		self.add_event_handler("register", self.register)

	async def start(self, event):
		print("start")
		self.send_presence()
		# Auto register & disconnect
		await self.get_roster()
		# self.connected_event.set()
		# self.disconnect()

	async def register(self, iq):
		print("register")
		payload = self.Iq()
		payload['type'] = 'set'
		print('username', self.boundjid.user)
		print('password', self.password)
		payload['register']['username'] = self.boundjid.user
		payload['register']['password'] = self.password

		try:
			await payload.send()
			logging.info(f"Account created for {self.boundjid}!")
			print(f"Account registered successfully: {self.boundjid}!")
		except IqError as e:
			logging.error(f"Could not register account: {e.iq['error']['text']}")
			print(f"Error on register new account: {e.iq['error']['text']}")
			self.disconnect()
		except IqTimeout:
			logging.error("No response from server.")
			print("No response from server.")
			self.disconnect()
			


