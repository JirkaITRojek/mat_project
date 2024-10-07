import discord
from discord.ext import commands
import openai
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO


with open("token.txt") as file:
    token = file.read()

with open('api_key.txt', 'r') as file:
    OPENAI_API_KEY = file.read().strip()  # Načtení a odstranění případných bílých znaků

# Inicializace OpenAI
openai.api_key = OPENAI_API_KEY


bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

@bot.command()
async def meme(ctx, *, text: str):
    # Vytvoření základního meme obrázku (bílý pozadí)
    img = Image.new('RGB', (500, 300), color=(255, 255, 255))
    d = ImageDraw.Draw(img)

    # Použití výchozího fontu, nebo lze použít vlastní font, pokud máš
    font = ImageFont.load_default()

    # Získání rozměrů textu
    text_bbox = d.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Vložení textu na obrázek
    # Text bude umístěn uprostřed obrázku
    text_x = (img.width - text_width) // 2
    text_y = (img.height - text_height) // 2
    d.text((text_x, text_y), text, font=font, fill=(0, 0, 0))

    # Uložení obrázku do paměti
    with BytesIO() as image_binary:
        img.save(image_binary, 'PNG')
        image_binary.seek(0)
        await ctx.send(file=discord.File(fp=image_binary, filename='meme.png'))


@bot.event
async def on_ready():
    print("Slime is here! propably?")

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def pong(ctx):
    await ctx.send('Ping!')


@bot.command()
async def wakeup(ctx, member: discord.Member):
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
async def je(ctx, member: discord.Member):
    await ctx.send(f'Tvůj názor nás nezajímá {member.mention}!')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Ahoj, {ctx.author}!')

@bot.command()
async def gay(ctx):
    await ctx.send(f'Je , {ctx.author}!')

@bot.command()
async def ilikewomen(ctx):
    gif_url = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExOXg1OGI3azA1emYwZ2ZkcHdoYnAzMTh3eWtjNmJ4Z3B4cHk4cGc1cCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/I6n8YSKRIJqPwGll4n/giphy.gif"  # Zde vložte odkaz na váš GIF
    await ctx.send(gif_url)




bot.run(token)