import os
import discord
from discord.ext import commands
from datetime import datetime, timedelta, timezone

JST = timezone(timedelta(hours=+9), "JST")

class Events(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot
        self.category = os.getenv("CATEGORY_ID")
        self.sending_channel = os.getenv("SENDING_CHANNEL_ID")

        if self.category:
            self.category = int(self.category)

        if self.sending_channel:
            self.sending_channel = int(self.sending_channel)

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if message.channel.category_id != self.category:
            return

        if message.channel.id == self.sending_channel:
            return

        time = datetime.now(JST).strftime("%m/%d %H:%M")

        embed = discord.Embed(description=message.content, color=0xf4a460)
        embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
        embed.set_footer(text=time)

        channel = await self.bot.fetch_channel(self.sending_channel)
        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Events(bot))