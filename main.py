import discord
from discord.ext import commands
import os
import asyncio
from settings import BOT_TOKEN  # Import tokenu ze settings.py

intents = discord.Intents.default()
intents.message_content = True  # Aby bot mohl číst obsah zpráv

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

# Načtení CogManager
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Načítán cog: {filename}")


@bot.event
async def on_message(message):
    if message.content == ".":
        # Seznam všech příkazů načtených z cogs a základních příkazů
        commands_list = """
        Dostupné příkazy:
        """

        # Příprava na rozdělení příkazů podle kogn
        cogs_commands = {}

        for command in bot.commands:
            cog_name = command.cog_name if command.cog_name else "Základní příkazy"

            # Pokud kogn neexistuje, vytvoříme nový seznam pro příkazy
            if cog_name not in cogs_commands:
                cogs_commands[cog_name] = []

            cogs_commands[cog_name].append(command)

        # Seřazení příkazů abecedně v každém kog
        for cog_name, commands in cogs_commands.items():
            # Seřadíme příkazy podle názvu
            sorted_commands = sorted(commands, key=lambda c: c.name.lower())

            # Přidáme název kognu
            commands_list += f"\n**{cog_name}**:\n"

            # Dynamické načítání příkazů
            for command in sorted_commands:
                commands_list += f"- {command.name}: {command.help}\n"

        # Poslání zprávy
        await message.channel.send(commands_list)

    # Pokračujeme v zpracování dalších příkazů
    await bot.process_commands(message)

@bot.event
async def on_ready():
    print("Slime is here! Probably?")

async def main():
    async with bot:
        await load_cogs()  # Načtení všech cogs
        await bot.start(BOT_TOKEN)  # Použití tokenu ze settings.py

# Spuštění hlavní funkce
asyncio.run(main())
