import xmpp
import slixmpp

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
		