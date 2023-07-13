#  core/__init__.py
#    automatically generated file

def create_user(permissions=1):
  ''' Creates a user account on this machine for this application via the CLI '''
  from getpass import getpass
  from core.models import Users
  from core.library import console

  console.out("\n> CREATE NEW USER\n")
  password = ""
  password_confirmation = ""

  def get_password_inputs():
    password = getpass("  Enter Password: ")
    password_confirmation = getpass("  Confirm Password: ")
    return password, password_confirmation

  email = input("  Enter Email: ")
  password, password_confirmation = get_password_inputs()

  while password != password_confirmation:
    print("Sorry! the password entries didn't match. Try again.\n")
    password, password_confirmation = get_password_inputs()

  first_name = input("  Enter First Name: ")
  last_name = input("  Enter Last Name: ")
  date_of_birth = input("  Enter Date of Birth (DD/MM/YYYY): ")

  return Users.create(
    email=email,
    password=password,
    first_name=first_name,
    last_name=last_name,
    date_of_birth=date_of_birth,
    permissions=permissions
  )
