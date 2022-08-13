import time
from menus_texts import *
from config import *
from getpass import getpass

def get_principal_menu_option():
	"""
	Get the option from the principal menu
	"""
	valid_option = False
	while not valid_option:
		print(main_menu)
		try:
			option = int(input('What do you want to do?\n> '))
			if option < 1 or option > 4:
				print('Choose a valid option')
				time.sleep(WAIT)
			else:
				valid_option = True
		except Exception:
			print('Choose a valid option')
			time.sleep(WAIT)
	return option

def get_login_menu_option():
	"""
	Get the option from the login menu
	"""
	valid_option = False
	while not valid_option:
		print(login_menu)
		try:
			option = int(input('What do you want to do?\n> '))
			if option < 1 or option > 7:
				print('Choose a valid option')
				time.sleep(WAIT)
			else:
				valid_option = True
		except Exception:
			print('Choose a valid option')
			time.sleep(WAIT)
	return option

def get_jid_and_password():
	"""
	Get the jid (email) and password of the user
	"""
	jid = input('JID: ')
	password = getpass('Password: ')
	return jid, password

def get_chat_room_option():
	"""
	Get the option from the chat room menu
	"""
	valid_option = False
	while not valid_option:
		print(rooms_menu)
		try:
			option = int(input('What do you want to do?\n> '))
			if option < 1 or option > 4:
				print('Choose a valid option')
				time.sleep(WAIT)
			else:
				valid_option = True
		except Exception:
			print('Choose a valid option')
			time.sleep(WAIT)
	return option

def get_status():
	"""
	Get the status of the user
	"""
	status_message = ''
	status = ''
	print('Set as available? (y/n)? ')
	stat_opt = input('> ')
	if stat_opt.lower() in ['y', "yes"]:
		status = 'Available'
	else:
		print('Write your current status')
		status = input('> ')
	print('Write down your status message: ')
	status_message = input('> ')
	return status, status_message

# TODO pending not implemented
async def chat(client):
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