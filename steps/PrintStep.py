from steps.Step import Step
from twitchio.ext import commands
import re

class PrintStep(Step):
    async def run(self, ctx: commands.Context, message: str):
        formattedMessage = message
        regex_result = re.search(r"(%\w*%)", message)

        if regex_result is not None:
            for group in regex_result.groups():
                string_to_replace_with = self.variables[group]
                formattedMessage = formattedMessage.replace(group, str(string_to_replace_with))
        
        await ctx.send(formattedMessage)
        return True