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