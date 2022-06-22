from random import randrange

from interactions import Embed, ActionRow, Permissions, Option, OptionType, Color, User
from numexpr import evaluate

from objects.button.button_class import ButtonClass
from processing.management.logger.logger import Log
from processing.management.objects.objects_manager import ObjectsManager
from source.scripts import bot


class CommandsManager:

    def __init__(self, client):
        self.__bot = client
        self.__view = None
        self.__button = None
        self.__calculators_messages = []

        self.__calcs_ids = []
        self.__bot = ObjectsManager.get_object_by_name("BotClass")
        self.__listener = ObjectsManager.get_object_by_name("Listeners")
        # self.__calc_action_rows = [ActionRow(), ActionRow(), ActionRow(), ActionRow()]

    @property
    def calc_action_rows(self):
        return self.__calc_action_rows

    @property
    def calculator_message(self):
        return self.__calculators_messages

    def create_new_set_of_buttons(self):
        while True:
            random_number = randrange(-1_000_000, 1_000_000)

            if random_number not in self.__calcs_ids:
                break

        self.__calc_action_rows[0].append(ButtonClass(label="7", custom_id=f"{random_number}"))
        self.__calc_action_rows[0].append(ButtonClass(label="8", custom_id=f"{random_number}"))
        self.__calc_action_rows[0].append(ButtonClass(label="9", custom_id=f"{random_number}"))
        self.__calc_action_rows[0].append(ButtonClass(label="<-", custom_id=f"{random_number}"))
        self.__calc_action_rows[0].append(ButtonClass(label="CE", custom_id=f"{random_number}"))
        self.__calc_action_rows[1].append(ButtonClass(label="4", custom_id=f"{random_number}"))
        self.__calc_action_rows[1].append(ButtonClass(label="5", custom_id=f"{random_number}"))
        self.__calc_action_rows[1].append(ButtonClass(label="6", custom_id=f"{random_number}"))
        self.__calc_action_rows[1].append(ButtonClass(label="+", custom_id=f"{random_number}"))
        self.__calc_action_rows[1].append(ButtonClass(label="-", custom_id=f"{random_number}"))
        self.__calc_action_rows[2].append(ButtonClass(label="1", custom_id=f"{random_number}"))
        self.__calc_action_rows[2].append(ButtonClass(label="2", custom_id=f"{random_number}"))
        self.__calc_action_rows[2].append(ButtonClass(label="3", custom_id=f"{random_number}"))
        self.__calc_action_rows[2].append(ButtonClass(label="*", custom_id=f"{random_number}"))
        self.__calc_action_rows[2].append(ButtonClass(label="/", custom_id=f"{random_number}"))
        self.__calc_action_rows[3].append(ButtonClass(label=".", custom_id=f"{random_number}"))
        self.__calc_action_rows[3].append(ButtonClass(label="0", custom_id=f"{random_number}"))
        self.__calc_action_rows[3].append(ButtonClass(label="(", custom_id=f"{random_number}"))
        self.__calc_action_rows[3].append(ButtonClass(label=")", custom_id=f"{random_number}"))
        self.__calc_action_rows[3].append(ButtonClass(label="=", custom_id=f"{random_number}"))

    @staticmethod
    @bot.command(name="say", description="Command 1", options=[
        Option(
            name="message",
            description="A descriptive description",
            type=OptionType.STRING,
            required=True,
        ),
    ], )
    async def say(ctx, message):
        Log.info(f"N$say command has been called with {message}!")
        await ctx.send(f"The bot says ({message})")

    @bot.command(name="calculator", description="Command 2")
    async def calculator(self, ctx):
        self.create_new_set_of_buttons()
        self.__calculators_messages.append(await ctx.send("equation: ",
                                                          components=[self.__calc_action_rows[0],
                                                                      self.__calc_action_rows[1],
                                                                      self.__calc_action_rows[2],
                                                                      self.__calc_action_rows[3]]))

        self.__calc_action_rows[0] = ActionRow()
        self.__calc_action_rows[1] = ActionRow()
        self.__calc_action_rows[2] = ActionRow()
        self.__calc_action_rows[3] = ActionRow()

    @staticmethod
    @bot.command(name="clear", description="Command 3", default_member_permissions=Permissions.MANAGE_MESSAGES,
                 options=[
                     Option(
                         name="count",
                         description="A descriptive description",
                         type=OptionType.INTEGER,
                         required=False,
                     ),
                 ], )
    async def clear(ctx, count=10000000000000):
        channel = await ctx.get_channel()
        await channel.purge(count)
        await ctx.send("Done!")

    @staticmethod
    @bot.command(name="avatar", description="Command 4",
                 options=[
                     Option(
                         name="member",
                         description="A descriptive description",
                         type=OptionType.USER,
                         required=False,
                     ),
                 ], )
    async def avatar(ctx, member: User = None):
        member = ctx.author if member is None else member
        avatar_url = member.user.avatar_url

        embed_avatar = Embed(title="Avatar Link", url=avatar_url)
        embed_avatar.set_author(name=member.name, icon_url=avatar_url)
        embed_avatar.set_footer(text=f"Request came from {ctx.author.name}")
        embed_avatar.set_image(url=avatar_url)

        await ctx.send(embeds=[embed_avatar])

    @staticmethod
    @bot.command(name="basic_calc", description="Command 5", options=[
        Option(
            name="equation",
            description="A descriptive description",
            type=OptionType.STRING,
            required=True,
        ),
    ], )
    async def basic_calc(ctx, equation):

        try:
            embed_calc = Embed(title=f"{equation} = ",
                               description=f"{evaluate(equation)}",
                               color=Color().blurple)

            embed_calc.set_author(name=ctx.author.name, icon_url=ctx.author.get_member_avatar_url(912267573641494538))
            await ctx.send(embeds=[embed_calc])

        except Exception as E:
            Log.exception(E)

    @staticmethod
    @bot.command(name="ping", description="Command 6")
    async def ping(ctx):
        try:
            bot.latency

        except Exception as E:
            Log.exception(E)

        _ping = f'{round(bot.latency)} ms :signal_strength::globe_with_meridians: '
        embed = Embed(title="Pong!", description=_ping)

        try:
            await ctx.send(embeds=[embed])

        except Exception as E:
            Log.exception(E)
