import sc2

class ShyZergling(sc2.BotAI):
    def __init__(self):
        pass
    
    # On Step method called every game iteration
    from .onStep import on_step
