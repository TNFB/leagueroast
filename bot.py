# This example requires the 'message_content' intent.

import discord
import requests
import json
from discord.ext import tasks
import asyncio
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv() 

api_key = os.getenv("RIOT_API_KEY")


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

liste_joueurs = []

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# Fonction pour obtenir l'ID du joueur en fonction de son nom d'invocateur
def get_summoner_puuid(summoner_name):
    url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
    response = requests.get(url, headers={"X-Riot-Token": api_key})
    
    if response.status_code == 200:
        summoner_data = response.json()
        url2 = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/"+str(summoner_data["id"])
        response2 = requests.get(url, headers={"X-Riot-Token": api_key})
        return summoner_data["puuid"]
    else:
        print("Echec de la recuperation des informations du joueur"+str(response.status_code))
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
def get_match_details(match_id):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}"
    response = requests.get(url, headers={"X-Riot-Token": api_key})
    
    if response.status_code == 200:
        match_data = json.dumps(response.json())
        return match_data
    else:
        print("Echec de la recuperation des details du match "+str(response.status_code))
        return None

def data_summoner(summoner_name):
    # Obtenez l'ID du joueur
    summoner_puuid = get_summoner_puuid(summoner_name)

    if summoner_puuid:
        # Obtenez le dernier match du joueur
        latest_match = get_last_match(summoner_puuid)
        
        if latest_match:
            # Obtenez les details du dernier match
            match_details = get_match_details(latest_match)

            if match_details:
                match_details = json.loads(match_details)
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
            
            
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('stats'):
        summoner_name = message.content[6:]
        liste_joueurs.append(summoner_name)
        await message.channel.send("Saved !")
    

@tasks.loop(seconds=10)
async def back_task() :
  channel = client.get_channel(os.getenv("DISCORD_CHANNEL"))
  if liste_joueurs != [] :
    for joueur in liste_joueurs :
        result = data_summoner(joueur)
        k = result[0]
        d = result[1]
        a = result[2]
        #if d-k > k*2 :
        if True :      
            await channel.send("Nom du joueur : "+str(joueur))
            await channel.send("Kills : " + str(k))
            await channel.send("Deaths : " + str(d))
            await channel.send("Assists : " + str(a))
            await channel.send("AVHFIFUBZEOIFKNZNVOZENFZ GROSSE MERDE")

@client.event
async def on_ready():
  await back_task.start()
          
client.run(os.getenv("DISCORD_TOKEN"))