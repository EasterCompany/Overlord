#! /usr/bin/python3

# Standard library
from sys import argv
from os import environ
# Overlord library
from core.tools import tools
from core.library import get_wsgi_application

if __name__ == '__main__':
  environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
  application = get_wsgi_application()

  if len(argv) >= 1 and argv[1] == 'createsuperuser':
    # Create an Overlord Admin User
    from core.models import Users
    print("\n --- CREATE NEW ADMIN USER --- \n")
    admin_email = input("Enter Email: ")
    admin_password = input("Enter Password: ")
    admin_password_confirmation = input("Confirm Password: ")
    if admin_password != admin_password_confirmation:
      print("Sorry! the password entries didn't match. Try again.\n")
    else:
      Users.create(admin_email, admin_password, 99)

  elif len(argv) >= 1 and argv[1] == 'createuser':
    # Create an Overlord App User
    from core.models import Users
    print("\n --- CREATE NEW USER --- \n")
    user_email = input("Enter Email: ")
    user_password = input("Enter Password: ")
    user_password_confirmation = input("Confirm Password: ")
    if user_password != user_password_confirmation:
      print("Sorry! the password entries didn't match. Try again.\n")
    else:
      Users.create(user_email, user_password, 1)

  elif len(argv) > 1 and argv[1] == 'tools':
    # Overlord Command Line Interface Tools
    tools.run()

  else:
    # Default Django Command Line Interface Tools
    from core.library import execute_from_command_line
    execute_from_command_line(argv)
