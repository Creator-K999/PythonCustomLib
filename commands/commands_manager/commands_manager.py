from discord import Member, Embed, Colour
from discord.ext.commands import Cog, command, has_permissions

from objects.button.button_class import ButtonClass
from processing.management.logger.logger import Log
from processing.management.objects.objects_manager import ObjectsManager


class CommandsManager(Cog):

    def __init__(self):
        self.__bot = ObjectsManager.get_object_by_name("BotClass")
        self.__view = None
        self.__button = None

    @command()
    async def say(self, ctx, *args):
        Log.info(f"N$say command has been called!")
        message = " ".join(args)
        await ctx.reply(f"The bot says ({message})")

    @command()
    @has_permissions(manage_channels=True)
    async def show_button(self, ctx):
        await ctx.send("Test!", components=[ButtonClass(label="Test!!")])

    @command()
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, count=10000000000000):
        await ctx.channel.purge(limit=count)

    @command(name="avatar")
    async def avatar(self, ctx, member: Member = None):
        avatar_url = ctx.author.avatar_url if member is None else member.avatar_url

        embed_avatar = Embed(title="Avatar Link", url=avatar_url, color=Colour.dark_grey())
        embed_avatar.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed_avatar.set_footer(text=f"Request came from {await self.__bot.fetch_user(ctx.author.id)}")
        embed_avatar.set_image(url=avatar_url)

        await ctx.reply(embed=embed_avatar)
