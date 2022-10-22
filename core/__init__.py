
def create_super_user():
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


def create_user():
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
