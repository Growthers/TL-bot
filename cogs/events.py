import os
import re
import discord
from discord.ext import commands
from datetime import datetime, timedelta, timezone

JST = timezone(timedelta(hours=+9), "JST")

class Events(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot
        self.guild = os.getenv("GUILD_ID")
        self.category = os.getenv("CATEGORY_ID")
        self.sending_channel = os.getenv("SENDING_CHANNEL_ID")
        self.url_sending_channel = os.getenv("URL_SENDING_CHANNEL_ID")
        self.ignore_category_list = os.getenv("IGNORE_CATEGORY_LIST")

        if self.guild:
            self.guild = int(self.guild)

        if self.category:
            self.category = int(self.category)

        if self.sending_channel:
            self.sending_channel = int(self.sending_channel)

        if self.url_sending_channel:
            self.url_sending_channel = int(self.url_sending_channel)

        if self.ignore_category_list:
            try:
                self.ignore_category_list = eval(self.ignore_category_list)
            except Exception as e:
                print(e)
                self.ignore_category_list = []

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if message.channel.guild.id != self.guild:
            return

        urls = re.findall("https?://[\w!\?/\+\-_~=;\.,\*&@#\$%\(\)'\[\]]+", message.content)

        isIgnore = False

        for ignore_category in self.ignore_category_list:
            if str(message.channel.category_id) == ignore_category:
                isIgnore = True

        if not isIgnore:
            for url in urls:
                url_channel = await self.bot.fetch_channel(self.url_sending_channel)
                await url_channel.send(url)

        if message.channel.category_id != self.category:
            return

        if message.channel.id == self.sending_channel:
            return

        time = datetime.now(JST).strftime("%m/%d %H:%M")
        author = message.author

        embed = discord.Embed(description=message.content, color=0xf4a460)
        embed.set_author(name=f"{author.display_name} ({author.name}#{author.discriminator})", icon_url=author.avatar_url)
        embed.set_footer(text=time)

        channel = await self.bot.fetch_channel(self.sending_channel)
        await channel.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx):
        self.bot.dispatch("reload")
        await ctx.send("Reload completed!")

    @reload.error
    async def reload_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            return
        print(error)

def setup(bot):
    bot.add_cog(Events(bot))