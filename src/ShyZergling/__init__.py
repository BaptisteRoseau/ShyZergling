import sc2

class ShyZergling(sc2.BotAI):
    from .Brain import Brain
    def __init__(self):
        pass
    
    # Required methods (do not change the order)
    from .expendCreep import expend_creep, build_tumours, expend_tumours, overlord_creep, compute_global_creepmap
    from .onStep import build_units, extend_supply, debug, expend_base, injections, cancel_building, build_extractors
    from .utils import generate_minimap

    # On Step method called every game iteration
    from .onStep import on_step, build_units, extend_supply

    def on_start(self):
        self.show_minimaps=True
        self._last_creep_map_check = 0 # Creep map time initialisation
        self.initial_minimap = self.generate_minimap() # A minimap with build locations and ramps
        #if self.show_minimaps:
        #    import cv2
        #    import numpy
        #    cv2.imshow('Global Minimap', self.initial_minimap())