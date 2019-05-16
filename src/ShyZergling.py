from functools import reduce
from operator import or_
import random

import sc2
from sc2 import Race, Difficulty
from sc2.constants import *
from sc2.player import Bot, Computer
from sc2.data import race_townhalls

import enum

class ShyZergling(sc2.BotAI):
    def __init__(self):
        self._larvae = None

    def select_target(self):
        if self.known_enemy_structures.exists:
            return random.choice(self.known_enemy_structures).position

        return self.enemy_start_locations[0]
    
    async def queens_injections(self):
        """ Realises queens injections for each base. """
        available_queens = set(self.units(QUEEN).idle)
        for base in self.townhalls:
            if base.is_ready:
                #TODO If not already injected
                #TODO Select nearest queen
                for queen in available_queens:
                    abilities = await self.get_available_abilities(queen)
                    if AbilityId.EFFECT_INJECTLARVA in abilities:
                        available_queens.remove(queen)
                        await self.do(queen(EFFECT_INJECTLARVA, base))
                        print("injection")
                        break

    async def expand_mucus(self):
        """ Expands the mucus on the map as much as possible """
        # Choisir le meilleur endroit d'expend pour chaque tumeur(DL)
        # Choisir 1 ou 2 queens pour répendre le mucus
        # Si la tumeur est attaquée, cancel la capacité
        pass

    async def build_supply_unit(self):
        """ Creates the supply unit for this bot race (Overlord) if necessary """
        if self.supply_left < 2:
            if self.can_afford(OVERLORD) and self._larvae.exists:
                await self.do(self._larvae.random.train(OVERLORD))
                return

    async def drone_reassignation(self):
        """ Reassing drones from over-saturated bases to under-saturated bases """
        # Assigning unassigned drones to collecting
        for drone in self.units(DRONE):
            if drone.is_idle:
                drone.gather(self.state.mineral_field.closest_to(drone.position))
        return

    async def on_step(self, iteration):
        self._larvae = self.units(LARVA)

        # Recurrent behaviors
        await self.queens_injections()
        await self.expand_mucus()
        await self.build_supply_unit()
        await self.drone_reassignation()

        # Creating a loooooooot of drones
        for base in self.townhalls:
            if base.assigned_harvesters < base.ideal_harvesters:
                if self.can_afford(DRONE) and self._larvae.exists:
                    larva = self._larvae.random
                    await self.do(larva.train(DRONE))
                    print("created drone, having", len(self.units(DRONE)), "on", len(self.townhalls), "bases at", self.time_formatted, "with", self.minerals, "minerals, queens", len(self.units(QUEEN)))
                    return
        
        if not (self.units(SPAWNINGPOOL).exists or self.already_pending(SPAWNINGPOOL)):
            if self.can_afford(SPAWNINGPOOL):
                await self.build(SPAWNINGPOOL, near=self.townhalls.first)
                print("created spawning pool")

        #if self.state.resources.mineral > 300:
        if self.units(SPAWNINGPOOL).ready.exists and self.can_afford(QUEEN):
            base = self.townhalls.random
            if base.is_ready and base.noqueue:
                await self.do(base.train(QUEEN))
                print("created queen, having", len(self.units(QUEEN)))

        await self.expand_now()
        
def main():
    sc2.run_game(sc2.maps.get("BloodBoilLE"), [
        Bot(Race.Zerg, ShyZergling()),
        Computer(Race.Terran, Difficulty.Easy)
    ], realtime=False, save_replay_as="replays/ShyZerglingVSBot.SC2Replay")

if __name__ == '__main__':
    main()
        