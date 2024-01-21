from O365 import Account

client_id = 'f38a489d-d4a0-4ae8-ad0f-0bf78d43ab34'  # Your client_id
client_secret = '79q8Q~Lgyc3T~fcujHIp-ovB3U4OvxE7TQW85bHP'  # Your client_secret, create an (id, secret)
tenant_id1 = 'f8cdef31-a31e-4b4a-93e4-5f571e91255a'
print("Connecting to O365")
account = Account(credentials=(client_id, client_secret)) 
if account.authenticate(scopes=['basic', 'MailboxSettings.ReadWrite','Mail.ReadWrite', 'Mail.Send','offline_access']):
   print('Authenticated!')
mailbox = account.mailbox()
inbox = mailbox.inbox_folder()
message = mailbox.new_message()
message.to.add(['vcharan@purdue.edu', 'abestrap@gmail.com'])
message.body = 'It Works!!!'
message.send()
