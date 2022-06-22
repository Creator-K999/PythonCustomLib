from datetime import datetime

from interactions import Extension, extension_listener

from discord import Embed, Colour, HTTPException
from numexpr import evaluate

from processing.management.logger.logger import Log
from processing.management.objects.objects_manager import ObjectsManager


class Listeners(Extension):

    def __init__(self, client):
        self.__bot = client
        self.__commands = None

        self.__view = None
        self.__attachment_log_channel = None
        self.__calculator_full_equation = [""]

    @extension_listener(name="on_message")
    async def on_message(self, message):

        if not message.author.bot:
            if message.attachments:
                embed = Embed(title=f"Message Link", url=message.jump_url, color=Colour.blurple())
                embed.set_author(name=await self.__bot.fetch_user(message.author.id))
                embed.set_footer(
                    text=f"Content of the message: {message.content or None}\n"
                         f"Time: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
                )
                await self.__attachment_log_channel.send(
                    embed=embed,
                    files=[await attach.to_file() for attach in message.attachments]
                )

    @extension_listener(name="on_ready")
    async def on_ready(self):
        self.__commands = ObjectsManager.get_object_by_name("CommandsManager")
        # self.__attachment_log_channel = await self.__bot.fetch_channel(926778297755500554)
        # DiscordComponents(self.__bot)

        Log.info("Bot is ready!")

    @extension_listener(name="on_button_click")
    async def on_button_click(self,  respond):
        button_label = respond.component.label

        if button_label == '=':
            await self.__commands.calculator_message.edit(
                content=f"{self.__calculator_full_equation} = {evaluate(self.__calculator_full_equation)}"
            )

            try:
                await respond.respond()

            except HTTPException as error:
                ...

            return

        elif button_label == "<-":
            self.__calculator_full_equation = self.__calculator_full_equation[:-1]

        elif button_label == "CE":
            self.__calculator_full_equation = ""

        else:
            self.__calculator_full_equation += button_label

        try:
            await self.__commands.calculator_message.edit(content=self.__calculator_full_equation)
            await respond.respond()

        except HTTPException as error:
            ...


def setup(client):
    Listeners(client)
