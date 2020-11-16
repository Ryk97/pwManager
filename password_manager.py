
from secret import get_secret_key
from menu import PWManagerMenu
import sys
# menu
# 1. create new password for a site
# 2. find password for a site
# 3. Find all sites connected to an email

secret = get_secret_key()

passw = input('Please prTestovide the master password to start using kallemanager3000: ')

if passw == secret:
    print('You\'re in')

else:
    print('no luck')
    sys.exit(1) 
menu = PWManagerMenu()
choice = menu.menu()
while choice != 'Q':
    if choice == '1':
        menu.create()
    if choice == '2':
        menu.find_accounts()
    if choice == '3':
        menu.find()
    else:
        choice = menu.menu()
exit()
