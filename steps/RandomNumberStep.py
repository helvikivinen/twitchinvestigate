from steps.Step import Step
from twitchio.ext import commands
import random

class RandomNumberStep(Step):
    async def run(self, lowerNumber: int, higherNumber: int):
        self.variables['%randomNumber%'] = random.randint(lowerNumber, higherNumber)
        return True