from undead import Undead

# Variables
tick_rate = 1000
tick_count = 0
souls = 0
souls_multiplier = 1
total_souls_gained = 0
total_souls_spent = 0
click_count = 0
click_power = 0.1

#Undead
skeleton = Undead("Skeleton", "Skeletons", 0, 1, 1.3, 0.2, True)
zombie = Undead("Zombie", "Zombies", 0, 10, 1.3, 0.6, True)
wraith = Undead("Wraith", "Wraiths", 0, 1000, 1.3, 10, True)
vampire = Undead("Vampire", "Vampires", 0, 100000, 1.3, 1000, False)

undead_list = [skeleton, zombie, wraith, vampire]

# Upgrades
upgrades = [
{
    "id": 1,
    "name": "Upgrade #1",
    "cost": 20,
    "bought": False,
    "requirement": lambda: click_count >= 100,
    "effect_type": "click_power",
    "effect_value": 5,
    "description": "Gathering Souls (Clicking) becomes 5x more powerful"
},
{
    "id": 2,
    "name": "Upgrade #2",
    "cost": 50,
    "bought": False,
    "requirement": lambda: skeleton.count >= 10,
    "effect_type": "skeleton_power",
    "effect_value": 2,
    "description": "Double the Souls production of Skeletons"
},
{
    "id": 3,
    "name": "Upgrade #3",
    "cost": 200,
    "bought": False,
    "requirement": lambda: zombie.count >= 10,
    "effect_type": "zombie_power",
    "effect_value": 2,
    "description": "Double the Souls production of Zombies"
},
{
    "id": 4,
    "name": "Upgrade #4",
    "cost": 250,
    "bought": False,
    "requirement": lambda: click_count >= 250,
    "effect_type": "click_power",
    "effect_value": 10,
    "description": "Gathering Souls (Clicking) becomes 10x more powerful"
},
{
    "id": 5,
    "name": "Upgrade #5",
    "cost": 500,
    "bought": False,
    "requirement": lambda: total_souls_gained >= 1000,
    "effect_type": "souls_multiplier",
    "effect_value": 1.5,
    "description": "Increase the Souls production from all sources by 1.5x"
},
{
    "id": 6,
    "name": "Upgrade #6",
    "cost": 1000,
    "bought": False,
    "requirement": lambda: tick_count >= 240,
    "effect_type": "tick_rate",
    "effect_value": 0.9,
    "description": "Increase the global Tick Rate (everything becomes faster)"
},
{
    "id": 7,
    "name": "Upgrade #7",
    "cost": 2000,
    "bought": False,
    "requirement": lambda: skeleton.count >= 20,
    "effect_type": "skeleton_cost_multiplier",
    "effect_value": 1.2,
    "description": "Reduces the cost multiplier of Skeletons to 1.2x (retroactive!)"
},
{
    "id": 8,
    "name": "Upgrade #8",
    "cost": 3000,
    "bought": False,
    "requirement": lambda: skeleton.count >= 30,
    "effect_type": "skeleton_power",
    "effect_value": 3,
    "description": "Triple the Souls production of Skeletons"
},
{
    "id": 9,
    "name": "Upgrade #9",
    "cost": 4000,
    "bought": False,
    "requirement": lambda: zombie.count >= 20,
    "effect_type": "zombie_cost_multiplier",
    "effect_value": 1.2,
    "description": "Reduces the cost multiplier of Zombies to 1.2x (retroactive!)"
},
{
    "id": 10,
    "name": "Upgrade #10",
    "cost": 6666,
    "bought": False,
    "requirement": lambda: click_count >= 1000,
    "effect_type": "click_power",
    "effect_value": 6.66,
    "description": "Gathering Souls (Clicking) becomes 6.66x more powerful"
},
{
    "id": 11,
    "name": "Upgrade #11",
    "cost": 8000,
    "bought": False,
    "requirement": lambda: zombie.count >= 30,
    "effect_type": "zombie_power",
    "effect_value": 3,
    "description": "Triple the Souls production of Zombies"
},
{
    "id": 12,
    "name": "Upgrade #12",
    "cost": 10000,
    "bought": False,
    "requirement": lambda: skeleton.count >= 40,
    "effect_type": "skeleton_multiplier",
    "effect_value": 0.02,
    "description": "Each Skeleton increases all Undead production by 2%"
},
{
    "id": 13,
    "name": "Upgrade #13",
    "cost": 20000,
    "bought": False,
    "requirement": lambda: wraith.count >= 10,
    "effect_type": "wraith_power",
    "effect_value": 3,
    "description": "Triple the Souls production of Wraiths"
},
]

upgrade_frames = {}