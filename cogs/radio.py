import discord
from discord.ext import commands
import yt_dlp as youtube_dl

class RadioStreamer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.radio_urls = {  # Předdefinovaný seznam rádiových URL
            'orion': 'http://icecast1.play.cz/cro1-128.mp3',  # Český rozhlas - Radiožurnál
            'evropa2': 'http://icecast2.play.cz/evropa2-128.mp3',  # Evropa 2
            'kiss': 'https://www.kiss.cz/stream',  # Kiss rádio
            'fajn': 'http://stream.fajnradio.cz:8000/fajn_128.mp3',  # Fajn rádio
            'rock': 'http://listen.rockradio.cz:8000/rockradio128.mp3'  # Rock rádio
        }

    @commands.command(name='join', help='Bot se připojí na voice kanál.')
    async def join(self, ctx):
        if not ctx.author.voice:
            await ctx.send("Musíš být připojený na voice kanálu, aby se k tobě bot mohl připojit.")
            return

        channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command(name='exit_radio', help='Bot opustí voice kanál.')
    async def exit_radio(self, ctx):
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
            await ctx.send("Bot opustil voice kanál.")
        else:
            await ctx.send("Bot není připojen na žádném voice kanálu.")

    @commands.command(name='radio', help='Streamuje rádio na voice kanál. Použití: !radio <název nebo URL>.')
    async def radio(self, ctx, source: str):
        if ctx.voice_client is None:
            await ctx.send("Bot není připojen na voice kanálu. Použij příkaz `!join`.")
            return

        # Zjistí, zda je zadán název z předdefinovaného seznamu nebo přímo URL
        url = self.radio_urls.get(source.lower(), source)

        # Nastavení pro yt-dlp pro získání streamu
        ydl_opts = {
            'format': 'bestaudio/best',  # Vybere nejlepší kvalitu
            'postprocessors': [{
                'key': 'FFmpegAudio',
                'preferredcodec': 'mp3',  # Převede do formátu MP3
                'preferredquality': '192',
            }],
            'outtmpl': 'downloads/%(id)s.%(ext)s',  # Stahování do dočasné složky
            'quiet': True,
            'source_address': None,  # Pokud je potřeba, může se specifikovat IP adresa
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                audio_url = info_dict['url']  # Vezme přímý URL pro stream
                # Spustí stream pomocí FFMpegPCMAudio
                ctx.voice_client.play(discord.FFmpegPCMAudio(audio_url, executable="C:/ffmpeg/bin/ffmpeg.exe"), after=lambda e: print(f"Chyba při přehrávání: {e}"))
                await ctx.send(f"Přehrávám rádio z {url}.")
        except Exception as e:
            await ctx.send(f"Nastala chyba při pokusu o streamování rádia: {e}")

    @commands.command(name='list_radios', help='Zobrazí seznam dostupných rádií.')
    async def list_radios(self, ctx):
        radio_list = "\n".join([f"{name}: {url}" for name, url in self.radio_urls.items()])
        await ctx.send(f"Dostupná rádia:\n{radio_list}")

async def setup(bot):
    await bot.add_cog(RadioStreamer(bot))
