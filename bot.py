from twitchio.ext import commands
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()

db_connection = sqlite3.connect("database.sqlite3")
db_cursor = db_connection.cursor()


class Bot(commands.Bot):
    def __init__(self):
        apikey = os.getenv("API_KEY")

        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=apikey, prefix="?", initial_channels=["..."])

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
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(f"Hello {ctx.author.name}!")


bot = Bot()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.
