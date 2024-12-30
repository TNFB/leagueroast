import discord
from discord.ext import tasks
import os
from dotenv import load_dotenv
import manager
import riot_module

load_dotenv() 

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
            
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('register'):
        riot_id = message.content[9:]
        manager.add_player(riot_id)
        embed = discord.Embed(title="Registration", description="Saved!", color=0x00ff00)
        await message.channel.send(embed=embed)
    
    if message.content.startswith('unregister'):
        riot_id = message.content[11:]
        manager.remove_player(riot_id)
        embed = discord.Embed(title="Unregistration", description="Removed!", color=0xff0000)
        await message.channel.send(embed=embed)

    if message.content.startswith('list'):
        embed = discord.Embed(title="List of players", color=0x00ff00)
        for player in manager.playerList:
            embed.add_field(name=player["gameName"], value=player["tagLine"], inline=True)
        await message.channel.send(embed=embed)

    if message.content.startswith('stats'):
        for player in manager.playerList:
            result = riot_module.get_stats(player["gameName"], player["tagLine"])
            k = result[0]
            d = result[1]
            a = result[2]
            embed = discord.Embed(title=f"Stats for {player['gameName']}#{player['tagLine']}", color=0x00ff00)
            embed.add_field(name="Kills", value=str(k), inline=True)
            embed.add_field(name="Deaths", value=str(d), inline=True)
            embed.add_field(name="Assists", value=str(a), inline=True)
            await message.channel.send(embed=embed)

# @tasks.loop(seconds=10)
# async def back_task() :
#   channel = client.get_channel(os.getenv("DISCORD_CHANNEL"))
#   if liste_joueurs != [] :
#     for joueur in liste_joueurs :
#         result = data_summoner(joueur)
#         k = result[0]
#         d = result[1]
#         a = result[2]
#         #if d-k > k*2 :
#         if True :      
#             await channel.send("Nom du joueur : "+str(joueur))
#             await channel.send("Kills : " + str(k))
#             await channel.send("Deaths : " + str(d))
#             await channel.send("Assists : " + str(a))

# @client.event
# async def on_ready():
#   await back_task.start()

def start_bot():
  client.run(os.getenv("DISCORD_TOKEN"))