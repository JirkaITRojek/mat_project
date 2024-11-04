# cogs/youtube.py
import discord
from discord.ext import commands
import os
import yt_dlp as youtube_dl
import asyncio

# Define the path to ffmpeg and initialize the queue and current song variable
FFMPEG_PATH = 'C:/ffmpeg/bin/ffmpeg.exe'
song_queue = []
current_song = None


class YouTube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def play_next_song(self, ctx):
        global current_song

        if len(song_queue) == 0:
            await ctx.send("Fronta je prázdná.")
            return

        voice_client = ctx.voice_client
        url = song_queue.pop(0)  # Take the next URL in the queue

        if os.path.exists('song.mp3'):
            os.remove('song.mp3')  # Remove old song file before downloading the new one

        # Download the next song from YouTube
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'song',  # Save downloaded audio as song.mp3
            'ffmpeg_location': FFMPEG_PATH,
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            # Play the downloaded song
            voice_client.play(
                discord.FFmpegPCMAudio('song.mp3', executable=FFMPEG_PATH),
                after=lambda e: self.bot.loop.create_task(self.play_next_song(ctx))
            )
            await ctx.send(f"Přehrávám zvuk z {url}")
            current_song = url  # Update the currently playing song

        except Exception as e:
            await ctx.send(f"Došlo k chybě při přehrávání: {str(e)}")

    @commands.command()
    async def play(self, ctx, url: str = None):
        global current_song

        if url is None:
            await ctx.send("Použijte příkaz `.play <YouTube URL>`.")
            return

        voice_client = ctx.voice_client

        if not voice_client:  # Join the user's voice channel if not connected
            if ctx.author.voice:
                channel = ctx.author.voice.channel
                voice_client = await channel.connect()
            else:
                await ctx.send("Nejste připojeni v hlasovém kanálu.")
                return

        # Add the URL to the queue and play immediately if nothing is playing
        song_queue.append(url)
        if not voice_client.is_playing():
            await self.play_next_song(ctx)

        current_song = url  # Update the current song

    @commands.command()
    async def next(self, ctx, url: str = None):
        if url is None:
            await ctx.send("Použijte příkaz `.next <YouTube URL>` pro přidání skladby do fronty.")
            return

        song_queue.append(url)  # Add the URL to the queue
        await ctx.send(f"URL {url} byla přidána do fronty.")

        if not ctx.voice_client.is_playing():  # Play immediately if nothing is playing
            await self.play_next_song(ctx)

    @commands.command()
    async def stop(self, ctx):
        voice_client = ctx.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()  # Stop the current song
            await ctx.send("Hudba byla zastavena. Můžete ji znovu spustit pomocí `.resume`.")
        else:
            await ctx.send("Momentálně žádná hudba nehraje.")

    @commands.command()
    async def resume(self, ctx):
        global current_song

        voice_client = ctx.voice_client
        if voice_client and not voice_client.is_playing() and current_song:
            # Play the currently saved song if it's paused
            voice_client.play(
                discord.FFmpegPCMAudio('song.mp3', executable=FFMPEG_PATH),
                after=lambda e: self.bot.loop.create_task(self.play_next_song(ctx))
            )
            await ctx.send("Hudba byla obnovena.")
        else:
            await ctx.send("Hudba již hraje nebo nebyla žádná skladba přehrána.")

    @commands.command()
    async def skip(self, ctx):
        voice_client = ctx.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()  # Stop the current song to skip to the next one
            await ctx.send("Přehrávání aktuální skladby bylo přeskočeno.")
            await self.play_next_song(ctx)
        else:
            await ctx.send("Momentálně žádná hudba nehraje.")

    @commands.command()
    async def leave(self, ctx):
        voice_client = ctx.voice_client
        if voice_client:
            await voice_client.disconnect()  # Disconnect from the voice channel
            await ctx.send("Bot opustil hlasový kanál.")
        else:
            await ctx.send("Bot není připojen k žádnému hlasovému kanálu.")


# Function to set up the cog
async def setup(bot):
    await bot.add_cog(YouTube(bot))
