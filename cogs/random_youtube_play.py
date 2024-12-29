import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import random
import asyncio

# Cesta k FFmpeg a klíčová slova
from settings import FFMPEG_PATH, KEYWORDS

class MusicPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False  # Flag pro kontrolu, zda je nějaká písnička přehrávána
        self.voice_channel = None
        self.song_queue = []  # Seznam písní, které budou přehrávány
        self.stop_requested = False  # Flag pro kontrolu, zda bylo požádáno o zastavení přehrávání

        # Použijeme klíčová slova ze settings
        self.keywords = KEYWORDS

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
        # Automatické připojení, pokud bot není připojen
        if ctx.voice_client is None:
            if not ctx.author.voice:
                await ctx.send("Musíš být připojený na voice kanálu, aby se k tobě bot mohl připojit.")
                return

            # Připojení k voice kanálu autora
            channel = ctx.author.voice.channel
            await channel.connect()

        self.voice_channel = ctx.voice_client
        self.stop_requested = False  # Resetuje příznak, pokud uživatel znovu spustí přehrávání
        await self.play_next_song(ctx)

    async def play_next_song(self, ctx):
        if self.is_playing or self.stop_requested:  # Zkontroluje, zda přehrávání pokračuje nebo bylo zastaveno
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
        source = discord.FFmpegPCMAudio(song_url, executable=FFMPEG_PATH)
        self.voice_channel.play(source, after=lambda e: self.after_song(ctx, e))
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
        if not self.stop_requested:  # Pokud nebylo přehrávání zastaveno, pokračujeme
            self.bot.loop.create_task(self.play_next_song(ctx))

    @commands.command(name='list_keywords', help='Zobrazí seznam klíčových slov pro náhodné písničky.')
    async def list_keywords(self, ctx):
        if not self.keywords:
            await ctx.send("Žádná klíčová slova nejsou definována.")
        else:
            keywords = "\n".join(self.keywords)
            await ctx.send(f"Seznam klíčových slov pro náhodné písničky:\n{keywords}")

    @commands.command(name='stop_random', help='Zastaví přehrávání náhodných písniček.')
    async def stop_random(self, ctx):
        if ctx.voice_client is not None:
            ctx.voice_client.stop()  # Zastavení přehrávání
            self.is_playing = False
            self.stop_requested = True  # Nastaví příznak zastavení
            await ctx.send("Přehrávání bylo zastaveno a nebude pokračovat.")
        else:
            await ctx.send("Bot není připojen na žádném voice kanálu nebo není aktivní přehrávání.")

async def setup(bot):
    await bot.add_cog(MusicPlayer(bot))
