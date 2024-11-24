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

@bot.command()
async def wakeup(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send("Použití příkazu: .wakeup @<uživatel> - Pošle 10 zpráv uživateli do DM.")
        return

    try:
        if member.display_name.lower() == "mikeš síť guy":
            await ctx.send("Nemohu posílat zprávy uživateli.")
            return
        if member.display_name.lower() == "alpaca":
            await ctx.send("Nemohu posílat zprávy uživateli.")
            return

        # Odeslání 10 zpráv uživateli do DM (soukromá zpráva)
        for i in range(10):
            await member.send(f"Zpráva {i + 1}: Hni sebou hrajeme hry {i + 1}!")

        # Potvrzení v kanálu, že zprávy byly odeslány
        await ctx.send(f"Bylo odesláno 10 zpráv uživateli {member.display_name}!")

    except discord.Forbidden:
        # Pokud bot nemůže odeslat zprávu, například pokud má uživatel zakázané DM
        await ctx.send(f"Nemohu odeslat zprávu uživateli {member.display_name}. Možná má zakázané přímé zprávy.")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def je(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send("Použití příkazu: .je @<uživatel> - Odpoví vtipně na zmíněného uživatele.")
        return

    await ctx.send(f'Tvůj názor nás nezajímá {member.mention}!')

    # Odeslání obrázku
    try:
        # Cesta k obrázku
        image_path = "./image/not-interested.jpg"
        await ctx.send(file=discord.File(image_path))
    except Exception as e:
        await ctx.send(f"Nepodařilo se odeslat obrázek: {str(e)}")

@bot.command()
async def hello(ctx):
    await ctx.send(f'Ahoj, {ctx.author}!')

@bot.command()
async def gay(ctx):
    await ctx.send(f'Je , {ctx.author}!')

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