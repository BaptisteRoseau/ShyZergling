import sc2
from sc2 import Race, Difficulty
from sc2.player import Bot, Computer

from ShyZergling import ShyZergling

def main():
    sc2.run_game(sc2.maps.get("CatalystLE"), [
        Bot(Race.Zerg, ShyZergling()),
        Computer(Race.Terran, Difficulty.Easy)
    ], realtime=False, save_replay_as="ZvT.SC2Replay")

if __name__ == '__main__':
    main()
