from twitchio.ext import commands, routines

from twitchio import Channel
from dotenv import load_dotenv
from viewermanager import ViewerManager
from commandmanager import CommandManager

import os
import random

load_dotenv()

command_prefix = "?"
commandlist = [
    command_prefix + "hello",
    command_prefix + "repeat",
    command_prefix + "setpoints",
    command_prefix + "diceroll",
    command_prefix + "points",
    command_prefix + "spend",
]


def str_to_int(strObj: str) -> int:
    if strObj.isdigit():
        return int(strObj, 10)
    else:
        raise Exception("bad data supplied to str_to_int")


class Bot(commands.Bot):
    def __init__(self):
        apikey = os.getenv("API_KEY")
        channel_name = os.getenv("CHANNEL_NAME")
        self.commandManager = CommandManager()
        self.viewerManager = ViewerManager()

        super().__init__(
            token=apikey, prefix=command_prefix, initial_channels=[channel_name]
        )

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f"Logged in as | {self.nick}")
        print(f"User ID is | {self.user_id}")

        for command in self.commandManager.load_commands():
            bot.add_command(command)
            print(f"Registering command `{command.name}` with bot")

    async def event_message(self, message):
        # first_word here is just message content so if a valid command, it WILL contain the command_prefix
        first_word = message.content.split(" ", 1)[0]

        if message.echo or not first_word.startswith(command_prefix):
            return

        print("event_message: ", end="")
        print(message.content)

        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f"Hello {ctx.author.name}!")

    @commands.command()
    async def points(self, ctx: commands.Context):
        amount = self.viewerManager.get_points(ctx.author.id)
        await ctx.send(f"{ctx.author.name}: {amount} points")

    @commands.command()
    async def spend(self, ctx: commands.Context):
        try:
            words = ctx.message.content.split(" ")
            spend_amount = str_to_int(words[1])
            user_points = self.viewerManager.get_points(ctx.author.id)
            if spend_amount > 0 and user_points >= spend_amount:
                remaining_points = self.viewerManager.deduct_points(
                    ctx.author.id, spend_amount
                )
                await ctx.send(
                    f"Thanks for the {spend_amount} points, {ctx.author.name}! remaining: {remaining_points}"
                )
            else:
                return False
        except Exception as e:
            return False

    @commands.command()
    async def diceroll(self, ctx: commands.Context):
        try:
            words = ctx.message.content.split(" ")
            dice = words[1]
            dice_words = dice.split("d")
            dice_amount = str_to_int(dice_words[0])
            dice_type = str_to_int(dice_words[1])
            result = 0
            if (
                isinstance(dice_amount, int)
                and isinstance(dice_type, int)
                and dice_amount >= 1
                and dice_amount <= 100
                and dice_type >= 1
                and dice_type <= 100
            ):
                result = random.randint(dice_amount, dice_amount * dice_type)
            else:
                return
            await ctx.send(
                f"{ctx.author.name} rolled {dice_amount}d{dice_type}: {result}"
            )
        except Exception as e:
            return False

    @commands.command()
    async def setpoints(self, ctx: commands.Context):
        try:
            if not ctx.author.is_mod:
                print(f"Non mod {ctx.author.name} tried to use `setpoints`")
                return

            words = ctx.message.content.split(" ")
            target_user = words[1]
            target_points = str_to_int(words[2])
            print(f"Getting user data for {target_user}")
            fetched_user_list = await bot.fetch_users(names=[target_user])
            twitch_id = fetched_user_list[0].id
            twitch_name = fetched_user_list[0].name
            print(f"> fetched user.id: {twitch_id}")
            print(f"> fetched user.name: {twitch_name}")

            self.viewerManager.insert_user_if_not_exists(twitch_id, twitch_name)
            self.viewerManager.set_points(twitch_id, target_points)

            await ctx.send(f"Set {target_user}'s points to {target_points}")
        except Exception as e:
            return False

    @commands.command()
    async def repeat(self, ctx: commands.Context):
        # ctx.command.name here does NOT contain the command_prefix
        await ctx.send(f"You used the command: {ctx.command.name}")

    # this runs as an async background task and not a memebr of the bot
    @routines.routine(seconds=30)
    async def point_heartbeat():
        # get the global bot object, this is equivalent to 'self'
        if bot._connection.is_alive:
            channel_name = os.getenv("CHANNEL_NAME")
            chatters = Channel(channel_name, bot._connection).chatters
            users = []
            for chatter in chatters:
                users.append(await chatter.user())

            bot.viewerManager.increment_points(users)

    point_heartbeat.start()


bot = Bot()
bot.run()
