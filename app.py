from flask import Flask
from flask import render_template, redirect
import requests
app = Flask(__name__)

links = {
    "BR1": "br1.api.riotgames.com",
    "EUN1": "eun1.api.riotgames.com"
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

@app.route("/<country>/<name>/<type>")
def index(country, name, type):
    data = define_map(get(country, name))
    return render_template('template.html', data = data[type])


def get(country, name):
    headers = {'X-Riot-Token': 'RGAPI-68de7c3b-780b-4b87-b1de-2eafe71442d5'}
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
    print(lista)
    return lista

if __name__ == '__main__':
    app.run(port=5000, debug=True)