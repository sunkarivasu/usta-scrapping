import requests
import json

headers = {
    'authority': 'prd-usta-kube-tournamentdesk-public-api.clubspark.pro',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://playtennis.usta.com',
    'referer': 'https://playtennis.usta.com/',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}

json_data = {
    'operationName': 'TournamentMatchUps',
    'variables': {
        'tournamentId': 'C543129D-6B38-41E2-BA31-415991EBFFE6',
    },
    'query': 'query TournamentMatchUps($tournamentId: ID!) {\n  tournamentMatchUps(tournamentId: $tournamentId)\n}\n',
}

response = requests.post('https://prd-usta-kube-tournamentdesk-public-api.clubspark.pro/', headers=headers, json=json_data)
print(json.loads(response.text))
