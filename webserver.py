from bottle import Bottle
from sessionmanager import SessionManager


class MyHttpServer(Bottle):
    def __init__(self):
        super(MyHttpServer, self).__init__()
        self.sessionManager = SessionManager()

        self.route("/", callback=self.index)
        self.route("/hello", callback=self.hello)
        self.route("/leaderboard", callback=self.leaderboard)

    def index(self):
        return "index page"

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
