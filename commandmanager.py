import yaml

from command import Command

class CommandManager:

    def load_commands(self):
        with open("commands.yaml", "r") as yamlStream:
            command_list = yaml.safe_load(yamlStream)

        self.commands = []

        for found_command in command_list['commands']:
            self.commands.append(Command(found_command))

    def find_command(self, input) -> Command | None:
        for command in self.commands:
            if command.id == input[1:]:
                return command
            
        return None