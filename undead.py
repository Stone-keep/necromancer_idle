import math

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
    
    def buy(self):
        self.count += 1
        self.cost = math.ceil(self.cost * self.cost_multiplier)

    def recalculate_cost(self):
        new_cost = self.base_cost
        for _ in range(self.count):
            new_cost = math.ceil(new_cost * self.cost_multiplier)
        self.cost = new_cost
