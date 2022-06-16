from discord.ext.commands import Cog, command
from discord_components import Button

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
    async def show_buttons(self, ctx):
        await ctx.send("Test!", components=[Button(label="Test!!")])
        respond = await self.__bot.wait_for("button_click")

        if respond.channel == ctx.channel and respond.message.id == ctx.channel.last_message.id:
            await respond.respond(content=f"Button has been pressed!")
