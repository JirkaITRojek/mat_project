import discord
from discord.ext import commands
import random

# Definování třídy pro cog
class MadaraCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_gif = None  # Uchování posledního GIFu

    @commands.command(help="Pošle náhodný GIF z gifs.txt, který není stejný jako poslední.")
    async def madara(self, ctx):
        try:
            with open('gifs.txt', 'r') as file:
                gifs = file.readlines()

            # Odstranění bílých míst (např. nové řádky)
            gifs = [gif.strip() for gif in gifs]

            # Výběr náhodného GIFu, který není stejný jako ten předchozí
            random_gif = random.choice(gifs)
            while random_gif == self.last_gif:
                random_gif = random.choice(gifs)

            # Uložení aktuálního GIFu jako posledního
            self.last_gif = random_gif

            # Poslání náhodně vybraného GIFu
            await ctx.send(random_gif)

        except FileNotFoundError:
            await ctx.send("Soubor gifs.txt nebyl nalezen!")
        except Exception as e:
            await ctx.send(f"Došlo k chybě: {e}")

    @commands.command(help="Pošle GIF, který reprezentuje 'I like women'.")
    async def ilikewomen(self, ctx):
        gif_url = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExOXg1OGI3azA1emYwZ2ZkcHdoYnAzMTh3eWtjNmJ4Z3B4cHk4cGc1cCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/I6n8YSKRIJqPwGll4n/giphy.gif"  # Zde vložte odkaz na váš GIF
        await ctx.send(gif_url)

# Funkce pro nastavení cogu
async def setup(bot):
    await bot.add_cog(MadaraCog(bot))
