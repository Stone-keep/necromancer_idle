import math

class Undead:
    def __init__(self, name, count, cost, cost_multiplier, power):
        self.name = name
        self.count = count
        self.base_cost = cost
        self.cost = cost
        self.cost_multiplier = cost_multiplier
        self.power = power

    def passive_gain(self):
        return self.count * self.power
    
    def buy(self):
        self.count += 1
        self.cost = math.ceil(self.cost * self.cost_multiplier)
