import aardvark as adv

class Connection():
    def __init__(self, source: str, target: str):
        self.source = source
        self.target = target

    def transfer(self, sol: dict):
        sol[self.target] = sol[self.source]