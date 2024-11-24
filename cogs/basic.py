import discord
from discord.ext import commands

class BasicCommands(commands.Cog):
    """
     Cog pro základní příkazy (ping, hello, pong).
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Odpoví na příkaz .ping s 'Pong!'")
    async def ping(self, ctx):
        """
        Odpoví na příkaz .ping s "Pong!".
        """
        await ctx.send("Pong!")

    @commands.command(help="Odpoví na příkaz .pong s 'Ping!'")
    async def pong(self, ctx):
        """
        Odpoví na příkaz .pong s "Ping!".
        """
        await ctx.send("Ping!")

    @commands.command(help="Odpoví na příkaz .hello s pozdravem.")
    async def hello(self, ctx):
        """
        Odpoví na příkaz .hello s pozdravem.
        """
        await ctx.send(f'Ahoj, {ctx.author}!')

# Registrace cogu
async def setup(bot):
    await bot.add_cog(BasicCommands(bot))
