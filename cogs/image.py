import discord
from discord.ext import commands
import os
import random

class ImageSender(commands.Cog):
    """
    Cog pro odesílání obrázků ze složky.
    """

    def __init__(self, bot):
        self.bot = bot
        self.image_folder = "./image"  # Cesta ke složce s obrázky

    @commands.command(name="image", help="Pošle obrázek ze složky. Zadejte číslo obrázku nebo nechte náhodně vybrat.")
    async def send_image(self, ctx, image_number: int = None):
        """
        Pošle obrázek ze složky. Obrázek je vybrán podle čísla, nebo náhodně.
        """
        # Kontrola existence složky
        if not os.path.exists(self.image_folder):
            await ctx.send("Složka s obrázky neexistuje.")
            return

        # Seznam všech souborů ve složce
        images = [f for f in os.listdir(self.image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

        if not images:
            await ctx.send("Ve složce nejsou žádné obrázky.")
            return

        # Výběr obrázku podle čísla nebo náhodně
        if image_number is not None:
            if 1 <= image_number <= len(images):
                selected_image = images[image_number - 1]
            else:
                await ctx.send(f"Zadejte číslo mezi 1 a {len(images)}.")
                return
        else:
            selected_image = random.choice(images)

        # Absolutní cesta k obrázku
        image_path = os.path.join(self.image_folder, selected_image)

        # Poslání obrázku
        file = discord.File(image_path, filename=selected_image)
        await ctx.send(file=file, content=f"Zde je váš obrázek: {selected_image}")

    @commands.command(name="list_images", help="Vypíše seznam dostupných obrázků seřazených podle čísel.")
    async def list_images(self, ctx):
        """
        Vypíše seznam dostupných obrázků ve složce.
        """
        if not os.path.exists(self.image_folder):
            await ctx.send("Složka s obrázky neexistuje.")
            return

        images = [f for f in os.listdir(self.image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

        if not images:
            await ctx.send("Ve složce nejsou žádné obrázky.")
            return

        # Vytvoření seznamu obrázků s čísly
        image_list = "\n".join([f"{i + 1}. {img}" for i, img in enumerate(images)])
        await ctx.send(f"Dostupné obrázky:\n{image_list}")

async def setup(bot):
    await bot.add_cog(ImageSender(bot))
