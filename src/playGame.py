import sc2
from sc2 import Race, Difficulty
from sc2.player import Bot, Computer

from ShyZergling import ShyZergling
from emptyBot import EmptyBot

import random

maps = [
    "AbiogenesisLE",
    "AbyssalReefLE",
    "AcidPlantLE",
    "AcolyteLE",
    "AscensiontoAiurLE",
    "AutomatonLE",
    "BackwaterLE",
    "BattleontheBoardwalkLE",
    "BlackpinkLE",
    "BloodBoilLE",
    "CatalystLE",
    "CyberForestLE",
    "DefendersLandingLE",
    "EastwatchLE",
    "FrostLE",
    "InterloperLE",
    "KairosJunctionLE",
    "KingsCoveLE",
    "MechDepotLE",
    "mini_games",
    "NeonVioletSquareLE",
    "NewRepugnancyLE",
    "OdysseyLE",
    "PortAleksanderLE",
    "ProximaStationLE",
    "SequencerLE",
    "YearZeroLE"
]

def main():
    sc2.run_game(sc2.maps.get(maps[random.randint(0, len(maps) - 1)]), [
        Bot(Race.Zerg, ShyZergling()),
        Computer(Race.Terran, Difficulty.Easy)
    ], realtime=False, save_replay_as="ZvT.SC2Replay")

if __name__ == '__main__':
    main()
