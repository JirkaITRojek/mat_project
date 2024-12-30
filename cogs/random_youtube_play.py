import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import random

# Cesta k FFmpeg a klíčová slova
from settings import FFMPEG_PATH, KEYWORDS

class MusicPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.voice_channel = None
        self.stop_requested = False
        self.keywords = KEYWORDS

    @commands.command(name='play_random', help='Začne přehrávat náhodné písničky na základě témat.')
    async def play_random(self, ctx):
        if not ctx.author.voice:
            await ctx.send("Musíš být připojený na voice kanálu, aby se k tobě bot mohl připojit.")
            return

        # Připojení na voice kanál, pokud není připojen
        channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await channel.connect()
        elif ctx.voice_client.channel != channel:
            await ctx.voice_client.move_to(channel)

        self.voice_channel = ctx.voice_client
        self.stop_requested = False
        await self.play_next_song(ctx)

    async def play_next_song(self, ctx):
        if self.stop_requested:
            return

        keyword = random.choice(self.keywords)
        await ctx.send(f"Vybrané téma: **{keyword}**. Hledám a přehrávám písničku...")

        song_url = await self.search_youtube(keyword)

        if not song_url:
            await ctx.send(f"Nepodařilo se najít písničku pro téma: {keyword}. Zkouším další...")
            return await self.play_next_song(ctx)

        source = discord.FFmpegPCMAudio(song_url, executable=FFMPEG_PATH)
        self.voice_channel.play(source, after=lambda e: self.bot.loop.create_task(self.after_song(ctx, e)))

    async def search_youtube(self, keyword):
        with youtube_dl.YoutubeDL({'quiet': True, 'format': 'bestaudio/best'}) as ydl:
            search_query = f"{keyword} site:youtube.com"
            info_dict = ydl.extract_info(f"ytsearch:{search_query}", download=False)

            if 'entries' in info_dict and len(info_dict['entries']) > 0:
                return info_dict['entries'][0]['url']
            else:
                return None

    async def after_song(self, ctx, error):
        if error:
            await ctx.send("Došlo k chybě při přehrávání písničky.")
        if not self.stop_requested:
            await self.play_next_song(ctx)

    @commands.command(name='stop_random', help='Zastaví přehrávání hudby a odpojí bota z voice kanálu.')
    async def stop_random(self, ctx):
        if ctx.voice_client:
            self.stop_requested = True
            ctx.voice_client.stop()
            await ctx.voice_client.disconnect()
            await ctx.send("Přehrávání zastaveno a bot opustil voice kanál.")
        else:
            await ctx.send("Bot není připojen na žádném voice kanálu.")

    @commands.command(name='list_keywords', help='Zobrazí seznam klíčových slov pro náhodné písničky.')
    async def list_keywords(self, ctx):
        if not self.keywords:
            await ctx.send("Žádná klíčová slova nejsou definována.")
        else:
            keywords = "\n".join(self.keywords)
            await ctx.send(f"Seznam klíčových slov pro náhodné písničky:\n{keywords}")

async def setup(bot):
    await bot.add_cog(MusicPlayer(bot))
