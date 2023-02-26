import urllib.parse

import requests

query = {
    'grant_type': 'authorization_code',
    'code': 1123775,
    'client_id': 'abc194a9dd6d438183ad07e58a11fb9f',
    'client_secret': 'f3ba31d928d949d081f78227415dfa95',
    'scope': 'openid login:email login:info'
}

query = urllib.parse.urlencode(query)
#print(query)

# Формирование заголовков POST-запроса
header = {
    'Content-Type': 'application/x-www-form-urlencoded'
}
#
# Выполнение POST-запроса и вывод результата
#req = requests.post(url='https://oauth.yandex.ru/token',
#                    headers=header, data=query)
#print(req.json())
#token = req.json()['refresh_token']
#print(token)
query_2 = {
    'grant_type': 'refresh_token',
    'refresh_token': '1s:8EQb1mZNm1uJ0gdp:x7skf0nVDuwetQe_t4Ph0yxbbrNQvs7R38kxu0yWzKf4YaeL1xSYJB93tiWizW-eLrdnfNT090Y3-g:SK9tnV9f0V85-pWY7RRVdg',
    'client_id': 'abc194a9dd6d438183ad07e58a11fb9f',
    'client_secret': 'f3ba31d928d949d081f78227415dfa95'
}

print(requests.post('https://oauth.yandex.ru/token', headers=header, data=query_2).json())
header = {
    'Authorization': f'OAuth {token}'
}
req_2 = requests.post(url='https://login.yandex.ru/info', headers=header)
#print(req_2.status_code)


debug_uri = 'https://oauth.yandex.ru/authorize?response_type=token&client_id=abc194a9dd6d438183ad07e58a11fb9f'
print(requests.get(debug_uri).status_code)

