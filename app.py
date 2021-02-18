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
    "IRON_I": "imgs/Emblem_Iron_I.png",
    "IRON_II": "imgs/Emblem_Iron_II.png",
    "IRON_III": "imgs/Emblem_Iron_III.png",
    "IRON_IV": "imgs/Emblem_Iron_IV.png",
    "BRONZE_I": "imgs/Emblem_Bronze_I.png",
    "BRONZE_II": "imgs/Emblem_Bronze_II.png",
    "BRONZE_III": "imgs/Emblem_Bronze_III.png",
    "BRONZE_IV": "imgs/Emblem_Bronze_IV.png",
    "SILVER_I": "imgs/Emblem_Silver_I.png",
    "SILVER_II": "imgs/Emblem_Silver_II.png",
    "SILVER_III": "imgs/Emblem_Silver_III.png",
    "SILVER_IV": "imgs/Emblem_Silver_IV.png",
    "GOLD_I": "imgs/Emblem_Gold_I.png",
    "GOLD_II": "imgs/Emblem_Gold_II.png",
    "GOLD_III": "imgs/Emblem_Gold_III.png",
    "GOLD_IV": "imgs/Emblem_Gold_IV.png",
    "DIAMOND_I": "imgs/Emblem_Diamond_I.png",
    "DIAMOND_II": "imgs/Emblem_Diamond_II.png",
    "DIAMOND_III": "imgs/Emblem_Diamond_III.png",
    "DIAMOND_IV": "imgs/Emblem_Diamond_IV.png",
    "PLATINUM_I": "imgs/Emblem_Platinum_I.png",
    "PLATINUM_II": "imgs/Emblem_Platinum_II.png",
    "PLATINUM_III": "imgs/Emblem_Platinum_III.png",
    "PLATINUM_IV": "imgs/Emblem_Platinum_IV.png",
    "MASTER_I": "imgs/Emblem_Master_I.png",
    "MASTER_II": "imgs/Emblem_Master_II.png",
    "MASTER_III": "imgs/Emblem_Master_III.png",
    "MASTER_IV": "imgs/Emblem_Master_IV.png",
    "GRANDMASTER_I": "imgs/Emblem_Grandmaster_I.png",
    "GRANDMASTER_II": "imgs/Emblem_Grandmaster_II.png",
    "GRANDMASTER_III": "imgs/Emblem_Grandmaster_III.png",
    "GRANDMASTER_IV": "imgs/Emblem_Grandmaster_IV.png",
    "CHALLENGER_I": "imgs/Emblem_Challenger_I.png",
    "CHALLENGER_II": "imgs/Emblem_Challenger_II.png",
    "CHALLENGER_III": "imgs/Emblem_Challenger_III.png",
    "CHALLENGER_IV": "imgs/Emblem_Challenger_IV.png",
    "UNRANKED": "imgs/Emblem_Unranked.png",
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
    hasBg = request.args.get('hasBg')
    if(queue == 'RANKED_TFT'):
        data = define_map(getTFT(region, name), queue)
    else:
        data = define_map(get(region, name), queue)
    return render_template('template.html', data = data[queue], color = color, hasBg = hasBg)


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

def getTFT(country, name):
    url = f"https://{links[country]}/lol/summoner/v4/summoners/by-name/{name}"
    response = requestLink(url)
    id = response["id"]
    url = f"https://{links[country]}/tft/league/v1/entries/by-summoner/{id}"
    response = requestLink(url)
    return response

def define_map(response, queue):
    lista = {}
    if(len(response) > 0):
        print(response)
        for res in response:
            map = {
                    "tier": images[res["tier"] + "_" + res["rank"]],
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