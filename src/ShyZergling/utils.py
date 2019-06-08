import sc2
from sc2.data import race_townhalls
from sc2.player import BotAI
from sc2.constants import OVERLORD, QUEEN, CREEPTUMOR, BUILD_CREEPTUMOR_QUEEN, BUILD_CREEPTUMOR_TUMOR,\
    CANCEL_CREEPTUMOR, BEHAVIOR_GENERATECREEPON, HATCHERY, LAIR

import cv2
import numpy as np

def generate_minimap(self):
    minimap = np.zeros((self.game_info.map_size[1], self.game_info.map_size[0], 3), np.uint8)
    # Marking unplayable area in blank
    

    # Marking ramp area in grey (higher is lighter)


    # Marking Player/Ennemy start locations in green/red


    self.game_info

    # flip horizontally to make our final fix in visual representation:
    flipped = cv2.flip(minimap, 0)
    resized = cv2.resize(flipped, dsize=None, fx=2, fy=2)

    if self.show_minimaps:
        cv2.imshow('Global Creep Map', resized)
        cv2.waitKey(1)
    
    return resized
