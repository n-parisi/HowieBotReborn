import os

import discord
import matplotlib.pyplot as plt
import wordcloud
from discord.ext import commands


class WordCloud(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wordcloud(self, ctx, limit=1000):
        if limit > 10000:
            limit = 10000

        comment_words = ''
        async for message in ctx.history(limit=int(limit)):
            comment_words += message.content.lower() + " "

        cloud = wordcloud.WordCloud(width=800, height=800,
                                    background_color='white',
                                    stopwords=wordcloud.STOPWORDS,
                                    min_font_size=10).generate(comment_words)

        # plot the WordCloud image
        plt.figure(figsize=(8, 8), facecolor=None)
        plt.imshow(cloud)
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.savefig("wordcloud.png")

        await ctx.send(file=discord.File("wordcloud.png"))
        os.remove("wordcloud.png")
