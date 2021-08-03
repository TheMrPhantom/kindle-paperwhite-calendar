from exchangelib import Account, Credentials, DELEGATE
import utilities
import config
import operator

print("Starting authentication...")
failed=True
while failed:
        try:
                creds = Credentials(username=config.email,password=config.pw)
                account = Account(
                        primary_smtp_address=config.email,
                        credentials=creds,
                        autodiscover=True,
                        access_type=DELEGATE)
                failed=False
        except:
                print("Authentication failed! Retrying...")
print("Authenticated!")

cal=utilities.Calendar_Manager(account)

#cal.get_Appointments()
#print("Getting appointments...")

def get_Appointments():
        appointments=cal.get_Appointments()
        appointments.sort(key=operator.attrgetter('start'))
        return appointments