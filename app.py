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
    data = define_map(get(region, name))
    return render_template('template.html', data = data[queue], color = color)


def get(country, name):
    token = config('TOKEN')
    headers = {'X-Riot-Token': token}
    url = f"https://{links[country]}/lol/summoner/v4/summoners/by-name/{name}"
    r = requests.get(url, headers=headers).json()
    id = r["id"]
    url = f"https://{links[country]}/lol/league/v4/entries/by-summoner/{id}"
    response = requests.get(url, headers=headers)
    return response.json()

def define_map(response):
    lista = {}
    for res in response:
        map = {
                "tier": images[res["tier"]],
                "rank": res["rank"],
                "leaguePoints": res["leaguePoints"],
                "percentWin": float(res["wins"] / res["wins"] + res["losses"])
            }
        lista[res["queueType"]] = map
    return lista

if __name__ == '__main__':
    app.run(port=5000, debug=True)