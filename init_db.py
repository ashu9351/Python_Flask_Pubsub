import sqlite3
import requests


connection = sqlite3.connect('pubsub.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()
authurl = 'https://login.salesforce.com/services/oauth2/token'
payload={
    'grant_type': 'password',
    'client_id': '3MVG9ZL0ppGP5UrAP59A8.dNkSsWx54hRgtkftFHZh1bxEMSGF6kwnRNA8VheLBe2RHROd01KucH2QHHt5ggh',
    'client_secret': '22883FEE07FDBA0FD71F317F8A4821155253D7853C280B4302EA229A30B1DDEF',
    'username': 'ashutoshexams@gmail.com',
    'password': 'ashutosh9351aozWQvXaav1CPDQaHHgtU7pQy',
    'organizationId': '00D28000000dVa8EAE'
}
'''payload = {
    'grant_type': 'password',
    'client_id': clientId,
    'client_secret': clientSecret,
    'username': username,
    'password': password,
}'''
res = requests.post(authurl, 
    headers={"Content-Type":"application/x-www-form-urlencoded"},
    data=payload)
token = ''
url= ''
if res.status_code == 200:
    response = res.json()

    access_token = response['access_token']
    instance_url = response['instance_url']
    access_token = access_token.encode(encoding="ascii",errors="ignore").decode('utf-8')
    instance_url = instance_url.encode(encoding="ascii",errors="ignore").decode('utf-8')
    print(access_token)
    print(instance_url)
    print('>>>>>>>AUTH Ends>>>>>>>>')

    cur.execute("INSERT INTO Auth (auth_token, instance_url) VALUES (?, ?)",
            (access_token, instance_url)
            )

    cur.execute("INSERT INTO Customers (name, email) VALUES (?, ?)",
            ('ABC Corp', 'test@abc.com')
            )

    cur.execute("INSERT INTO Customers (name, email) VALUES (?, ?)",
            ('Alex Inc.', 'testalex@inc.com')
            )

connection.commit()
connection.close()