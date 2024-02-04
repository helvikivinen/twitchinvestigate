from bottle import Bottle
from bottle import template
from sessionmanager import SessionManager

command_prefix = "?"
commandlist = [
    command_prefix + "hello",
    command_prefix + "repeat",
    command_prefix + "setpoints",
    command_prefix + "diceroll",
    command_prefix + "points",
    command_prefix + "spend",
    command_prefix + "leaderboard",
]


class MyHttpServer(Bottle):
    def __init__(self):
        super(MyHttpServer, self).__init__()
        self.sessionManager = SessionManager()

        self.route("/", callback=self.index)
        self.route("/hello", callback=self.hello)
        self.route("/leaderboard", callback=self.leaderboard)

    def index(self):
        index_page = open("webpages/index.html", "r")
        command_list_items = []
        for command in commandlist:
            command_list_items += ["<li>{}</li>".format(command)]
        full_commands = "".join(command_list_items)
        print(full_commands)
        return template(index_page.read(), command_list_items=full_commands)

    def hello(self):
        return "hello, world"

    def run_server(self):
        Bottle.run(self, host="localhost", port=8080, debug=True)

    # @route("/hello")
    # def hello():
    #     return "Hello World!"

    # @route("/leaderboard")
    def leaderboard(self):
        top_users = self.sessionManager.get_top_users_by_points()
        user_strings = []
        for user in top_users:
            user_strings.append(f"{user.twitch_name}: {user.channel_points} points")
        joined_string = ", ".join(user_strings)
        return joined_string
