from functools import reduce
from operator import or_
import random
from asyncio import PriorityQueue
import enum
import datetime

import sc2
from sc2 import Race, Difficulty
from sc2.player import Bot, Computer
from sc2.data import race_townhalls
from sc2.constants import LARVA, DRONE, OVERLORD, SPAWNINGPOOL

from PrioritizedItem import PrioritizedItem

DFLT_PRIO = 0 # Default priority for the queues

#============================= END BOT =============================#

class ShyZergling(sc2.BotAI):
    def __init__(self):
        self.building_queue = PriorityQueue()
        self.unit_queue = PriorityQueue()


    def debug(self, iteration):
        if iteration % 200 == 0:
            print("BUILDING QUEUE:", self.building_queue)
            print("UNIT QUEUE:", self.unit_queue)
            print("DRONE AMOUNT", len(self.drones))
            print()

    #### MAIN PROCESS

    async def on_step(self, iteration):
        self.larvae = self.units(LARVA)
        self.drones = self.units(DRONE)
        await self.build_drones()
        await self.extend_supply()
        await self.distribute_workers()
        await self.build_from_queues()
        self.debug(iteration)

    #### SUBFUNCTIONS

    # Unit queues
    async def build_from_queues(self):
        await self.build_buildings()
        await self.build_units()
        
    async def build_buildings(self):
        while not self.building_queue.empty():
            building = self.building_queue.get_nowait().item
            drones = self.drones
            if self.can_afford(building) and drones.exists:
                await self.do(drones.random.build(building, near=self.townhalls.first))

    async def build_units(self):
        while not self.unit_queue.empty():
            unit = self.unit_queue.get_nowait().item
            if self.can_afford(unit) and self.larvae.exists:
                await self.do(self.larvae.random.train(unit))

    # Building things
    async def extend_supply(self):
        if self.supply_left < 2:
            if self.can_afford(OVERLORD) and self.larvae.exists:
                await self.do(self.larvae.random.train(OVERLORD))

    async def build_drones(self):
        if len(self.drones) < 90:
            if self.can_afford(DRONE) and self.larvae.exists:
                await self.do(self.larvae.random.train(DRONE))
    
    async def build_spawningpool(self):
        if self.can_afford(SPAWNINGPOOL) and self.drones.exists:
            await self.do(self.drones.random.build(SPAWNINGPOOL, near=self.townhalls.first))
            print("Spawning pool created")

#============================= END BOT =============================#

def replay_name():
    return "Replays/ShyZergling"\
        +str(datetime.datetime.now()).replace(' ', '-').replace('.', '-').replace(':', '-')\
        +".SC2Replay"

def main():
    sc2.run_game(sc2.maps.get("CatalystLE"), [
        Bot(Race.Zerg, ShyZergling()),
        Computer(Race.Terran, Difficulty.Easy)
    ], realtime=False, save_replay_as=replay_name())

if __name__ == '__main__':
    main()
