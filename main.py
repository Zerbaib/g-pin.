import disnake
from disnake.ext import commands
import json
import os
import platform
import requests

config_file_path = "config.json"
online_version = "https://raw.githubusercontent.com/Guillaume0001/g-pin./main/version.txt"

if not os.path.exists(config_file_path):
    with open(config_file_path, 'w') as config_file:
        token = input("Enter the bot's token: ")
        prefix = input("Enter the bot's prefix: ")
        log_id = input("Enter the log's channel ID: ")
        id_client = input("Enter your discord ID: ")
        config_data = {
            "TOKEN": token,
            "PREFIX": prefix,
            "LOG_ID": log_id,
            "OWNER_ID": id_client,
            "DEL_TIME": 3
        }
        json.dump(config_data, config_file, indent=4)
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)
else:
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)

token = config["TOKEN"]
prefix = config["PREFIX"]
log = config["LOG_ID"]
owner = config["OWNER_ID"]
time_del = config["DEL_TIME"]

bot = commands.Bot(
    command_prefix=prefix,
    intents=disnake.Intents.all(),
    case_insensitive=True
)

@bot.event
async def on_ready():
    if bot.user.discriminator == 0:
        nbot = bot.user.name
    else:
        nbot = bot.user.name + "#" + bot.user.discriminator

    response = requests.get(online_version)
    if response.status_code == 200:
        bot_repo_version = response.text.strip()
    else:
        bot_repo_version = "Unknown"
    with open('version.txt', 'r') as version_file:
        bot_version = version_file.read().strip()
    if bot_version != bot_repo_version:
        print('===============================================')
        print('🛑 ATTENTION')
        print('🛑 Je ne suis pas sur la dernière version !')
        print('🛑 Met moi à jour !')
        print('🛑 Utilise "git fetch && git pull" pour me mettre à jour.')
    print('===============================================')    
    print(f"🔱 Prêt pour parcourir ton serveur !")
    print(f'🔱 Je suis {nbot} | {bot.user.id}')
    print(f'🔱 Ma version local: {bot_version}')
    print(f'🔱 Ma version en ligne: {bot_repo_version}')
    print(f"🔱 Version de Disnake: {disnake.__version__}")
    print(f"🔱 Je fonctionne sur{platform.system()} {platform.release()} {os.name}")
    print(f"🔱 Version de python: {platform.python_version()}")
    print('===============================================')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        cog_name = filename[:-3]
        try:
            bot.load_extension(f'cogs.{cog_name}')
        except:
            print(f"🌪️  Erreur dans le chargement de l'extension '{cog_name}':\n\n{e}")

bot.run(token)