import time
from menus_texts import *
from config import *
from aioconsole import ainput
from aioconsole.stream import aprint
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

async def get_login_menu_option():
	"""
	Get the option from the login menu
	"""
	valid_option = False
	while not valid_option:
		await aprint(login_menu)
		try:
			option = int(await ainput('What do you want to do?\n> '))
			if option < 1 or option > 7:
				await aprint('Choose a valid option')
				time.sleep(WAIT)
			else:
				valid_option = True
		except Exception:
			await aprint('Choose a valid option')
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
		status = 'chat'
	else:
		print(status_menu)
		status = input('What status do you want to set?\n> ')
		if status == '1':
			status = 'chat'
		elif status == '2':
			status = 'away'
		elif status == '3':
			status = 'xa'
		else:
			status = 'dnd'
	print('Write down your status message: ')
	status_message = input('> ')
	return status, status_message
