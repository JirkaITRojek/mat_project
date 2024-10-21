import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from textwrap import fill
import requests
import yt_dlp as youtube_dl  # Přidáno pro stahování zvuku z YouTube
import os
import asyncio

with open("token.txt") as file:
    token = file.read()

FFMPEG_PATH = 'C:/ffmpeg/bin/ffmpeg.exe'  # Zadej zde cestu k ffmpeg.exe
# Fronta pro skladby
song_queue = []
current_song = None

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())


@bot.event
async def on_message(message):
    if message.content == ".":
        commands_list = """
        Dostupné příkazy:
        - `.ping`: Zobrazí "Pong!"
        - `.pong`: Zobrazí "Ping!"
        - `.meme <font> <text>`: Vytvoří meme s daným fontem a textem.
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


available_fonts = {
    "brit": "./fonts/ANTIGB__.TTF",
    "nemec": "./fonts/ANTIGRG_.TTF",
    "krysa": "./fonts/rattfinny.ttf",
    # Přidej další fonty podle potřeby
}


@bot.command()
async def meme(ctx, font: str = None, *, text: str = None):
    if font is None or text is None:
        await ctx.send(
            "Použití příkazu: `.meme <font> <text>`. Dostupné fonty jsou: " + ", ".join(available_fonts.keys()))
        return

    try:
        # Zkontroluj, zda uživatel zvolil dostupný font
        if font.lower() not in available_fonts:
            await ctx.send("Není dostupný tento font. Použij některý z těchto: " + ", ".join(available_fonts.keys()))
            return

        # Načti font na základě výběru uživatele
        font_path = available_fonts[font.lower()]

        # Zalamování textu na více řádků (pokud je dlouhý)
        wrapped_text = fill(text, width=20)

        # Vytvoření základního obrázku (bílý pozadí)
        img = Image.new('RGB', (500, 300), color=(255, 255, 255))
        d = ImageDraw.Draw(img)

        # Načti vybraný font
        meme_font = ImageFont.truetype(font_path, size=30)

        # Rozděl zalomený text na jednotlivé řádky
        lines = wrapped_text.split('\n')

        # Výpočet celkové výšky textu
        total_text_height = sum([d.textbbox((0, 0), line, font=meme_font)[3] for line in lines])

        # Začátek Y (vertikální zarovnání na střed)
        current_y = (img.height - total_text_height) // 2

        # Pro každý řádek textu: zarovnat na střed a vykreslit
        for line in lines:
            text_bbox = d.textbbox((0, 0), line, font=meme_font)
            text_width = text_bbox[2] - text_bbox[0]

            # Vypočítat x souřadnici pro zarovnání na střed
            text_x = (img.width - text_width) // 2

            # Přidání obrysu textu
            d.text((text_x - 1, current_y - 1), line, font=meme_font, fill=(0, 0, 0))
            d.text((text_x + 1, current_y - 1), line, font=meme_font, fill=(0, 0, 0))
            d.text((text_x - 1, current_y + 1), line, font=meme_font, fill=(0, 0, 0))
            d.text((text_x + 1, current_y + 1), line, font=meme_font, fill=(0, 0, 0))

            # Vložení hlavního bílého textu
            d.text((text_x, current_y), line, font=meme_font, fill=(255, 255, 255))

            # Posun y souřadnice dolů pro další řádek
            current_y += text_bbox[3] - text_bbox[1]

        # Uložení obrázku do paměti
        with BytesIO() as image_binary:
            img.save(image_binary, 'PNG')
            image_binary.seek(0)
            await ctx.send(file=discord.File(fp=image_binary, filename='meme.png'))

    except Exception as e:
        await ctx.send(f"Došlo k chybě při generování meme: {str(e)}")


@bot.command()
async def wakeup(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send("Použití příkazu: `.wakeup @<uživatel>` - Pošle 10 zpráv uživateli do DM.")
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
async def je(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send("Použití příkazu: `.je @<uživatel>` - Odpoví vtipně na zmíněného uživatele.")
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


@bot.command()
async def ilikewomen(ctx):
    gif_url = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExOXg1OGI3azA1emYwZ2ZkcHdoYnAzMTh3eWtjNmJ4Z3B4cHk4cGc1cCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/I6n8YSKRIJqPwGll4n/giphy.gif"  # Zde vložte odkaz na váš GIF
    await ctx.send(gif_url)


@bot.command()
async def quote(ctx):
    try:
        # API endpoint pro náhodný citát
        response = requests.get("https://zenquotes.io/api/random")

        # Zkontroluj, zda je odpověď úspěšná (status kód 200)
        if response.status_code == 200:
            data = response.json()
            # Extrahuj citát a autora z odpovědi API
            quote = data[0]['q']
            author = data[0]['a']

            # Odešli citát do Discordu
            await ctx.send(f'"{quote}" – {author}')
        else:
            # Pokud API neodpoví úspěšně, odešli chybovou zprávu
            await ctx.send("Nemohu získat citát, zkuste to prosím později.")
    except Exception as e:
        # Zachytí chybu a odešle ji do Discordu
        await ctx.send(f"Došlo k chybě: {str(e)}")


@bot.command()
async def play(ctx, url: str = None):
    global current_song  # Declare as global to modify it

    if url is None:
        await ctx.send("Použijte příkaz `.play <YouTube URL>`.")
        return

    voice_client = ctx.voice_client

    # Pokud bot není připojen k hlasovému kanálu, připoj se k autorovi
    if not voice_client:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            voice_client = await channel.connect()
        else:
            await ctx.send("Nejste připojeni v hlasovém kanálu.")
            return

    # Přidání URL do fronty
    song_queue.append(url)

    # Pokud momentálně nic nehraje, přehraj první skladbu z fronty
    if not voice_client.is_playing():
        await play_next_song(ctx)

    current_song = url  # Uložení aktuální skladby


async def play_next_song(ctx):
    global current_song  # Declare as global to modify it

    if len(song_queue) == 0:
        await ctx.send("Fronta je prázdná.")
        return

    voice_client = ctx.voice_client

    # Vezme první URL ze seznamu a stáhne ji
    url = song_queue.pop(0)

    # Před stažením nové skladby odstraň starý soubor
    if os.path.exists('song.mp3'):
        os.remove('song.mp3')

    # Nastavení yt-dlp pro stažení zvuku z YouTube
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'song',  # Uloží stažený zvuk do souboru song.mp3
        'ffmpeg_location': FFMPEG_PATH,  # Nastav cestu k ffmpeg
    }

    # Stáhnutí a přehrání zvuku
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Přehrání staženého souboru v hlasovém kanálu s FFmpeg cestou
        voice_client.play(discord.FFmpegPCMAudio('song.mp3', executable=FFMPEG_PATH), after=lambda e: on_song_end(ctx))
        await ctx.send(f"Přehrávám zvuk z {url}")

        current_song = url  # Update the currently playing song
    except Exception as e:
        await ctx.send(f"Došlo k chybě při přehrávání: {str(e)}")


# Funkce, která spustí další skladbu po ukončení přehrávání
def on_song_end(ctx):
    bot.loop.create_task(play_next_song(ctx))


@bot.command()
async def stop(ctx):
    voice_client = ctx.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await ctx.send("Hudba byla zastavena. Můžete ji znovu spustit pomocí `.resume`.")
    else:
        await ctx.send("Momentálně žádná hudba nehraje.")


@bot.command()
async def resume(ctx):
    global current_song  # Declare as global to use the variable

    voice_client = ctx.voice_client
    if voice_client and not voice_client.is_playing() and current_song:
        # Play the currently saved song if it's paused
        voice_client.play(discord.FFmpegPCMAudio('song.mp3', executable=FFMPEG_PATH), after=lambda e: on_song_end(ctx))
        await ctx.send("Hudba byla obnovena.")
    else:
        await ctx.send("Hudba již hraje nebo nebyla žádná skladba přehrána.")


@bot.command()
async def skip(ctx):
    voice_client = ctx.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.stop()  # Zastav aktuální skladbu
        await ctx.send("Přehrávání aktuální skladby bylo přeskočeno.")
        await play_next_song(ctx)
    else:
        await ctx.send("Momentálně žádná hudba nehraje.")


@bot.command()
async def next(ctx, url: str = None):
    if url is None:
        await ctx.send("Použijte příkaz `.next <YouTube URL>` pro přidání skladby do fronty.")
        return

    # Přidání URL do fronty
    song_queue.append(url)
    await ctx.send(f"URL {url} byla přidána do fronty.")

    # Pokud nic nehraje, přehraj skladbu hned
    if not ctx.voice_client.is_playing():
        await play_next_song(ctx)


@bot.command()
async def leave(ctx):
    voice_client = ctx.voice_client
    if voice_client:
        await voice_client.disconnect()
        await ctx.send("Bot opustil hlasový kanál.")
    else:
        await ctx.send("Bot není připojen k žádnému hlasovému kanálu.")


@bot.event
async def on_ready():
    print("Slime is here! Probably?")


bot.run(token)
