import yaml

from command import YamlCommand
from twitchio.ext.commands import Command

class CommandManager:

    def load_commands(self):
        with open("commands.yaml", "r") as yamlStream:
            command_list = yaml.safe_load(yamlStream)

        commands = []
        for found_command in command_list['commands']:
            mapped_command = YamlCommand(found_command)
            commands.append(Command(mapped_command.id, mapped_command.noop))
        
        return commands    