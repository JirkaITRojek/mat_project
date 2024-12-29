import discord
from discord.ext import commands
import os
import yt_dlp as youtube_dl
import asyncio
from settings import FFMPEG_PATH

song_queue = []
current_song = None


class YouTube(commands.Cog):
    """
    Cog pro YouTube hudbu.
    """

    def __init__(self, bot):
        self.bot = bot

    async def play_next_song(self, ctx):
        global current_song

        if len(song_queue) == 0:
            await ctx.send("🎵 Fronta je prázdná.")
            current_song = None
            return

        voice_client = ctx.voice_client
        url = song_queue.pop(0)  # Take the next URL in the queue

        if os.path.exists('song.mp3'):
            os.remove('song.mp3')  # Remove old song file before downloading the new one

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'song',  # Soubor ke stažení
            'ffmpeg_location': FFMPEG_PATH,
            'quiet': False,  # Zobrazit výstup stahování
            'no_warnings': True,  # Potlačit varování
            'noplaylist': True,  # Stahovat pouze jedno video, ne playlist
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Neznámý název')
                await ctx.send(f"🎵 Připravuji skladbu: **{title}**")

                ydl.download([url])

            voice_client.play(
                discord.FFmpegPCMAudio('song.mp3', executable=FFMPEG_PATH),
                after=lambda e: self.bot.loop.create_task(self.play_next_song(ctx))
            )
            await ctx.send(f"▶️ Přehrávám: **{title}**")
            current_song = title

        except Exception as e:
            await ctx.send(f"❌ Chyba při přehrávání: {str(e)}")

    @commands.command(help="Přehrává hudbu z YouTube podle zadané URL.")
    async def play(self, ctx, url: str = None):
        """
        Přehrává hudbu z YouTube.
        """
        global current_song

        if url is None:
            await ctx.send("❗ Použijte příkaz `.play <YouTube URL>`.")
            return

        voice_client = ctx.voice_client

        if not voice_client:  # Join the user's voice channel if not connected
            if ctx.author.voice:
                channel = ctx.author.voice.channel
                voice_client = await channel.connect()
            else:
                await ctx.send("❗ Nejste připojeni v hlasovém kanálu.")
                return

        # Add the URL to the queue and play immediately if nothing is playing
        song_queue.append(url)
        if not voice_client.is_playing():
            await self.play_next_song(ctx)

        current_song = url  # Update the current song

    @commands.command(help="Zobrazí aktuální frontu skladeb.")
    async def queue(self, ctx):
        """
        Zobrazí frontu skladeb.
        """
        if len(song_queue) == 0:
            await ctx.send("🎵 Fronta je prázdná.")
        else:
            queue_list = "\n".join([f"**#{i+1}** {url}" for i, url in enumerate(song_queue)])
            await ctx.send(f"🎶 Fronta skladeb:\n{queue_list}")

    @commands.command(help="Zobrazí aktuálně přehrávanou skladbu.")
    async def nowplaying(self, ctx):
        """
        Zobrazí aktuálně přehrávanou skladbu.
        """
        if current_song:
            await ctx.send(f"🎶 Nyní hraje: **{current_song}**")
        else:
            await ctx.send("🎵 Momentálně žádná hudba nehraje.")

    @commands.command(help="Zastaví aktuálně přehrávanou hudbu.")
    async def stop(self, ctx):
        """
        Zastaví aktuálně přehrávanou skladbu.
        """
        voice_client = ctx.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()  # Stop the current song
            await ctx.send("⏹️ Hudba byla zastavena.")
        else:
            await ctx.send("❗ Momentálně žádná hudba nehraje.")

    @commands.command(help="Přeskočí aktuální skladbu.")
    async def skip(self, ctx):
        """
        Přeskočí aktuálně přehrávanou skladbu.
        """
        voice_client = ctx.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()  # Stop the current song to skip to the next one
            await ctx.send("⏭️ Přeskočil jsem skladbu.")
            await self.play_next_song(ctx)
        else:
            await ctx.send("❗ Momentálně žádná hudba nehraje.")

    @commands.command(help="Opustí hlasový kanál.")
    async def leave(self, ctx):
        """
        Opustí hlasový kanál.
        """
        voice_client = ctx.voice_client
        if voice_client:
            await voice_client.disconnect()  # Disconnect from the voice channel
            await ctx.send("👋 Bot opustil hlasový kanál.")
        else:
            await ctx.send("❗ Bot není připojen k žádnému hlasovému kanálu.")


# Function to set up the cog
async def setup(bot):
    await bot.add_cog(YouTube(bot))
