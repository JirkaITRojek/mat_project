import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from textwrap import fill
from io import BytesIO

available_fonts = {
    "brit": "./fonts/ANTIGB__.TTF",
    "nemec": "./fonts/ANTIGRG_.TTF",
    "krysa": "./fonts/rattfinny.ttf",
    # Přidej další fonty podle potřeby
}

class Write(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def style(self, ctx, font: str = None, *, text: str = None):
        if font is None or text is None:
            await ctx.send(
                "Použití příkazu: `.style <font> <text>`. Dostupné fonty jsou: " + ", ".join(available_fonts.keys()))
            return

        try:
            # Zkontroluj, zda uživatel zvolil dostupný font
            if font.lower() not in available_fonts:
                await ctx.send("Není dostupný tento font. Použij některý z těchto: " + ", ".join(available_fonts.keys()))
                return

            # Načti font na základě výběru uživatele
            font_path = available_fonts[font.lower()]

            # Zalamování textu na více řádků (pokud je dlouhý)
            wrapped_text = fill(text, width=20)

            # Vytvoření základního obrázku (bílý pozadí)
            img = Image.new('RGB', (500, 300), color=(255, 255, 255))
            d = ImageDraw.Draw(img)

            # Načti vybraný font
            meme_font = ImageFont.truetype(font_path, size=30)

            # Rozděl zalomený text na jednotlivé řádky
            lines = wrapped_text.split('\n')

            # Výpočet celkové výšky textu
            total_text_height = sum([d.textbbox((0, 0), line, font=meme_font)[3] for line in lines])

            # Začátek Y (vertikální zarovnání na střed)
            current_y = (img.height - total_text_height) // 2

            # Pro každý řádek textu: zarovnat na střed a vykreslit
            for line in lines:
                text_bbox = d.textbbox((0, 0), line, font=meme_font)
                text_width = text_bbox[2] - text_bbox[0]

                # Vypočítat x souřadnici pro zarovnání na střed
                text_x = (img.width - text_width) // 2

                # Přidání obrysu textu
                d.text((text_x - 1, current_y - 1), line, font=meme_font, fill=(0, 0, 0))
                d.text((text_x + 1, current_y - 1), line, font=meme_font, fill=(0, 0, 0))
                d.text((text_x - 1, current_y + 1), line, font=meme_font, fill=(0, 0, 0))
                d.text((text_x + 1, current_y + 1), line, font=meme_font, fill=(0, 0, 0))

                # Vložení hlavního bílého textu
                d.text((text_x, current_y), line, font=meme_font, fill=(255, 255, 255))

                # Posun y souřadnice dolů pro další řádek
                current_y += text_bbox[3] - text_bbox[1]

            # Uložení obrázku do paměti
            with BytesIO() as image_binary:
                img.save(image_binary, 'PNG')
                image_binary.seek(0)
                await ctx.send(file=discord.File(fp=image_binary, filename='meme.png'))

        except Exception as e:
            await ctx.send(f"Došlo k chybě při generování obrázek: {str(e)}")


async def setup(bot):
    await bot.add_cog(Write(bot))
