from undead import Undead

# Variables
tick_rate = 1000
tick_count = 0
souls = 0
souls_multiplier = 1
souls_tick_multiplier = 0
total_souls_gained = 0
total_souls_spent = 0
click_count = 0
click_power = 0.1
click_passive_scaling = 0
wraith_per_zombie_scaling = 0

#Undead
skeleton = Undead("Skeleton", "Skeletons", 0, 1, 1.3, 0.2, True)
zombie = Undead("Zombie", "Zombies", 0, 10, 1.3, 0.6, True)
wraith = Undead("Wraith", "Wraiths", 0, 1000, 1.3, 10, True)
vampire = Undead("Vampire", "Vampires", 0, 50000, 1.3, 100, False)
lich = Undead("Lich", "Liches", 0, 1000000, 1.3, 10000, False)

undead_list = [skeleton, zombie, wraith, vampire, lich]

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
    "description": "Gathering Souls (Clicking) becomes 5x more powerful."
},
{
    "id": 2,
    "name": "Upgrade #2",
    "cost": 50,
    "bought": False,
    "requirement": lambda: skeleton.count >= 10,
    "effect_type": "skeleton_power",
    "effect_value": 2,
    "description": "Skeletons harvest 2x more Souls."
},
{
    "id": 3,
    "name": "Upgrade #3",
    "cost": 200,
    "bought": False,
    "requirement": lambda: zombie.count >= 10,
    "effect_type": "zombie_power",
    "effect_value": 2,
    "description": "Zombies harvest 2x more Souls."
},
{
    "id": 4,
    "name": "Upgrade #4",
    "cost": 250,
    "bought": False,
    "requirement": lambda: click_count >= 250,
    "effect_type": "click_power",
    "effect_value": 10,
    "description": "Gathering Souls (Clicking) is 10x more powerful."
},
{
    "id": 5,
    "name": "Upgrade #5",
    "cost": 500,
    "bought": False,
    "requirement": lambda: total_souls_gained >= 1000,
    "effect_type": "souls_multiplier",
    "effect_value": 1.5,
    "description": "Harvest 1.5x more Souls from all sources."
},
{
    "id": 6,
    "name": "Upgrade #6",
    "cost": 1000,
    "bought": False,
    "requirement": lambda: tick_count >= 240,
    "effect_type": "tick_rate",
    "effect_value": 0.8,
    "description": "Decreases the Tick Rate by 20% (everything becomes faster!)"
},
{
    "id": 7,
    "name": "Upgrade #7",
    "cost": 2000,
    "bought": False,
    "requirement": lambda: skeleton.count >= 20,
    "effect_type": "skeleton_cost_multiplier",
    "effect_value": 0.1,
    "description": "Reduces the cost scaling of Skeletons by 0.1 (retroactive!)"
},
{
    "id": 8,
    "name": "Upgrade #8",
    "cost": 3000,
    "bought": False,
    "requirement": lambda: skeleton.count >= 30,
    "effect_type": "skeleton_power",
    "effect_value": 3,
    "description": "Skeletons harvest 3x more Souls."
},
{
    "id": 9,
    "name": "Upgrade #9",
    "cost": 4000,
    "bought": False,
    "requirement": lambda: zombie.count >= 20,
    "effect_type": "zombie_cost_multiplier",
    "effect_value": 0.1,
    "description": "Reduces the cost scaling of Zombies by 0.1 (retroactive!)"
},
{
    "id": 10,
    "name": "Upgrade #10",
    "cost": 6666,
    "bought": False,
    "requirement": lambda: click_count >= 1000,
    "effect_type": "click_power",
    "effect_value": 6.66,
    "description": "Gathering Souls (Clicking) is 6.66x more powerful."
},
{
    "id": 11,
    "name": "Upgrade #11",
    "cost": 8000,
    "bought": False,
    "requirement": lambda: zombie.count >= 30,
    "effect_type": "zombie_power",
    "effect_value": 3,
    "description": "Zombies harvest 3x more Souls."
},
{
    "id": 12,
    "name": "Upgrade #12",
    "cost": 11111,
    "bought": False,
    "requirement": lambda: skeleton.count >= 40,
    "effect_type": "skeleton_multiplier",
    "effect_value": 0.02,
    "description": "Each Skeleton increases Souls harvest of all Undead by 2%"
},
{
    "id": 13,
    "name": "Upgrade #13",
    "cost": 15000,
    "bought": False,
    "requirement": lambda: wraith.count >= 5,
    "effect_type": "wraith_per_zombie_scaling",
    "effect_value": 0.001,
    "description": "Each Zombie reduces the cost scaling of Wraiths by 0.001 (retroactive!)"
},
{
    "id": 14,
    "name": "Upgrade #14",
    "cost": 20000,
    "bought": False,
    "requirement": lambda: wraith.count >= 10,
    "effect_type": "wraith_power",
    "effect_value": 3,
    "description": "Wraiths Harvest 3x more Souls"
},
{
    "id": 15,
    "name": "Upgrade #15",
    "cost": 28000,
    "bought": False,
    "requirement": lambda: zombie.count >= 40,
    "effect_type": "skeleton_zombie_power",
    "effect_value": 2.5,
    "description": "Skeletons and Zombies harvest 2.5x more Souls"
},
{
    "id": 16,
    "name": "Upgrade #16",
    "cost": 33000,
    "bought": False,
    "requirement": lambda: click_count >= 1500,
    "effect_type": "click_passive_scaling",
    "effect_value": 0.02,
    "description": "Gathering Souls now scales with passive Souls harvest (2%)"
},
{
    "id": 17,
    "name": "Upgrade #17",
    "cost": 50000,
    "bought": False,
    "requirement": lambda: wraith.count >= 15,
    "effect_type": "wraith_multiplier",
    "effect_value": 0.05,
    "description": "Each Wraith increases Souls harvest of all Undead by 5%"
},
{
    "id": 18,
    "name": "Upgrade #18",
    "cost": 66666,
    "bought": False,
    "requirement": lambda: total_souls_spent >= 300000,
    "effect_type": "souls_tick_multiplier",
    "effect_value": 0.01,
    "description": "Increases the Souls harvest by 1% per 10 game Ticks"
},
{
    "id": 19,
    "name": "Upgrade #19",
    "cost": 91100,
    "bought": False,
    "requirement": lambda: tick_count >= 1200,
    "effect_type": "tick_rate",
    "effect_value": 0.8,
    "description": "Decreases the Tick Rate by 20% (everything becomes faster!)"
},
]

upgrade_frames = {}