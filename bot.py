from twitchio.ext import commands
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from viewer import Viewer

import os
import viewer

load_dotenv()

db_file = "sqlite:///database.sqlite3"

engine = create_engine(db_file, echo=True)
Session = sessionmaker(bind=engine)
command_prefix = "?"
commandlist = [command_prefix + "hello", command_prefix + "repeat"]


class Bot(commands.Bot):
    def __init__(self):
        apikey = os.getenv("API_KEY")
        channel_name = os.getenv("CHANNEL_NAME")

        super().__init__(
            token=apikey, prefix=command_prefix, initial_channels=[channel_name]
        )

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f"Logged in as | {self.nick}")
        print(f"User ID is | {self.user_id}")

    async def event_message(self, message):
        # first_word here is just message content so if a valid command, it WILL contain the command_prefix
        first_word = message.content.split(" ", 1)[0]

        # if message.echo is true, it's a message by the bot
        # also, ignore messages that don't match a command in our commandlist
        # or first_word not in commandlist

        # print(f"first_word: {first_word}")
        # print(f"message_content: {message.content}")

        if message.echo or first_word not in commandlist:
            return

        print("event_message: ", end="")
        print(message.content)

        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        session = Session()
        print("Session Created")
        viewerExists = session.query(
            session.query(Viewer).filter(Viewer.twitch_id == ctx.author.id).exists()
        ).scalar()

        if not viewerExists:
            viewer = Viewer(
                twitch_id=ctx.author.id,
                twitch_display_name=ctx.author.display_name,
                channel_points=0,
            )
            session.add(viewer)
            session.commit()

        await ctx.send(f"Hello {ctx.author.name}!")

    @commands.command()
    async def repeat(self, ctx: commands.Context):
        # ctx.command.name here does NOT contain the command_prefix
        await ctx.send(f"You used the command: {ctx.command.name}")


bot = Bot()
bot.run()
