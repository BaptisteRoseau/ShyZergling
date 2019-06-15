import sc2
from sc2.data import race_townhalls, ActionResult
from sc2.player import BotAI
from sc2.unit import Unit
from sc2.constants import OVERLORD, QUEEN, CREEPTUMOR, CREEPTUMORBURROWED, CREEPTUMORQUEEN,\
    BUILD_CREEPTUMOR_QUEEN, BUILD_CREEPTUMOR_TUMOR,\
    CANCEL_CREEPTUMOR, BEHAVIOR_GENERATECREEPON, HATCHERY, LAIR, ZERGBUILD_CREEPTUMOR

import cv2
import numpy as np

async def expend_creep(self):
    self.tumors = self.units(CREEPTUMOR) #Note: The other tumors cannot cast BUILD_CREEPTUMOR_TUMOR
    #await self.compute_global_creepmap()
    await self.queen_tumors()
    await self.tumor_tumors()
    await self.overlord_creep()

async def queen_tumors(self):
    queens = self.units(QUEEN).idle
    if queens.exists:
        tum_queens = queens.filter(lambda q: q.energy > 25) #TODO: Find a less hardcoded way to do that
        if tum_queens.exists:
            q = tum_queens.random
            loc = q.position.random_on_distance(1)
            await self.do(q(BUILD_CREEPTUMOR_QUEEN, loc))

async def tumor_tumors(self):
    # Expending tumors
    tumors = self.tumors
    if tumors.exists:
        for t in tumors:
            net_input = self.tumor_creepmap(self.positionsWithoutCreep, castingUnit=t) # Numpy inpu for the neural net
            loc = self.findCreepPlantLocation(t, )
            await self.do(t(BUILD_CREEPTUMOR_TUMOR, loc))

    # Canceling tumors if necessary
    unfinished_tumors = self.tumors.not_ready
    for ut in unfinished_tumors:
        if ut.health_percentage > 1.1*ut.build_progress and ut.health_percentage < 0.55:
            await self.do(ut(CANCEL_CREEPTUMOR))


async def overlord_creep(self): #TODO: le faire "on constructuction(LAIR1) ou OVERLORD"
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
    
    self._last_creep_map_check = self.time
    

async def tumor_creepmap(self, tumor: Unit): #TODO
    width = self.state.creep.width
    heigth = self.state.creep.height
    
    side = int(15) #TODO: Hardcode it
    local_creepmap = np.zeros((side, side, 3), np.uint8) # 0: creep, 1: unbuildable, 2:buildable
    pos = tumor.position

    # LEs indices ne sont pas les bons
    for i in range(max(pos.x - side//2, 0), min(pos.x + side//2 + 1, heigth)):
        for j in range(max(pos.y - side//2, 0), min(pos.y + side//2 + 1, width)):
            if self.state.creep.is_set((j, i)):
                cv2.circle(local_creepmap, (i, j), 2, (255, 0, 0), -1)
    cv2.imshow('Local creep map', local_creepmap)
    return local_creepmap
            


# Taken from https://github.com/BurnySc2/burny-bots-python-sc2/blob/master/CreepyBot/CreepyBot.py
def getPositionsAroundUnit(self, unit, minRange=0, maxRange=500, stepSize=1, locationAmount=32):
        # e.g. locationAmount=4 would only consider 4 points: north, west, east, south
        assert isinstance(unit, (Unit, Point2, Point3))
        if isinstance(unit, Unit):
            loc = unit.position.to2
        else:
            loc = unit
        positions = [Point2(( \
            loc.x + distance * math.cos(math.pi * 2 * alpha / locationAmount), \
            loc.y + distance * math.sin(math.pi * 2 * alpha / locationAmount))) \
            for alpha in range(locationAmount) # alpha is the angle here, locationAmount is the variable on how accurate the attempts look like a circle (= how many points on a circle)
            for distance in range(minRange, maxRange+1)] # distance depending on minrange and maxrange
        return positions

# Taken from https://github.com/BurnySc2/burny-bots-python-sc2/blob/master/CreepyBot/CreepyBot.py
async def findCreepPlantLocation(self, targetPositions, castingUnit, minRange=None, maxRange=None, stepSize=1, onlyAttemptPositionsAroundUnit=False, locationAmount=32, dontPlaceTumorsOnExpansions=True):
        """function that figures out which positions are valid for a queen or tumor to put a new tumor     
        
        Arguments:
            targetPositions {set of Point2} -- For me this parameter is a set of Point2 objects where creep should go towards 
            castingUnit {Unit} -- The casting unit (queen or tumor)
        
        Keyword Arguments:
            minRange {int} -- Minimum range from the casting unit's location (default: {None})
            maxRange {int} -- Maximum range from the casting unit's location (default: {None})
            onlyAttemptPositionsAroundUnit {bool} -- if True, it will only attempt positions around the unit (ideal for tumor), if False, it will attempt a lot of positions closest from hatcheries (ideal for queens) (default: {False})
            locationAmount {int} -- a factor for the amount of positions that will be attempted (default: {50})
            dontPlaceTumorsOnExpansions {bool} -- if True it will sort out locations that would block expanding there (default: {True})
        
        Returns:
            list of Point2 -- a list of valid positions to put a tumor on
        """

        assert isinstance(castingUnit, Unit)
        positions = []
        ability = self._game_data.abilities[ZERGBUILD_CREEPTUMOR.value]
        if minRange is None: minRange = 0
        if maxRange is None: maxRange = 500

        # get positions around the casting unit
        positions = self.getPositionsAroundUnit(castingUnit, minRange=minRange, maxRange=maxRange, stepSize=stepSize, locationAmount=locationAmount)

        # stop when map is full with creep
        if len(self.positionsWithoutCreep) == 0:
            return None

        # filter positions that would block expansions
        if dontPlaceTumorsOnExpansions and hasattr(self, "exactExpansionLocations"):
            positions = [x for x in positions if self.getHighestDistance(x.closest(self.exactExpansionLocations), x) > 3] 
            # TODO: need to check if this doesnt have to be 6 actually
            # this number cant also be too big or else creep tumors wont be placed near mineral fields where they can actually be placed

        # check if any of the positions are valid
        validPlacements = await self._client.query_building_placement(ability, positions)

        # filter valid results
        validPlacements = [p for index, p in enumerate(positions) if validPlacements[index] == ActionResult.Success]

        allTumors = self.units(CREEPTUMOR) | self.units(CREEPTUMORBURROWED) | self.units(CREEPTUMORQUEEN)
        # usedTumors = allTumors.filter(lambda x:x.tag in self.usedCreepTumors)
        unusedTumors = allTumors.filter(lambda x:x.tag not in self.usedCreepTumors)
        if castingUnit is not None and castingUnit in allTumors:
            unusedTumors = unusedTumors.filter(lambda x:x.tag != castingUnit.tag)

        # filter placements that are close to other unused tumors
        if len(unusedTumors) > 0:
            validPlacements = [x for x in validPlacements if x.distance_to(unusedTumors.closest_to(x)) >= 10] 

        validPlacements.sort(key=lambda x: x.distance_to(x.closest(self.positionsWithoutCreep)), reverse=False)

        if len(validPlacements) > 0:
            return validPlacements
        return None