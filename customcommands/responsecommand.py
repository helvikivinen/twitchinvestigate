from customcommands.basecommand import BaseCommand
from twitchio.ext import commands

class ResponseCommand(BaseCommand):    

    def __init__(self, yaml_object):
        super().__init__(yaml_object)

    async def run_command(self, ctx: commands.Context):
        await ctx.send(self.description)
        return True