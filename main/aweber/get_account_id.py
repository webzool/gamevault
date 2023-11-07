import requests

headers = {'Accept': 'application/json',
           'User-Agent': 'AWeber-Python-code-sample/1.0',
           'Authorization': f'Bearer qG8ZtZpOimVVITsiv6rUY9BJUrbNxr0O'}
url = 'https://api.aweber.com/1.0/accounts'
response = requests.get(url, headers=headers)
print(response.json())