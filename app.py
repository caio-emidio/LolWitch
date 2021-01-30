from flask import Flask
from flask import render_template, redirect, request
import requests
from decouple import config
app = Flask(__name__)

links = {
    "BR1": "br1.api.riotgames.com",
    "EUN1": "eun1.api.riotgames.com",
    "EUW1": "euw1.api.riotgames.com",
    "JP1": "jp1.api.riotgames.com",
    "KR": "kr.api.riotgames.com",
    "LA1": "la1.api.riotgames.com",
    "LA2": "la2.api.riotgames.com",
    "NA1": "na1.api.riotgames.com",
    "OC1": "oc1.api.riotgames.com",
    "TR1": "tr1.api.riotgames.com",
    "RU": "ru.api.riotgames.com",
}

images = {
    "SILVER": "Emblem_Silver.png",
    "PLATINUM": "Emblem_Platinum.png",
    "MASTER": "Emblem_Master.png",
    "IRON": "Emblem_Iron.png",
    "GRANDMASTER": "Emblem_Grandmaster.png",
    "GOLD": "Emblem_Gold.png",
    "DIAMOND": "Emblem_Diamond.png",
    "CHALLENGER": "Emblem_Challenger.png",
    "BRONZE": "Emblem_Bronze.png",
    "UNRANKED": "Emblem_Unranked.png",
}

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/rankedwitch/")
def showData():
    region = request.args.get('region')
    name = request.args.get('summoner')
    queue = request.args.get('queue')
    color = request.args.get('color')
    data = define_map(get(region, name), queue)
    return render_template('template.html', data = data[queue], color = color)


def requestLink(url):
    token = config('TOKEN')
    headers = {'X-Riot-Token': token}
    try:
        return requests.get(url, headers=headers).json()
    except ValueError:
        return "No name recognized"
def get(country, name):
    url = f"https://{links[country]}/lol/summoner/v4/summoners/by-name/{name}"
    response = requestLink(url)
    id = response["id"]
    url = f"https://{links[country]}/lol/league/v4/entries/by-summoner/{id}"
    response = requestLink(url)
    return response

def define_map(response, queue):
    lista = {}
    if(len(response) > 0):
        for res in response:
            map = {
                    "tier": images[res["tier"]],
                    "rank": res["rank"],
                    "leaguePoints": res["leaguePoints"],
                    "percentWin": float(res["wins"] / res["wins"] + res["losses"]),
                    "wins": res["wins"],
                    "loses": res["losses"]
                    
                }
            lista[res["queueType"]] = map
    if queue not in lista:
        map = {
            "tier": images["UNRANKED"],
            "rank": "Unranked",
            "leaguePoints": 0,
            "percentWin": 0,
            "wins": 0,
            "loses": 0       
        }
        lista[queue] = map

    return lista

if __name__ == '__main__':
    DEBUG = config('DEBUG', default=False, cast=bool)
    app.run(port=5000, debug=DEBUG)