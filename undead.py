import math
from game_logic import true_cost_multiplier

class Undead:
    def __init__(self, name, name_plural, count, cost, cost_multiplier, power, unlocked):
        self.name = name
        self.name_plural = name_plural
        self.count = count
        self.base_cost = cost
        self.cost = cost
        self.cost_multiplier = cost_multiplier
        self.power = power
        self.global_multiplier = 0
        self.unlocked = unlocked

    def passive_gain(self):
        return self.count * self.power
    
    def recalculate_cost(self):
        new_cost = self.base_cost
        multiplier = true_cost_multiplier(self)
        for _ in range(self.count):
            new_cost = math.ceil(new_cost * multiplier)
        self.cost = new_cost
    
    def buy(self):
        self.count += 1
    
