import logging
import aiodns
import asyncio
from account import *
from utils import *
from optparse import OptionParser
from menus_texts import *

async def chat():
	connected = True
	print('User coneected successfully')
	while connected:
		option = get_login_menu_option()

  

if __name__ == "__main__":
	optp = OptionParser()
	optp.add_option('-d', '--debug', help='set loggin to DEBUG', action='store_const', dest='loglevel', const=logging.DEBUG, default=logging.INFO)

	opts, args = optp.parse_args()

	# ! DO NOT DELETE THIS LINE, PATCH A ERROR ON ASYNCIO LIB
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

	logging.basicConfig(level=opts.loglevel, format='%(levelname)-8s %(message)s')

	option = None
	while option != 4:
		# Get the first option from the main menu
		option = get_principal_menu_option()

		# OPTION 1: Register
		if option == 1:
			jid, password = get_jid_and_password()
			if not sign_in(jid, password):
				print("Error signing in, please try again")
			else:
				print("Signed in successfully")
			# TODO - ask if user want to log in and add login logic
			option = get_principal_menu_option()
		# OPTION 2: Login
		if option == 2:
			jid, password = get_jid_and_password()
			# client = Client(jid, password)
			# client.connect(force_starttls=False)
			# client.process(forever=False)
			# chat()
		# OPTION 3: Remove account
		if option == 3:
			jid, password = get_jid_and_password()
			client = Delete_account(jid, password)
			client.connect(force_starttls=False)
			client.process(forever=False)
		# OPTION 4: Exit login
		if option == 4:
			print("Goodbye!")
			exit(1)