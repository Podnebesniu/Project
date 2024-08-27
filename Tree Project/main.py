import os
import art
import disnake
from art import text2art
from config import token
from disnake.ext import commands


intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, test_guilds=[1277507396939550771])

@bot.event
async def on_ready():
    print(text2art('Tree Project'))
    print(text2art('The bot is working'))
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_guild_join(guild):
    channel = disnake.utils.get(guild.text_channels, name='general')
    if channel:
        await channel.send(f"Привет, {guild.name}! 👋 Я рад присоединиться к вашему серверу.")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(token)