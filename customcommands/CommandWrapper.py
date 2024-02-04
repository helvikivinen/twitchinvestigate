from twitchio.ext import commands

from steps.PrintStep import PrintStep
from steps.RandomNumberStep import RandomNumberStep

class CommandWrapper():
    def __init__(self, yaml_object):
        self.id = yaml_object['id']
        self.description = yaml_object['description']
        self.cost = yaml_object['cost']
        self.steps = yaml_object['steps']

    async def run_command(self, ctx: commands.Context):
        variableCollection = {}
        for step in self.steps:
            if step['type'] == 'PrintStep':
                command = PrintStep(variableCollection)
                await command.run(ctx, step['message'])
            
            if step['type'] == 'RandomNumber':
                command = RandomNumberStep(variableCollection)
                await command.run(step['min'], step['max'])
        return True