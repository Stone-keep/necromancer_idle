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
skeleton = Undead("Skeleton", 0, 1, 1.3, 0.2)
zombie = Undead("Zombie", 0, 10, 1.3, 0.6)

# Upgrades
upgrades = [
{
    "id": 1,
    "name": "Upgrade #1",
    "cost": 20,
    "bought": False,
    "requirement": lambda: click_count >= 100,
    "effect_type": "click_power",
    "effect_value": 10,
    "description": "Gathering Souls (Clicks) become 10x more powerful"
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
    "cost": 300,
    "bought": False,
    "requirement": lambda: zombie.count >= 10,
    "effect_type": "zombie_power",
    "effect_value": 2,
    "description": "Double the Souls production of Zombies"
},
{
    "id": 4,
    "name": "Upgrade #4",
    "cost": 500,
    "bought": False,
    "requirement": lambda: total_souls_gained >= 1000,
    "effect_type": "souls_multiplier",
    "effect_value": 1.2,
    "description": "Increase the Souls production from all sources by 20%"
},
{
    "id": 5,
    "name": "Upgrade #5",
    "cost": 1000,
    "bought": False,
    "requirement": lambda: tick_count >= 200,
    "effect_type": "tick_rate",
    "effect_value": 0.9,
    "description": "Increase the global Tick Rate (everything becomes faster)"
}
]

upgrade_frames = {}