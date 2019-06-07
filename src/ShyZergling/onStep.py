import sc2
from sc2.data import race_townhalls
from sc2.constants import LARVA, DRONE, OVERLORD

# ShyZergling Class imported methods
from .expendCreep import expend_creep

#===========================================================#
#                      MAIN FUNCTION                        #
#===========================================================#

async def on_step(self, iteration):
    self.larvae = self.units(LARVA)
    self.distribute_workers()
    self.build_units()
    self.expend_creep()


#===========================================================#
#                      SUBFUNCTIONS                         #
#===========================================================#

async def build_units(self):
    if self.can_afford(DRONE) and self.larvae.exists:
        await self.do(self.larvae.random.train(DRONE))

async def extend_supply(self):
    if self.supply_left < 2:
        if self.can_afford(OVERLORD) and self.larvae.exists:
            await self.do(self.larvae.random.train(OVERLORD))