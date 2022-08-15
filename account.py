import xmpp
import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET

def sign_in(client, password):
	"""
	Function to sign in to the server.
	Atributes:
		client: string with the JID of the client.
		password: string
	Returns:
		True if the client is signed in, False otherwise.
	"""
	jid = xmpp.JID(client)
	account = xmpp.Client(jid.getDomain(), debug=[])
	account.connect()
	return bool(
	    xmpp.features.register(account, jid.getDomain(), {
	        'username': jid.getNode(),
	        'password': password
	    }))

class Delete_account(slixmpp.ClientXMPP):
	"""
	A delete account class to remove the account from the server.
	Attributes:
		jid: string with the JID of the client.
		password: string
	"""
	def __init__(self, jid, password):
		slixmpp.ClientXMPP.__init__(self, jid, password)
		self.user = jid
		# event handler for the session_start event
		self.add_event_handler("session_start", self.start)

	async def start(self, event):
		self.send_presence()
		await self.get_roster()
		# unregister & disconnect
		await self.unregister()
		self.disconnect()

	async def unregister(self):
		"""
		Function to unregister the client from the server.
		"""
		response = self.Iq()
		response['type'] = 'set'
		response['from'] = self.boundjid.user
		fragment = ET.fromstring("<query xmlns='jabber:iq:register'><remove/></query>")
		response.append(fragment)

		try:
			# send the request to the server
			await response.send()
			print(f"Account deleted successfully: {self.boundjid.jid}!")
		except IqError as e:
			print(f"Error on deleted account: {e.iq['error']['text']}")
			self.disconnect()
		except IqTimeout:
			print("No response from server.")
			self.disconnect()