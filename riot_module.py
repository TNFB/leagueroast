# Fonction pour obtenir l'ID du joueur en fonction de son nom d'invocateur
import json
import requests
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv() 

api_key = os.getenv("RIOT_API_KEY")

def get_summoner_puuid(gameName, tagLine):
    url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
    response = requests.get(url, headers={"X-Riot-Token": api_key})
    
    if response.status_code == 200:
        summoner_data = response.json()
        return summoner_data["puuid"]
    else:
        print("Echec de la recuperation des informations du joueur : "+str(response.status_code))
        return None

# Fonction pour obtenir le dernier match du joueur
def get_last_match(summoner_puuid):
    url = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/"+summoner_puuid+"/ids"
    response = requests.get(url, headers={"X-Riot-Token": api_key})

    if response.status_code == 200:
        matchlist_data = response.json()
        latest_match = matchlist_data[0]
        return latest_match
    else:
        print("Echec de la recuperation de la liste des matchs du joueur "+str(response.status_code))
        return None

# Fonction pour obtenir les details du dernier match
def get_match_details_for_puuid(match_id, summoner_puuid):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}"
    response = requests.get(url, headers={"X-Riot-Token": api_key})
    
    if response.status_code == 200:
        match_data = json.dumps(response.json())
        match_details = json.loads(match_data)
        joueur = 0
        for participant in match_details["metadata"]["participants"] :
            if participant == summoner_puuid :
                break
            else :
                joueur += 1
        # Imprimer la valeur des colonnes "deaths", "kills" et "assists" du joueur
        k = match_details["info"]["participants"][joueur]["kills"]
        d = match_details["info"]["participants"][joueur]["deaths"]
        a = match_details["info"]["participants"][joueur]["assists"]
        return [k,d,a]
    else:
        print("Echec de la recuperation des details du match : "+str(response.status_code))
        return None
    
def get_stats(gameName, tagLine):
    puuid = get_summoner_puuid(gameName, tagLine)
    last_match = get_last_match(puuid)
    match_details = get_match_details_for_puuid(last_match, puuid)
    return match_details