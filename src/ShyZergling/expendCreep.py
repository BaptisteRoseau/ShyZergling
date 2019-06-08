import sc2
from sc2.data import race_townhalls
from sc2.player import BotAI
from sc2.constants import OVERLORD, QUEEN, CREEPTUMOR, BUILD_CREEPTUMOR_QUEEN, BUILD_CREEPTUMOR_TUMOR,\
    CANCEL_CREEPTUMOR, BEHAVIOR_GENERATECREEPON, HATCHERY, LAIR

import cv2
import numpy as np

async def expend_creep(self):
    await self.compute_global_creepmap()
    await self.build_tumours()
    await self.expend_tumours()
    await self.overlord_creep()

async def build_tumours(self):
    queens = self.units(QUEEN).idle
    if queens.exists:
        tum_queens = queens.filter(lambda q: q.energy > 25) #TODO: Find a less hardcoded way to do that
        if tum_queens.exists:
            q = tum_queens.random
            loc = q.position  #TODO: tumour creation location
            await self.do(q(BUILD_CREEPTUMOR_QUEEN, loc))

async def expend_tumours(self):
    # Expending tumours
    tumours = self.units(CREEPTUMOR)
    if tumours.exists:
        for t in tumours:
            loc = t.position  #TODO: tumour creation location
            await self.do(t(BUILD_CREEPTUMOR_TUMOR, loc))

    # Canceling tumours if necessary
    unfinished_tumours = self.units(CREEPTUMOR).not_ready
    for ut in unfinished_tumours:
        if ut.health_percentage > 1.1*ut.build_progress and ut.health_percentage < 0.20:
            await self.do(ut(CANCEL_CREEPTUMOR))


async def overlord_creep(self):
    overlords = self.units(OVERLORD).idle
    if self.units(LAIR).ready.exists:
        for ov in overlords:
            await self.do(ov(BEHAVIOR_GENERATECREEPON))
            #TODO If overlord not casting creep, ov.cast(creep), eviter d'appeller cette fonction constament

async def compute_global_creepmap(self, force=False): #FIXME
    if force or self.time > self._last_creep_map_check + 10:
        width = self.state.creep.width
        heigth = self.state.creep.height
        game_data = np.zeros((width, heigth, 3), np.uint8)

        for i in range(heigth):
            for j in range(width):
                if self.state.creep.is_set((j, i)):
                    game_data[i, j] = (255, 255, 255)
        self.global_creepmap = game_data

        # flip horizontally to make our final fix in visual representation:
        flipped = cv2.flip(game_data, 0)
        resized = cv2.resize(flipped, dsize=None, fx=2, fy=2)

        if self.show_minimaps:
            cv2.imshow('Global Creep Map', resized)
            cv2.waitKey(1)
    
    self._last_creep_map_check = self.time
    

async def tumour_creepmap(self): #TODO
    pass