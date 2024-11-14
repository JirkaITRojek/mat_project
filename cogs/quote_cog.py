import discord
from discord.ext import commands
import requests

class Quote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def quote(self, ctx):
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

# Tuto funkci použijte k nastavení cogu
async def setup(bot):
    await bot.add_cog(Quote(bot))
