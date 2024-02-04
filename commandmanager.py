import yaml

from twitchio.ext.commands import Command
from customcommands.CommandWrapper import CommandWrapper


class CommandManager:

    def load_commands(self):
        with open("commands.yaml", "r") as yamlStream:
            command_list = yaml.safe_load(yamlStream)
            
        commands = []
        for found_command in command_list['commands']: 
            mapped_command = CommandWrapper(found_command)
            commands.append(Command(mapped_command.id, mapped_command.run_command))
        
        return commands
