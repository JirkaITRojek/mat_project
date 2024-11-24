import discord
from discord.ext import commands

import os


class CogManager(commands.Cog):
    """
    Cog pro správu dalších cogs.
    Poskytuje příkazy pro načítání, vypínání, znovunačítání a zobrazení seznamu cogs.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def load_cog(self, ctx, cog_name: str):
        """
        Načte specifický cog podle názvu.
        Použití: .load_cog <název_cogu>
        """
        try:
            await self.bot.load_extension(f"cogs.{cog_name}")
            await ctx.send(f"Cog '{cog_name}' byl úspěšně načten.")
        except commands.ExtensionAlreadyLoaded:
            await ctx.send(f"Cog '{cog_name}' je již načten.")
        except commands.ExtensionNotFound:
            await ctx.send(f"Cog '{cog_name}' nebyl nalezen.")
        except Exception as e:
            await ctx.send(f"Chyba při načítání cogu '{cog_name}': {e}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unload_cog(self, ctx, cog_name: str):
        """
        Vypne specifický cog podle názvu.
        Použití: .unload_cog <název_cogu>
        """
        try:
            await self.bot.unload_extension(f"cogs.{cog_name}")
            await ctx.send(f"Cog '{cog_name}' byl úspěšně vypnut.")
        except commands.ExtensionNotLoaded:
            await ctx.send(f"Cog '{cog_name}' není načten.")
        except commands.ExtensionNotFound:
            await ctx.send(f"Cog '{cog_name}' nebyl nalezen.")
        except Exception as e:
            await ctx.send(f"Chyba při vypínání cogu '{cog_name}': {e}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reload_cog(self, ctx, cog_name: str):
        """
        Znovu načte specifický cog podle názvu.
        Použití: .reload_cog <název_cogu>
        """
        try:
            await self.bot.reload_extension(f"cogs.{cog_name}")
            await ctx.send(f"Cog '{cog_name}' byl úspěšně znovu načten.")
        except commands.ExtensionNotLoaded:
            await ctx.send(f"Cog '{cog_name}' není načten, použij `.load_cog {cog_name}`.")
        except commands.ExtensionNotFound:
            await ctx.send(f"Cog '{cog_name}' nebyl nalezen.")
        except Exception as e:
            await ctx.send(f"Chyba při znovunačítání cogu '{cog_name}': {e}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def list_cogs(self, ctx):
        """
        Zobrazí seznam názvů všech cogs.
        """
        cogs_folder = "./cogs"
        cog_files = [f for f in os.listdir(cogs_folder) if f.endswith(".py")]

        # Seznam názvů cogs
        cog_names = [cog_file[:-3] for cog_file in cog_files]

        # Vytvoření embed pro přehlednost
        embed = discord.Embed(
            title="Seznam Cogs",
            description="Názvy všech cogs:",
            color=discord.Color.blue()
        )

        # Přidání všech názvů cogs do embed
        for cog_name in cog_names:
            embed.add_field(name=cog_name, value="----", inline=False)

        # Odeslání embed zprávy
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(CogManager(bot))
