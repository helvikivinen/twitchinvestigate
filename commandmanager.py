import yaml

from twitchio.ext.commands import Command
from commands.commandtype import CommandType
from commands.responsecommand import ResponseCommand

class CommandManager:

    def load_commands(self):
        with open("commands.yaml", "r") as yamlStream:
            command_list = yaml.safe_load(yamlStream)

        commands = []
        for found_command in command_list['commands']:
            mapped_command = None
            match CommandType(found_command["type"]):
                case CommandType.responsecommand:
                    mapped_command = ResponseCommand(found_command)
            
            if mapped_command is not None:
                commands.append(Command(mapped_command.id, mapped_command.noop))
        
        return commands    