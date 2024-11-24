import discord
from discord.ext import commands

class Wakeup(commands.Cog):
    """
    Cog pro příkaz .wakeup
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wakeup(self, ctx, member: discord.Member = None):
        """
        Pošle 10 zpráv uživateli do DM. Použití: .wakeup @<uživatel>
        """
        if member is None:
            await ctx.send("Použití příkazu: .wakeup @<uživatel> - Pošle 10 zpráv uživateli do DM.")
            return

        try:
            if member.display_name.lower() == "mikeš síť guy":
                await ctx.send("Nemohu posílat zprávy uživateli.")
                return
            if member.display_name.lower() == "alpaca":
                await ctx.send("Nemohu posílat zprávy uživateli.")
                return

            # Odeslání 10 zpráv uživateli do DM
            for i in range(10):
                await member.send(f"Zpráva {i + 1}: Hni sebou hrajeme hry {i + 1}!")

            # Potvrzení v kanálu
            await ctx.send(f"Bylo odesláno 10 zpráv uživateli {member.display_name}!")

        except discord.Forbidden:
            # Pokud bot nemůže odeslat zprávu, například pokud má uživatel zakázané DM
            await ctx.send(f"Nemohu odeslat zprávu uživateli {member.display_name}. Možná má zakázané přímé zprávy.")

# Registrace cogu
async def setup(bot):
    await bot.add_cog(Wakeup(bot))
