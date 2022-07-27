from http import client
import logging
import aiodns
import asyncio
from client import *
from getpass import getpass
from account import *
from utils import *
from menus_texts import *
from client import *

# ! DO NOT DELETE THIS LINE, PATCH A ERROR ON ASYNCIO LIB
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def start_chat():
  # Get the first option from the main menu
  option = get_principal_menu_option()

  # OPTION 1: Register
  if option == 1:
    jid = input("JID: ")
    password = getpass("Password: ")
    account = Client(jid, password, create_account=True)
    account.connect(disable_starttls=True)
    account.process(forever=False)
    # if not sign_in(jid, password):
    #   print("Error signing in, please try again")
    # else:
    #   print("Signed in successfully")
    #   # TODO - ask if user want to log in and add login logic
  # OPTION 2: Login
  elif option == 2:
    pass
  # OPTION 3: Exit login
  elif option == 3:
    print("Goodbye!")
    exit(1)

logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')
start_chat()