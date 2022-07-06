import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from sqlalchemy import create_engine
import pandas as pd
import email, smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import numpy as np
import json


###Method for sending weekly email expiration updates along with a cronjob to activate

with open('/etc/config.json') as config_file:
     config = json.load(config_file)

site = config['SQLALCHEMY_DATABASE_URI']
engine = create_engine(site)
df_food = pd.read_sql('foods_foods', engine, index_col=False)
df_food['expiration'] = pd.to_datetime(df_food['expiration'], format ='%Y-%m-%d')
df_food['Days_Left'] = df_food['expiration'] - pd.to_datetime('today').normalize()
df_food['Days_Left'] = pd.to_numeric(df_food['Days_Left'].dt.days, downcast='integer')
df_food['expiration'] = df_food['expiration'].dt.strftime('%m/%d/%Y')
df_food['updated'] = pd.to_datetime(df_food.updated)
df_food['updated'] = df_food['updated'].dt.strftime('%m/%d/%Y')
df_food.rename(columns={'barcode': 'Barcode',
                        'product_name': 'Product Name',
                        'category': 'Category',
                        'sub_category': 'Sub Category',
                        'location': 'Location',
                        'quantity': 'Quantity',
                        'expiration': 'Expires On',
                        'updated': 'Updated On',
                        'Days_Left': 'Days Left'}, inplace=True)
df_user_prof = pd.read_sql('users_profile', engine)
df_user = pd.read_sql('auth_user', engine)
df_user =df_user[['id','email']]
df_user_prof =df_user_prof[['id','user_id', 'weekly_email_updates']]
selected_users_df =df_user_prof.loc[df_user_prof['weekly_email_updates']==1]
selected_users_df_final = df_user.loc[df_user['id']==df_user_prof['user_id']]
print(df_user)
print(selected_users_df)
users_dict =selected_users_df_final.set_index('id').to_dict()
users_list = selected_users_df['user_id'].tolist()
print(users_list)
print(users_dict)
user_email_list = []
for user in users_list:
    for k1, v1 in users_dict.items():
        for k2,v2 in v1.items():
            if user == k2:
                user_email_list.append(v2)

print(df_food)
email_dictionary = dict(zip(users_list, user_email_list))


sender_email = config['MAIL_USERNAME']
password = config['MAIL_PASSWORD']

message = MIMEMultipart("alternative")
message["Subject"] = "Food Inventory Update"
message["From"] = sender_email


context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    for key, value in email_dictionary.items():
        df = df_food.loc[df_food['author_id']==key]
        df = df.drop(['id', 'author_id'], axis=1)
        df = df.sort_values(by=['Days Left'])
        df = df.head(10)
        text = """\
Food Inventory Update"""
        html = '''
        This is your personalized weekly food inventory update. If you wish to disable this 
        feature you may do so in the user profile section of https://www.foodinventory.app
        '''
        html += df.to_html(classes='data')
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)
        receiver_email = value
        message["To"] = receiver_email
        server.sendmail(sender_email, receiver_email, message.as_string())


