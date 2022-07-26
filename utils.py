import time
from menus_texts import *
from config import *

def get_principal_menu_option():
	valid_option = False
	while not valid_option:
		print(main_menu)
		try:
			option = int(input('What do you want to do?\n> '))
			if option < 1 or option > 3:
				print('Choose a valid option')
				time.sleep(WAIT)
			else:
				valid_option = True
		except Exception:
			print('Choose a valid option')
			time.sleep(WAIT)
	return option