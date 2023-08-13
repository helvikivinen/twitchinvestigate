from twitchio.ext import commands, routines
from twitchio import Channel, PartialChatter
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
commandlist = [
    command_prefix + "hello",
    command_prefix + "repeat",
    command_prefix + "setpoints",
]

def IncrementPoints(users):
    session = Session()
    for user in users:
        found_user = session.query(Viewer).filter(Viewer.twitch_id == user.id).scalar()
        if found_user is not None:
            print(f"Incrementing Point for {user.name}")
            found_user.channel_points += 1
            session.query(Viewer).filter(Viewer.twitch_id == user.id).update(
                {"channel_points": found_user.channel_points}
            )
        else:
            print(f"Record could not be found for {user.name}")            

    session.commit()

def insert_user_if_not_exists(twitch_id, twitch_name):
    session = Session()
    print("Session Created")

    viewerExists = session.query(
        session.query(Viewer).filter(Viewer.twitch_id == twitch_id).exists()
    ).scalar()

    if viewerExists:
        return
    else:
        new_viewer = Viewer(
            twitch_id=twitch_id,
            twitch_name=twitch_name,
            channel_points=0,
        )
        session.add(new_viewer)
        session.commit()
    return


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
                twitch_name=ctx.author.name,
                channel_points=0,
            )
            session.add(viewer)
            session.commit()

        await ctx.send(f"Hello {ctx.author.name}!")

    @commands.command()
    async def setpoints(self, ctx: commands.Context):
        if not ctx.author.is_mod:
            print(f"Non mod {ctx.author.name} tried to use `setpoints`")
            return

        words = ctx.message.content.split(" ")
        target_user = words[1]
        target_points = words[2]

        print(f"Getting user data for {target_user}")
        fetched_user_list = await bot.fetch_users(names=[target_user])
        twitch_id = fetched_user_list[0].id
        twitch_name = fetched_user_list[0].name
        print(f"> fetched user.id: {twitch_id}")
        print(f"> fetched user.name: {twitch_name}")

        insert_user_if_not_exists(twitch_id=twitch_id, twitch_name=twitch_name)

        session = Session()
        print("Session Created")
        session.query(Viewer).filter(Viewer.twitch_name == twitch_name).update(
            {"channel_points": target_points}
        )
        result = session.commit()
        if result is not None:
            # reflect what the command-user actually typed in chat by printing `target_user` over `twitch_name`
            await ctx.send(f"Set {target_user}'s points to {target_points}")
        else:
            await ctx.send(f"setpoints failed! no db rows were affected")

    @commands.command()
    async def repeat(self, ctx: commands.Context):
        # ctx.command.name here does NOT contain the command_prefix
        await ctx.send(f"You used the command: {ctx.command.name}")

    #this runs as an async background task and not a memebr of the bot    
    @routines.routine(minutes=1)
    async def get_points():   
        #get the global bot object, this is equivalent to 'self'
        if bot._connection.is_alive:     
            channel_name = os.getenv("CHANNEL_NAME")
            chatters = Channel(channel_name, bot._connection).chatters
            users = []
            for chatter in chatters:
                users.append(await chatter.user())
            
            IncrementPoints(users)

    get_points.start()


bot = Bot()
bot.run()
