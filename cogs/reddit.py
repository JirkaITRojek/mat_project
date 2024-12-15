import discord
from discord.ext import commands
from random import choice
import asyncpraw as praw
from settings import DEFAULT_SUBREDDIT, DEFAULT_SORT, VALID_SORTS


class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Načti client_id a client_secret ze souborů
        with open("client_id.txt", "r") as f:
            client_id = f.read().strip()
        with open("client_secret.txt", "r") as f:
            client_secret = f.read().strip()

        # Inicializuj Reddit API klienta
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent="script:randommeme:v1.0 (by u/Agitated_Arachnid891)"
        )

        self.used_posts = set()  # Sada pro uchování již zobrazených meme

    @commands.command()
    async def meme(self, ctx: commands.Context, subreddit: str = None, sort_type: str = None):
        """
        Zobrazí náhodný meme obrázek z vybraného subredditu a typu řazení.
        Použití: !meme [subreddit] [sort_type]
        - subreddit: Vybraný subreddit (výchozí: nastavený v settings.py)
        - sort_type: Typ řazení (hot, new, top, rising, controversial; výchozí: nastavený v settings.py)
        """

        # Použij výchozí hodnoty, pokud nejsou zadány argumenty
        subreddit = subreddit or DEFAULT_SUBREDDIT
        sort_type = sort_type or DEFAULT_SORT

        # Ověření platnosti typu řazení
        if sort_type not in VALID_SORTS:
            await ctx.send(f"Invalid sort type '{sort_type}'. Valid options are: {', '.join(VALID_SORTS)}.")
            return

        # Připojíme se k subredditu
        subreddit_obj = await self.reddit.subreddit(subreddit)
        post_list = []

        # Vyber příspěvky podle zvoleného typu řazení
        if sort_type == "hot":
            async for post in subreddit_obj.hot(limit=30):
                post_list.append(post)
        elif sort_type == "new":
            async for post in subreddit_obj.new(limit=30):
                post_list.append(post)
        elif sort_type == "top":
            async for post in subreddit_obj.top(limit=30):
                post_list.append(post)
        elif sort_type == "rising":
            async for post in subreddit_obj.rising(limit=30):
                post_list.append(post)
        elif sort_type == "controversial":
            async for post in subreddit_obj.controversial(limit=30):
                post_list.append(post)

        # Filtruj vhodné příspěvky
        valid_posts = [
            (post.id, post.url, post.author.name if post.author else "N/A")
            for post in post_list
            if not post.over_18 and any(post.url.endswith(ext) for ext in [".png", ".jpeg", ".jpg", ".gif", ".webp",
                                                                           ".gifv", ".bmp", ".tiff", ".tif"])
            and post.id not in self.used_posts
        ]

        if valid_posts:
            # Vybereme náhodný příspěvek
            random_post = choice(valid_posts)

            meme_embed = discord.Embed(
                title="Random meme",
                description=f"Fetches random meme from r/{subreddit} sorted by {sort_type}.",
                color=discord.Color.random()
            )
            meme_embed.set_author(name=f"Meme requested by {ctx.author.name}", icon_url=ctx.author.avatar)
            meme_embed.set_image(url=random_post[1])
            meme_embed.set_footer(text=f"Post created by {random_post[2]}.", icon_url=None)

            # Uložíme post.id jako zobrazený příspěvek
            self.used_posts.add(random_post[0])

            # Po zobrazení deseti příspěvků vyprázdníme seznam
            if len(self.used_posts) >= 10:
                self.used_posts.clear()

            await ctx.send(embed=meme_embed)
        else:
            await ctx.send("Unable to fetch post, try again later.")

    def cog_unload(self):
        self.bot.loop.create_task(self.reddit.close())


async def setup(bot):
    await bot.add_cog(Reddit(bot))
