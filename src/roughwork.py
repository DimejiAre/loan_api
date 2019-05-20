import math

from datetime import datetime
from datetime import timedelta

from src.common.database import Database
from src.models.loanees import Loanee

Database.initialize()

# print(datetime.now() + timedelta(days=2))
y = datetime.now()
x = datetime(2019, 3, 25)
z = datetime(2018, 1, 15)
x -= timedelta(days=2)
print(x)
print(x.strftime("%x"))
print(y)
print((x - y).days)

print("......")


def _amount_due(date_due, date_collected, amount_collected):
    days = int((date_due - date_collected).days)
    print("money was borrowed for {} days".format(days))
    interest = amount_collected * (math.floor(days / 30) * 0.05)
    print(amount_collected + interest)


# _amount_due(date_due=x,date_collected=y,amount_collected=200)


# newLoanee = Loanee(name="Fehintola",phone_number="08052517453",email_address="lawalaref@gmail.com")
#
# newLoanee.save_to_mongo()

# Loanee.delete_loanee(id="d467bbc9-6e97-440e-8f5c-24b7a31bc10b")



zz = datetime.strptime("02/02/2018", "%d/%m/%Y")
print("{} {}".format(zz, type(zz)))


print(datetime.now())
print(datetime.now().date())


import smtplib

sender = "olardi2@gmail.com"
recipient = "dimejiare@yahoo.com"
password = "Cod3br4k3r!" # Your SMTP password for Gmail
subject = "Test email from Python"
text = "Hello from Python"

smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
smtp_server.login(sender, password)
message = "Subject: {}\n\n{}".format(subject, text)
smtp_server.sendmail(sender, recipient, message)
smtp_server.close()