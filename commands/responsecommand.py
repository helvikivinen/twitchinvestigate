from commands.basecommand import BaseCommand

class ResponseCommand(BaseCommand):    

    def __init__(self, yaml_object):
        super().__init__(yaml_object)

    async def noop(self, ctx):
        print(self.description)
        return True