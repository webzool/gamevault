import requests, os
from .models import ZohoToken
import datetime
from django.utils import timezone
ZOHO_TOKEN_URL='https://accounts.zoho.com/oauth/v2/token'
ZOHO_REFRESH_TOKEN='1000.d80cb814b1508b683632912e648142cf.a6af5786b628e4e363c75e41311ab4ab'
ZOHO_CLIENT_ID='1000.MD01YYHJM75FG51XF774E1Y2JDM0WD'
ZOHO_CLIENT_SECRET='32db9a7ebd1939bc1096a8c12440acd1c9179b7c98'
ZOHO_CODE='1000.f4b9948ebdf02acd05a74cbf460886c9.bcffbedda07889822aeb072be6cd1b02'
CRM_URL='https://www.zohoapis.com/crm/v2'
REFRESH_URL = f'{ZOHO_TOKEN_URL}?refresh_token={ZOHO_REFRESH_TOKEN}&client_id={ZOHO_CLIENT_ID}&client_secret={ZOHO_CLIENT_SECRET}&code={ZOHO_CODE}&grant_type=refresh_token'


class ZohoClient:
    def __init__(self):
            pass

    @classmethod
    def refresh_token(cls):
        """Renew the token required to send request to Zoho.

        Returns:
            ZohoToken: Zoho token object that contains access token & expire date.
        """

        try:
            # Zohodan yeni tokeni almak için istek at
            print("zoho refresh url", REFRESH_URL)
            response = requests.post(REFRESH_URL)
            token = response.json()
            print("TOken", token)
            # Veri tabanından ilk objeyi getir (ayrı saklamamıza gerek yok)
            zoho_token = ZohoToken.objects.first()

            # Eğer veri tabanında kayıtlı değil ise yeni oluştur
            if not zoho_token:
                zoho_token = ZohoToken()

            zoho_token.token = token['access_token']

            # Token bitiş süresini alınan zamandan 5dk önceye ayarla
            zoho_token.expires_at = timezone.now(
            ) + datetime.timedelta(seconds=int(token['expires_in']) - 300)

            # Veri tabanına kayıt et
            zoho_token.save()
            print('Zoho token refreshed.')

            return zoho_token
        except Exception as e:
            print(f'Error on getting the Zoho token. {e}')
        return None

    @classmethod
    def get_token(cls):
        """Gets the token from database and if it doesn't exist or it is expired, renews.

        Returns:
            ZohoToken: Zoho token object that contains access token & expire date.
        """

        # Veri tabanından ilk objeyi getir
        token = ZohoToken.objects.first()

        # Bulunamazsa yenisini iste
        if not token:
            token = cls.refresh_token()

        # Zamanı geçmiş ise yenisini iste
        if timezone.now() >= token.expires_at:
            token = cls.refresh_token()

        return token

    @classmethod
    def request(cls, baseUrl: str, path: str, type: str, queryParams={}, body={}, raw=False):
        """Sends request to Zoho with given information.

        Args:
            baseUrl (str): Zoho Api URL.
            path (str): Special path or module name.
            type (str): POST | GET | PUT | DELETE .
            queryParams (dict, optional): Parameters after URL. Defaults to {}.
            body (dict, optional): Data you want to send. Defaults to {}.

        Returns:
            Dict: Response object.
        """

        token = cls.get_token()

        # BaseUrl/Path şeklinde olacak
        url = baseUrl
        if not baseUrl.endswith('/'):
            url += '/'
        url += path

        # Gerekli headerlar
        headers = {
            'Authorization': f'Zoho-oauthtoken {token.token}',
            'Access-Control-Allow-Origin': '*',

        }

        response = requests.request(url=url, method=type, headers=headers, params=queryParams,
                                    json=body)

        # Boş bilgi gelince hata verme boş getir.
        if raw:
            return response.content

        if response.text != '':
            data = response.json()
        else:
            data = {}

        return data


    def crmAddNew(cls, module: str, data=[], triggers_enabled=True):
            """Adds new document to module on Zoho CRM.
            Note: 'data' argument must be a List or Array.

            Args:
                module (str): Module name.
                data (list, optional): Data you want to add. Defaults to [].

            Returns:
                Dict: Response object.
            """
            triggers = []
            if triggers_enabled:
                triggers = ['approval', 'workflow', 'blueprint']
            result = cls.request(CRM_URL, module, 'POST', body={
                                'data': data, 'trigger': triggers})
            return result