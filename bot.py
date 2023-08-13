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

class Bot(commands.Bot):
    def __init__(self):
        apikey = os.getenv("API_KEY")
        channel_name = os.getenv("CHANNEL_NAME")        

        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=apikey, prefix="?", initial_channels=[channel_name])

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f"Logged in as | {self.nick}")
        print(f"User ID is | {self.user_id}")

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Print the contents of our message to console...
        print(message.content)

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        session = Session()
        print("Session Created")        
        viewerExists = session.query(session.query(Viewer).filter(Viewer.twitch_id == ctx.author.id).exists()).scalar()

        if not viewerExists:
            viewer = Viewer(twitch_id = ctx.author.id, twitch_display_name = ctx.author.display_name, channel_points = 0)
            session.add(viewer)
            session.commit()

        await ctx.send(f"Hello {ctx.author.name}!")


bot = Bot()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.
