from abc import ABC

class Step(ABC):
    def __init__(self, variableCollection):
        self.variables = variableCollection