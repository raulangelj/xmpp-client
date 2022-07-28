import time
from menus_texts import *
from config import *
from getpass import getpass

def get_principal_menu_option():
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
	jid = input('JID: ')
	password = getpass('Password: ')
	return jid, password