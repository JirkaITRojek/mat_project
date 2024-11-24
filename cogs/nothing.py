import discord
from discord.ext import commands

class FunCommands(commands.Cog):
    """
    Cog pro zábavné příkazy jako .je a .gay.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def je(self, ctx, member: discord.Member = None):
        """
        Odpoví vtipně na zmíněného uživatele.
        """
        if member is None:
            await ctx.send("Použití příkazu: .je @<uživatel> - Odpoví vtipně na zmíněného uživatele.")
            return

        await ctx.send(f'Tvůj názor nás nezajímá {member.mention}!')

        # Odeslání obrázku
        try:
            # Cesta k obrázku
            image_path = "./image/not-interested.jpg"
            await ctx.send(file=discord.File(image_path))
        except Exception as e:
            await ctx.send(f"Nepodařilo se odeslat obrázek: {str(e)}")

    @commands.command()
    async def gay(self, ctx):
        """
        Odpoví na příkaz .gay.
        """
        await ctx.send(f'Je , {ctx.author}!')

# Registrace cogu
async def setup(bot):
    await bot.add_cog(FunCommands(bot))
