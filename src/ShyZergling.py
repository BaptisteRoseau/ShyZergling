from functools import reduce
from operator import or_
import random
from asyncio import PriorityQueue

import sc2
from sc2 import Race, Difficulty
from sc2.constants import *
from sc2.player import Bot, Computer
from sc2.data import race_townhalls

import enum

class ShyZergling(sc2.BotAI):
    def __init__(self):
        self.building_queue = PriorityQueue()
        self.unit_queue = PriorityQueue()

    #### MAIN PROCESS

    async def on_step(self, iteration):
        self.larvae = self.units(LARVA)
        self.distribute_worker()
        self.build_from_queues(self)

    #### SUBFUNCTIONS

    async def build_from_queues(self):
        await self.extend_supply()
        await self.build_buildings()
        await self.build_units()
        
    async def build_buildings(self):
        while not building_queue.empty():
            building = building_queue.get()
            drones = self.units(DRONE)
            if self.can_afford(building) and drones.exists:
                await self.do(drones.random.build(building, near=self.race_townhalls.first))

    async def build_units(self):
        while not unit_queue.empty():
            unit = unit_queue.get()
            if self.can_afford(unit) and self.larvae.exists:
                await self.do(larvae.random.train(unit))

    async def extend_supply(self):
        if self.supply_left < 2:
            if self.can_afford(OVERLORD) and self.larvae.exists:
                await self.unit_queue.put(OVERLORD)
                return

def main():
    sc2.run_game(sc2.maps.get("CatalystLE"), [
        Bot(Race.Zerg, ShyZergling()),
        Computer(Race.Terran, Difficulty.Medium)
    ], realtime=False, save_replay_as="ZvT.SC2Replay")

if __name__ == '__main__':
    main()
