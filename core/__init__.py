
def create_super_user():
  '''
  Create an admin user account on the local database for this application
  requires the minimal amount of admin data: email, password & permissions
  '''
  from core.models import Users
  print("\n --- CREATE NEW ADMIN USER --- \n")
  admin_email = input("Enter Email: ")
  admin_password = input("Enter Password: ")
  admin_password_confirmation = input("Confirm Password: ")
  if admin_password != admin_password_confirmation:
    print("Sorry! the password entries didn't match. Try again.\n")
  else:
    Users.create(admin_email, admin_password, 99)


def create_user():
  '''
  Create a basic user account on the local database for this application
  requires the minimal amount of user data: email & password
  '''
  from core.models import Users
  print("\n --- CREATE NEW USER --- \n")
  user_email = input("Enter Email: ")
  user_password = input("Enter Password: ")
  user_password_confirmation = input("Confirm Password: ")
  if user_password != user_password_confirmation:
    print("Sorry! the password entries didn't match. Try again.\n")
  else:
    Users.create(user_email, user_password, 1)
