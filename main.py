import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from textwrap import fill
import requests
import yt_dlp as youtube_dl
import os
import asyncio

# Načtení tokenu z textového souboru
with open("token.txt") as file:
    token = file.read()

# Cesta k FFMPEG
FFMPEG_PATH = 'C:/ffmpeg/bin/ffmpeg.exe'

# Inicializace bota s prefixem a intenty
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

# Fronta pro skladby
song_queue = []
current_song = None

# Dostupné fonty pro meme příkaz
available_fonts = {
    "brit": "./fonts/ANTIGB__.TTF",
    "nemec": "./fonts/ANTIGRG_.TTF",
    "krysa": "./fonts/rattfinny.ttf",
}

# Načítání cogs
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Načítán cog: {filename}")

# Událost při spuštění bota
@bot.event
async def on_ready():
    print("Slime is here! Probably?")

# Seznam dostupných příkazů při odeslání "."
@bot.event
async def on_message(message):
    if message.content == ".":
        commands_list = """
        Dostupné příkazy:
        - `.ping`: Zobrazí "Pong!"
        - `.pong`: Zobrazí "Ping!"
        - `.style <font> <text>`: Vytvoří stylizovaný obrázek s daným fontem a textem (např. `.style brit Hello World`).
        - `.meme`: Načte a zobrazí náhodný meme z Redditu (r/memes).
        - `.wakeup <uživatel>`: Pošle soukromou zprávu uživateli.
        - `.je <uživatel>`: Odpoví vtipně na zmíněného uživatele.
        - `.hello`: Pozdraví tě.
        - `.gay`: Vtipná odpověď.
        - `.ilikewomen`: Odesílá GIF.
        - `.quote`: Získá náhodný citát z API.
        - `.play <YouTube URL>`: Přehrává zvuk z YouTube videa.
        - `.next <YouTube URL>`: Přidá skladbu do fronty.
        - `.skip`: Přeskočí aktuálně hranou skladbu.
        - `.stop`: Zastaví aktuální skladbu.
        - `.resume`: Obnoví zastavenou skladbu.
        - `.leave`: Opuštění hlasového kanálu.
        """
        await message.channel.send(commands_list)
    await bot.process_commands(message)

# Příkaz pro vytvoření stylizovaného obrázku s textem
@bot.command()
async def style(ctx, font: str = None, *, text: str = None):
    if font is None or text is None:
        await ctx.send(
            "Použití příkazu: `.style <font> <text>`. Dostupné fonty jsou: " + ", ".join(available_fonts.keys()))
        return

    try:
        # Zkontroluj, zda uživatel zvolil dostupný font
        if font.lower() not in available_fonts:
            await ctx.send("Není dostupný tento font. Použij některý z těchto: " + ", ".join(available_fonts.keys()))
            return

        font_path = available_fonts[font.lower()]
        wrapped_text = fill(text, width=20)

        img = Image.new('RGB', (500, 300), color=(255, 255, 255))
        d = ImageDraw.Draw(img)
        meme_font = ImageFont.truetype(font_path, size=30)
        lines = wrapped_text.split('\n')

        total_text_height = sum([d.textbbox((0, 0), line, font=meme_font)[3] for line in lines])
        current_y = (img.height - total_text_height) // 2

        for line in lines:
            text_bbox = d.textbbox((0, 0), line, font=meme_font)
            text_x = (img.width - (text_bbox[2] - text_bbox[0])) // 2
            d.text((text_x, current_y), line, font=meme_font, fill=(255, 255, 255))
            current_y += text_bbox[3] - text_bbox[1]

        with BytesIO() as image_binary:
            img.save(image_binary, 'PNG')
            image_binary.seek(0)
            await ctx.send(file=discord.File(fp=image_binary, filename='style.png'))

    except Exception as e:
        await ctx.send(f"Došlo k chybě při generování obrázku: {str(e)}")

# Hudební příkazy
@bot.command()
async def play(ctx, url: str = None):
    global current_song

    if url is None:
        await ctx.send("Použijte příkaz `.play <YouTube URL>`.")
        return

    voice_client = ctx.voice_client
    if not voice_client:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            voice_client = await channel.connect()
        else:
            await ctx.send("Nejste připojeni v hlasovém kanálu.")
            return

    song_queue.append(url)
    if not voice_client.is_playing():
        await play_next_song(ctx)

    current_song = url

async def play_next_song(ctx):
    global current_song

    if len(song_queue) == 0:
        await ctx.send("Fronta je prázdná.")
        return

    voice_client = ctx.voice_client
    url = song_queue.pop(0)

    if os.path.exists('song.mp3'):
        os.remove('song.mp3')

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
        'outtmpl': 'song', 'ffmpeg_location': FFMPEG_PATH,
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        voice_client.play(discord.FFmpegPCMAudio('song.mp3', executable=FFMPEG_PATH), after=lambda e: on_song_end(ctx))
        await ctx.send(f"Přehrávám zvuk z {url}")
        current_song = url
    except Exception as e:
        await ctx.send(f"Došlo k chybě při přehrávání: {str(e)}")

def on_song_end(ctx):
    bot.loop.create_task(play_next_song(ctx))

@bot.command()
async def stop(ctx):
    voice_client = ctx.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await ctx.send("Hudba byla zastavena.")

@bot.command()
async def resume(ctx):
    global current_song
    voice_client = ctx.voice_client
    if voice_client and not voice_client.is_playing() and current_song:
        voice_client.play(discord.FFmpegPCMAudio('song.mp3', executable=FFMPEG_PATH), after=lambda e: on_song_end(ctx))
        await ctx.send("Hudba byla obnovena.")

@bot.command()
async def skip(ctx):
    voice_client = ctx.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await ctx.send("Přehrávání aktuální skladby bylo přeskočeno.")
        await play_next_song(ctx)

@bot.command()
async def next(ctx, url: str = None):
    if url is None:
        await ctx.send("Použijte příkaz `.next <YouTube URL>` pro přidání skladby do fronty.")
        return
    song_queue.append(url)
    await ctx.send(f"URL {url} byla přidána do fronty.")
    if not ctx.voice_client.is_playing():
        await play_next_song(ctx)

@bot.command()
async def leave(ctx):
    voice_client = ctx.voice_client
    if voice_client:
        await voice_client.disconnect()
        await ctx.send("Bot opustil hlasový kanál.")

# Hlavní funkce pro spuštění bota a načtení cogs
async def main():
    async with bot:
        await load_cogs()
        await bot.start(token)

# Spuštění hlavní funkce
import asyncio
asyncio.run(main())
