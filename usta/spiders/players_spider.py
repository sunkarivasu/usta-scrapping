import scrapy
import json
from ..items import UstaMatchItem


class PlayersSpiderSpider(scrapy.Spider):
    name = 'players_spider'
    # allowed_domains = ['playtennis.usta.com']
    start_urls = ['https://playtennis.usta.com/Competitions/virginiabeachtennisandcountryclub/Tournaments/draws/C543129D-6B38-41E2-BA31-415991EBFFE6']

    def parse(self, response):
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


        yield scrapy.Request("https://prd-usta-kube-tournamentdesk-public-api.clubspark.pro/",method="POST",headers=headers,body=json.dumps(json_data),callback=self.yieldEachMatchAsSeperateRecord)


    def yieldEachMatchAsSeperateRecord(self,response):
        matchItem = UstaMatchItem()
        res = json.loads(response.text)
        matches = res["data"]["tournamentMatchUps"]["completedMatchUps"]
        for match in matches:
            eventName = match["eventName"]
            abbreviatedRoundName = match["abbreviatedRoundName"]
            if abbreviatedRoundName not in ["R32","R16","QF","SF","F"]:
                continue
            winningSide = match["winningSide"]
            isDoubles = match["sides"][winningSide - 1]["participant"]["participantType"] == "PAIR"

            if isDoubles == False:
                winner1 = match["sides"][winningSide - 1]["participant"]["participantName"]
                loser1 = match["sides"][winningSide % 2]["participant"]["participantName"]
                winner2 = None
                loser2 = None
            else:
                winner1 = match["sides"][winningSide - 1]["participant"]["individualParticipants"][0]["participantName"]
                loser1 = match["sides"][winningSide % 2]["participant"]["individualParticipants"][0]["participantName"]
                winner2 = match["sides"][winningSide - 1]["participant"]["individualParticipants"][1]["participantName"]
                loser2 = match["sides"][winningSide % 2]["participant"]["individualParticipants"][1]["participantName"]

            matchItem["eventName"] = eventName
            matchItem["roundName"] = abbreviatedRoundName
            matchItem["winner1"] = winner1
            matchItem["winner2"] = winner2
            matchItem["loser1"] = loser1
            matchItem["loser2"] = loser2

            yield matchItem









    def fetchWholeDataInProperFormat(self,response):
        print("fetching ...")
        # print(json.loads(response.text))
        res = json.loads(response.text)
        matches = res["data"]["tournamentMatchUps"]["completedMatchUps"]

        resultFormat = {
            "eventName":{"r16":[{"winner1":"","winner2":"","loser1":"","loser2":""}],
                         "quaterFinals":[{"winner1":"","winner2":"","loser1":"","loser2":""}],
                         "semiFinals":[{"winner1":"","winner2":"","loser1":"","loser2":""}],
                         "finals":[{"winner1":"","winner2":"","loser1":"","loser2":""}]},
            "eventName": {"r16": [{"winner1": "", "winner2": "", "loser1": "", "loser2": ""}],
                          "quaterFinals": [{"winner1": "", "winner2": "", "loser1": "", "loser2": ""}],
                          "semiFinals": [{"winner1": "", "winner2": "", "loser1": "", "loser2": ""}],
                          "finals": [{"winner1": "", "winner2": "", "loser1": "", "loser2": ""}]},
        }

        result = {}
        for match in matches:
            eventName = match["eventName"]
            winningSide = match["winningSide"]
            isDoubles = match["sides"][winningSide - 1]["participant"]["participantType"] == "PAIR"

            if isDoubles == False:
                winner1 = match["sides"][winningSide - 1]["participant"]["participantName"]
                loser1 = match["sides"][winningSide % 2]["participant"]["participantName"]
                winner2 = None
                loser2 = None
            else:
                winner1 = match["sides"][winningSide - 1]["participant"]["individualParticipants"][0]["participantName"]
                loser1 = match["sides"][winningSide % 2]["participant"]["individualParticipants"][0]["participantName"]
                winner2 = match["sides"][winningSide - 1]["participant"]["individualParticipants"][1]["participantName"]
                loser2 = match["sides"][winningSide % 2]["participant"]["individualParticipants"][1]["participantName"]

            if eventName not in result:
                result[eventName] = {}
            else:
                pass
            abbreviatedRoundName = match["abbreviatedRoundName"]
            if abbreviatedRoundName not in result[eventName]:
                result[eventName][abbreviatedRoundName] = [{"winner1":winner1,
                                                                "winner2":winner2,
                                                                "loser1":loser1,
                                                                "loser2":loser2}]
            else:
                result[eventName][abbreviatedRoundName].append({"winner1":winner1,
                                                                "winner2":winner2,
                                                                "loser1":loser1,
                                                                "loser2":loser2})
        yield result

