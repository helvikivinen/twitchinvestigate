class YamlCommand:
    def __init__(self, yaml_object):
        self.id = yaml_object['id']
        self.description = yaml_object['description']
        self.cost = yaml_object['cost']

    async def noop(self, ctx):
        print("noop()")
        return True