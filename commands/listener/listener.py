from discord.ext.commands import Cog
from discord_components import DiscordComponents

from processing.management.logger.logger import Log
from processing.management.objects.objects_manager import ObjectsManager


class Listeners(Cog):

    def __init__(self):
        self.__bot = ObjectsManager.get_object_by_name("BotClass")
        self.__commands = ObjectsManager.get_object_by_name("CommandsManager")
        self.__view = None

    @Cog.listener()
    async def on_ready(self):
        # self.__bot.add_command(self.__commands.say)
        Log.info("Bot is ready!")
        DiscordComponents(self.__bot)

    @Cog.listener()
    async def on_button_click(self, respond):
        await respond.respond(content="Pressed !!!")
