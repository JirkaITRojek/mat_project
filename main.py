import discord
from discord.ext import commands
import os
import asyncio

with open("token.txt") as file:
    token = file.read()

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

        # Seřazení příkazů abecedně
        sorted_commands = sorted(bot.commands, key=lambda c: c.name.lower())

        # Dynamické načítání příkazů
        for command in sorted_commands:
            commands_list += f"- {command}: {command.help}\n"

        await message.channel.send(commands_list)
    await bot.process_commands(message)

@bot.event
async def on_ready():
    print("Slime is here! Probably?")

async def main():
    async with bot:
        await load_cogs()  # Načtení všech cogs
        await bot.start(token)

# Spuštění hlavní funkce
import asyncio
asyncio.run(main())
