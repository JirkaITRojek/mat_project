import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Slime is here! propably?")

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')


@bot.command()
async def wakeup(ctx, member: discord.Member):
    try:

        if member.display_name.lower() == "mikeš síť guy":
            await ctx.send("Nemohu posílat zprávy uživateli.")
            return
        if member.display_name.lower() == "alpaca":
            await ctx.send("Nemohu posílat zprávy uživateli.")
            return

        # Odeslání 10 zpráv uživateli do DM (soukromá zpráva)
        for i in range(10):
            await member.send(f"Zpráva {i + 1}: Hni sebou hrajeme hry {i + 1}!")

        # Potvrzení v kanálu, že zprávy byly odeslány
        await ctx.send(f"Bylo odesláno 10 zpráv uživateli {member.display_name}!")

    except discord.Forbidden:
        # Pokud bot nemůže odeslat zprávu, například pokud má uživatel zakázané DM
        await ctx.send(f"Nemohu odeslat zprávu uživateli {member.display_name}. Možná má zakázané přímé zprávy.")

@bot.command()
async def je(ctx, member: discord.Member):
    await ctx.send(f'Tvůj názor nás nezajímá {member.mention}!')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Ahoj, {ctx.author}!')

@bot.command()
async def gay(ctx):
    await ctx.send(f'Je , {ctx.author}!')

@bot.command()
async def ilikewomen(ctx):
    gif_url = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExOXg1OGI3azA1emYwZ2ZkcHdoYnAzMTh3eWtjNmJ4Z3B4cHk4cGc1cCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/I6n8YSKRIJqPwGll4n/giphy.gif"  # Zde vložte odkaz na váš GIF
    await ctx.send(gif_url)


with open("token.txt") as file:
    token = file.read()

bot.run(token)