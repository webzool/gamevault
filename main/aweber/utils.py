from main.models import AweberCredentials, AweberLog
from requests_oauthlib import OAuth2Session
from django.conf import settings


TOKEN_URL = "https://auth.aweber.com/oauth2/token"


def read_aweber_credentials_table():
    from main.models import AweberCredentials
    credential = AweberCredentials.objects.last()
    data = {
        'client_id': credential.client_id,
        'client_secret': credential.client_secret,
        'token': credential.token
        }
    return data


def token_updater(token):
    credentials = read_aweber_credentials_table()
    AweberCredentials.objects.create(
        client_id=credentials['client_id'],
        client_secret=credentials['client_secret'],
        token=token
        )
    AweberCredentials.objects.first().delete()

def session():
    credentials = read_aweber_credentials_table()
    extra = {
        'client_id': credentials['client_id'],
        'client_secret': credentials['client_secret'],
        'token': credentials['token'],
    }
    oauth_session = OAuth2Session(
        client_id=credentials['client_id'],
        token=credentials['token'],
        auto_refresh_url=TOKEN_URL,
        token_updater=token_updater,
        auto_refresh_kwargs=extra
    )
    return oauth_session



def add_subscriber(full_name, email, phone, tags):
    body = {
        'email': email,
        'custom_fields': {
            'Phone': phone,
        },
        'name': full_name,
        'tags': [tags],
        'strict_custom_fields': True,
    }

    url = settings.AWEBER_LIST_URL
    post_response = session().post(url, json=body)
    
    if str(post_response.status_code) != str(201):
        AweberLog.objects.create(
        email=email,
        log=post_response.json()
    )

