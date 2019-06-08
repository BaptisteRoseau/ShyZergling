import sc2
from sc2.data import race_townhalls
from sc2.player import BotAI
from sc2.constants import LARVA, DRONE, OVERLORD, QUEEN, CREEPTUMOR, SPAWNINGPOOL,\
    HATCHERY, EFFECT_INJECTLARVA, CANCEL, EXTRACTOR

# ShyZergling Class imported methods
from .expendCreep import expend_creep

#===========================================================#
#                      MAIN FUNCTION                        #
#===========================================================#

async def on_step(self, iteration):
    if iteration == 5:
        await self.chat_send("gl hf")
    self.larvae = self.units(LARVA)
    self.townhalls_ready  = self.townhalls.ready
    await self.debug(iteration) # Debug here
    await self.distribute_workers()
    await self.build_units()
    await self.extend_supply()
    await self.expend_creep()
    await self.expend_base()
    await self.injections()
    await self.cancel_building()
    await self.build_extractors()

#===========================================================#
#                      SUBFUNCTIONS                         #
#===========================================================#

async def debug(self, iteration):
    if iteration % 75 == 0:
        print("Debuging iteration", iteration, "at time "+self.time_formatted)
        print("Mineras / Vespene:", self.minerals, '/',self.vespene)
        print("Base amount:",  self.townhalls.amount)
        print("Drone amount:", self.units(DRONE).amount)
        print("Queen amount:", self.units(QUEEN).amount)
        print("Tumour amount:",self.units(CREEPTUMOR).amount)
        print()

async def injections(self):
    queens = self.units(QUEEN).idle
    if queens.exists:
        inj_queens = queens.filter(lambda q: q.energy > 25) #TODO: Find a less hardcoded way to do that
        if inj_queens.exists:
            for base in self.townhalls_ready:
                await self.do(inj_queens.closest_to(base)(EFFECT_INJECTLARVA, base))

async def build_units(self):
    # Drones
    need_harvesting = len(list(filter(lambda th: th.surplus_harvesters < 0, self.townhalls))) > 0
    if self.can_afford(DRONE) and self.larvae.exists and need_harvesting:
        await self.do(self.larvae.random.train(DRONE))

    # Queen and Spawningpool
    if self.units(SPAWNINGPOOL).ready.exists:
        for base in self.townhalls_ready:
            if self.can_afford(QUEEN) and base.noqueue:
                await self.do(base.train(QUEEN))
    elif not self.already_pending(SPAWNINGPOOL):
            if self.can_afford(SPAWNINGPOOL):
                await self.build(SPAWNINGPOOL, near=self.townhalls.first)

async def build_extractors(self):
    for base in self.townhalls_ready:
        vespenes = self.state.vespene_geyser.closer_than(15.0, base)
        for vespene in vespenes:
            if not self.can_afford(EXTRACTOR):
                break
            worker = self.select_build_worker(vespene.position)
            if worker is None:
                break
            if not self.units(EXTRACTOR).closer_than(1.0, vespene).exists:
                await self.do(worker.build(EXTRACTOR, vespene))

async def expend_base(self):
    if self.can_afford(HATCHERY):
          await self.expand_now()

async def extend_supply(self):
    if self.supply_left < 2:
        if self.can_afford(OVERLORD) and self.larvae.exists:
            await self.do(self.larvae.random.train(OVERLORD))

async def cancel_building(self):
    unfinished_buildings = self.units().not_ready
    for ub in unfinished_buildings:
        if ub.health_percentage < 0.95*ub.build_progress and ub.health_percentage < 0.05:
            await self.do(ub(CANCEL))