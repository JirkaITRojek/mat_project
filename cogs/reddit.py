import discord
from discord.ext import commands
from random import choice
import asyncpraw as praw


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

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is ready")

    @commands.command()
    async def meme(self, ctx: commands.Context, subreddit: str = "memes"):
        # Připojíme se k subredditu
        subreddit = await self.reddit.subreddit(subreddit)
        post_list = []

        # Procházej příspěvky v hot (nejlepší příspěvky)
        async for post in subreddit.hot(limit=30):
            if not post.over_18 and post.author is not None and any(
                    post.url.endswith(ext) for ext in [".png", ".jpeg", "jpg", ".gif"]):
                if post.id not in self.used_posts:  # Zajistíme, že příspěvek ještě nebyl použit
                    author_name = post.author.name
                    post_list.append((post.id, post.url, author_name))
                if post.author is None:
                    if post.id not in self.used_posts:
                        post_list.append((post.id, post.url, "N/A"))

        if post_list:
            # Vybereme náhodný příspěvek
            random_post = choice(post_list)

            meme_embed = discord.Embed(title="Random meme", description=f"Fetches random meme from r/{subreddit}",
                                       color=discord.Color.random())
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
