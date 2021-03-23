from venmo_api import Client
import os
import datetime
import pandas as pd
# Get your access token. You will need to complete the 2FA process
access_token = Client.get_access_token(username=os.environ['indeed-email'],
                                       password=os.environ['indeed-pass'])

venmo = Client(access_token=access_token)
venmo.user.get_my_profile()
# friends = venmo.user.get_user_friends_list(user_id='2526605075283968007')
transactions = venmo.user.get_user_transactions(user_id='2526605075283968007')

jordan = 'Jordan-Adams907'
data = []
for item in transactions:
    datum = {}
    if item.target.username == jordan or item.actor.username == jordan:
        datum['epoch'] = item.date_completed
        datum['date_completed'] = datetime.datetime.fromtimestamp(item.date_completed)
        datum['amount'] = item.amount
        datum['note'] = item.note
        data.append(datum)
data.sort(key=lambda x: x['date_completed'], reverse=True)
pd.DataFrame(data).to_csv('jordans-payments.csv', index=False)

last_payment = datetime.datetime.fromtimestamp(data[0]['epoch'])
delta_from_last_payment = datetime.datetime.now() - last_payment
print(f'{delta_from_last_payment.seconds/3600/24} days since last payment')

if delta_from_last_payment.seconds/3600/24 > 30:
    now = datetime.datetime.now()
    note = f'{now.year}-{now.month}-{now.day} phone payment'
    venmo.payment.send_money(80.00, note, '1994505100197888035')