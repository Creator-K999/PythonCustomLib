from discord.ext.commands import Cog, command

from processing.management.logger.logger import Log
from processing.management.objects.objects_manager import ObjectsManager


class CommandsManager(Cog):

    def __init__(self):

        self.__bot = ObjectsManager.get_object_by_name("BotClass")

    @command()
    async def say(self, ctx, *args):
        Log.info(f"N$say command has been called!")
        message = " ".join(args)
        await ctx.reply(f"The bot says ({message})")
