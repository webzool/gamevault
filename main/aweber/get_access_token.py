from __future__ import print_function
import getpass
import json
import os

from requests_oauthlib import OAuth2Session

OAUTH_URL = 'https://auth.aweber.com/oauth2/{}'

client_id = input('Enter your client id: ')
client_secret = getpass.getpass('Enter your client secret: ')

redirect_uri = 'https://localhost:9000/aweber'

scope = [
    'account.read', 'list.read', 'list.write', 'subscriber.read',
    'subscriber.write', 'email.read', 'email.write',
    'subscriber.read-extended', 'landing-page.read'
]
oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
authorization_url, state = oauth.authorization_url(
    OAUTH_URL.format('authorize'))

print('Go to this URL: ' + authorization_url)
authorization_response = input('Log in and paste the returned URL here: ')

token = oauth.fetch_token(OAUTH_URL.format('token'),
                          authorization_response=authorization_response,
                          client_secret=client_secret)

p = "main/aweber/credentials.json"
with open(p, 'wt') as creds_file:
    json.dump(
        {
            'client_id': client_id,
            'client_secret': client_secret,
            'token': token
        }, creds_file)
os.chmod('main/aweber/credentials.json', 0o600)
print('Updated credentials.json with your new credentials')