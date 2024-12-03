import discord
from discord.ext import commands, tasks
import yt_dlp as youtube_dl
import random
import asyncio

# Cesta k FFmpeg
FFMPEG_PATH = 'C:/ffmpeg/bin/ffmpeg.exe'

class MusicPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False  # Flag pro kontrolu, zda je nějaká písnička přehrávána
        self.voice_channel = None
        self.song_queue = []  # Seznam písní, které budou přehrávány

        self.keywords = [  # Seznam náhodných klíčových slov pro vyhledání písniček
            "pop music", "rock hits", "top charts", "hip hop music", "indie songs", "jazz music", "sad songs"
        ]

    @commands.command(name='join', help='Bot se připojí na voice kanál.')
    async def join(self, ctx):
        if not ctx.author.voice:
            await ctx.send("Musíš být připojený na voice kanálu, aby se k tobě bot mohl připojit.")
            return

        channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command(name='exit', help='Bot opustí voice kanál.')
    async def exit(self, ctx):
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
            await ctx.send("Bot opustil voice kanál.")
        else:
            await ctx.send("Bot není připojen na žádném voice kanálu.")

    @commands.command(name='randomplay', help='Začne přehrávat náhodné písničky.')
    async def randomplay(self, ctx):
        if ctx.voice_client is None:
            await ctx.send("Bot není připojen na voice kanálu. Použij příkaz `!join`.")
            return

        self.voice_channel = ctx.voice_client
        await self.play_next_song(ctx)

    async def play_next_song(self, ctx):
        if self.is_playing:
            return

        self.is_playing = True

        # Vybere náhodné klíčové slovo pro hledání písničky na YouTube
        keyword = random.choice(self.keywords)
        song_url = await self.search_youtube(keyword)

        if not song_url:
            await ctx.send(f"Píseň pro '{keyword}' nebyla nalezena.")
            self.is_playing = False
            return

        # Přehrávání písničky
        self.voice_channel.play(discord.FFmpegPCMAudio(song_url, executable=FFMPEG_PATH), after=lambda e: self.after_song(ctx, e))
        await ctx.send(f"Přehrávám náhodnou písničku na téma: {keyword}.")

    async def search_youtube(self, keyword):
        with youtube_dl.YoutubeDL({'quiet': True, 'format': 'bestaudio/best'}) as ydl:
            search_query = f"{keyword} site:youtube.com"
            info_dict = ydl.extract_info(f"ytsearch:{search_query}", download=False)

            if 'entries' in info_dict:
                # Vrátíme URL první nalezené písničky
                return info_dict['entries'][0]['url']
            else:
                return None

    def after_song(self, ctx, error):
        # Po dokončení přehrávání písničky zkontrolujeme, zda máme další písničku v seznamu
        self.is_playing = False
        asyncio.run_coroutine_threadsafe(self.play_next_song(ctx), self.bot.loop)

    @commands.command(name='list_keywords', help='Zobrazí seznam klíčových slov pro náhodné písničky.')
    async def list_keywords(self, ctx):
        if not self.keywords:
            await ctx.send("Žádná klíčová slova nejsou definována.")
        else:
            keywords = "\n".join(self.keywords)
            await ctx.send(f"Seznam klíčových slov pro náhodné písničky:\n{keywords}")

    @commands.command(name='add_keyword', help='Přidá klíčové slovo pro hledání písniček. Použití: !add_keyword <klíčové slovo>.')
    async def add_keyword(self, ctx, *, keyword: str):
        self.keywords.append(keyword)
        await ctx.send(f"Klíčové slovo '{keyword}' bylo přidáno.")

async def setup(bot):
    await bot.add_cog(MusicPlayer(bot))
