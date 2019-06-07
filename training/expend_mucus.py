
def main():
    sc2.run_game(sc2.maps.get("AscensiontoAiurLE.SC2Map"), [
        Bot(Race.Zerg, ShyZergling()),
        Computer(Race.Terran, Difficulty.Medium)
    ], realtime=False, save_replay_as="expend_mucus.SC2Replay")

if __name__ == '__main__':
    main()
