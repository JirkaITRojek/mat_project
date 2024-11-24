import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from textwrap import fill
import requests
import os
import asyncio
import random

with open("token.txt") as file:
    token = file.read()

intents = discord.Intents.default()
intents.message_content = True  # Aby bot mohl číst obsah zpráv

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

# Načtení CogManager
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Načítán cog: {filename}")


@bot.event
async def on_message(message):
    if message.content == ".":
        commands_list = """
        Dostupné příkazy:
        - .ping: Zobrazí "Pong!"
        - .pong: Zobrazí "Ping!"
        - .style <font> <text>: Vytvoří obrázek s daným fontem a textem.
        - .meme: Načte a zobrazí náhodný meme z Redditu (r/memes).    
        - .wakeup <uživatel>: Pošle soukromou zprávu uživateli.
        - .je <uživatel>: Odpoví vtipně na zmíněného uživatele.
        - .hello: Pozdraví tě.
        - .gay: Vtipná odpověď.
        - .ilikewomen: Odesílá GIF.
        - .quote: Získá náhodný citát z API.
        - .play <YouTube URL>: Přehrává zvuk z YouTube videa.
        - .next <YouTube URL>: Přidá skladbu do fronty.
        - .skip: Přeskočí aktuálně hranou skladbu.
        - .stop: Zastaví aktuální skladbu.
        - .resume: Obnoví zastavenou skladbu.
        - .leave: Opuštění hlasového kanálu.
        """
        await message.channel.send(commands_list)
    await bot.process_commands(message)

@bot.event
async def on_ready():
    print("Slime is here! Probably?")

async def main():
    async with bot:
        await load_cogs()  # Načtení všech cogů
        await bot.start(token)

# Spuštění hlavní funkce
import asyncio
asyncio.run(main())