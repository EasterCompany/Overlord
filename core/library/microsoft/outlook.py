from O365 import Account
from web.settings import SECRET_DATA

credentials = (SECRET_DATA['EMAIL_USER'], SECRET_DATA['EMAIL_PASS'])

account = Account(credentials)
m = account.new_message()
m.to.add('oweneaster@outlook.com')
m.subject = 'Test'
m.body = "hello world!"
m.send()
