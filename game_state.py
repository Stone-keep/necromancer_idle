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
skeletons_per_vampire_scaling = 0
vampire_and_lich_per_wraith_scaling = 0
vampire_tick_rate = 0
lich_summoning = 0
lich_summoning_wraith = 0
souls_gained_on_spend = 0

undead_king_unlocked = False
victory_achieved = False
game_paused = False

#Undead
skeleton = Undead("Skeleton", "Skeletons", 0, 1, 1.3, 0.2, True)
zombie = Undead("Zombie", "Zombies", 0, 10, 1.3, 0.6, True)
wraith = Undead("Wraith", "Wraiths", 0, 1000, 1.3, 10, True)
vampire = Undead("Vampire", "Vampires", 0, 50000, 1.3, 100, False)
lich = Undead("Lich", "Liches", 0, 1000000, 1.3, 500, False)

undead_list = [skeleton, zombie, wraith, vampire, lich]

# Upgrades
upgrades = [
{
    "id": 1,
    "name": "Warming Up",
    "cost": 20,
    "bought": False,
    "requirement": lambda: click_count >= 100,
    "effect_type": "click_power",
    "effect_value": 5,
    "description": "Gathering Souls (Clicking) becomes 5x more powerful."
},
{
    "id": 2,
    "name": "More Calcium",
    "cost": 50,
    "bought": False,
    "requirement": lambda: skeleton.count >= 10,
    "effect_type": "skeleton_power",
    "effect_value": 2,
    "description": "Skeletons harvest 2x more Souls."
},
{
    "id": 3,
    "name": "Don't Dead Open Inside",
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
    "effect_value": 1.4,
    "description": "Harvest 1.4x more Souls from all sources."
},
{
    "id": 6,
    "name": "Upgrade #6",
    "cost": 1000,
    "bought": False,
    "requirement": lambda: tick_count >= 240,
    "effect_type": "tick_rate",
    "effect_value": 0.8,
    "description": "Decreases the Tick Rate by 20% (everything becomes faster)."
},
{
    "id": 7,
    "name": "Good Bones",
    "cost": 2000,
    "bought": False,
    "requirement": lambda: skeleton.count >= 20,
    "effect_type": "skeleton_cost_multiplier",
    "effect_value": 0.1,
    "description": "Reduces the cost scaling of Skeletons by 0.1"
},
{
    "id": 8,
    "name": "Doot Doot",
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
    "description": "Reduces the cost scaling of Zombies by 0.1."
},
{
    "id": 10,
    "name": "Upgrade #10",
    "cost": 6666,
    "bought": False,
    "requirement": lambda: click_count >= 1300,
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
    "effect_value": 0.01,
    "description": "Each Skeleton increases Souls harvest of all Undead by 1%."
},
{
    "id": 13,
    "name": "Upgrade #13",
    "cost": 13000,
    "bought": False,
    "requirement": lambda: wraith.count >= 5,
    "effect_type": "wraith_per_zombie_scaling",
    "effect_value": 0.001,
    "description": "Each Zombie reduces the cost scaling of Wraiths by 0.001."
},
{
    "id": 14,
    "name": "Upgrade #14",
    "cost": 20000,
    "bought": False,
    "requirement": lambda: wraith.count >= 10,
    "effect_type": "wraith_power",
    "effect_value": 2,
    "description": "Wraiths harvest 2x more Souls."
},
{
    "id": 15,
    "name": "Upgrade #15",
    "cost": 28000,
    "bought": False,
    "requirement": lambda: zombie.count >= 35,
    "effect_type": "skeleton_zombie_power",
    "effect_value": 2.5,
    "description": "Skeletons and Zombies harvest 2.5x more Souls."
},
{
    "id": 16,
    "name": "Upgrade #16",
    "cost": 33000,
    "bought": False,
    "requirement": lambda: click_count >= 2000,
    "effect_type": "click_passive_scaling",
    "effect_value": 0.03,
    "description": "Gathering Souls now scales with passive Souls harvest (+3%)."
},
{
    "id": 17,
    "name": "Upgrade #17",
    "cost": 50000,
    "bought": False,
    "requirement": lambda: wraith.count >= 15,
    "effect_type": "wraith_multiplier",
    "effect_value": 0.02,
    "description": "Each Wraith increases Souls harvest of all Undead by 2%"
},
{
    "id": 18,
    "name": "Upgrade #18",
    "cost": 66666,
    "bought": False,
    "requirement": lambda: total_souls_spent >= 600_000,
    "effect_type": "souls_tick_multiplier",
    "effect_value": 0.002,
    "description": "Increases the Souls harvest by 0.2% per 10 game Ticks"
},
{
    "id": 19,
    "name": "Upgrade #19",
    "cost": 91100,
    "bought": False,
    "requirement": lambda: tick_count >= 1200,
    "effect_type": "tick_rate",
    "effect_value": 0.9,
    "description": "Decreases the Tick Rate by 10% (everything becomes faster)."
},
{
    "id": 20,
    "name": "Upgrade #20",
    "cost": 150_000,
    "bought": False,
    "requirement": lambda: total_souls_gained >= 1_200_000,
    "effect_type": "souls_multiplier",
    "effect_value": 1.4,
    "description": "Harvest 1.4x more Souls from all sources."
},
{
    "id": 21,
    "name": "Upgrade #20",
    "cost": 300_000,
    "bought": False,
    "requirement": lambda: vampire.count >= 5,
    "effect_type": "skeletons_per_vampire_scaling",
    "effect_value": 0.005,
    "description": "Each Vampire reduces the Cost scaling of Skeletons by 0.005."
},
{
    "id": 22,
    "name": "Upgrade #21",
    "cost": 400_000,
    "bought": False,
    "requirement": lambda: skeleton.count >= 60,
    "effect_type": "skeleton_power",
    "effect_value": 4,
    "description": "Skeletons harvest 4x more Souls."
},
{
    "id": 23,
    "name": "Upgrade #22",
    "cost": 800_000,
    "bought": False,
    "requirement": lambda: wraith.count >= 25,
    "effect_type": "vampire_wraith_power",
    "effect_value": 1.5,
    "description": "Vampires and Wraiths harvest 1.5x more Souls."
},
{
    "id": 24,
    "name": "Upgrade #23",
    "cost": 1_500_000,
    "bought": False,
    "requirement": lambda: vampire.count >= 10,
    "effect_type": "vampire_tick_rate",
    "effect_value": 0.01,
    "description": "Each Vampire decreases the Tick Rate by 1%."
},
{
    "id": 25,
    "name": "Upgrade #24",
    "cost": 2_500_000,
    "bought": False,
    "requirement": lambda: lich.count >= 1,
    "effect_type": "lich_summoning",
    "effect_value": 1,
    "description": "Each Lich raises a Skeleton and a Zombie."
},
{
    "id": 26,
    "name": "Upgrade #24",
    "cost": 3_000_000,
    "bought": False,
    "requirement": lambda: zombie.count >= 60,
    "effect_type": "zombie_power",
    "effect_value": 3,
    "description": "Zombies harvest 3x more Souls."
},
{
    "id": 27,
    "name": "Upgrade #25",
    "cost": 5_000_000,
    "bought": False,
    "requirement": lambda: click_count >= 4000,
    "effect_type": "click_passive_scaling",
    "effect_value": 0.05,
    "description": "Gathering Souls further scales with passive Souls harvest (+5%)."
},
{
    "id": 28,
    "name": "Upgrade #26",
    "cost": 10_000_000,
    "bought": False,
    "requirement": lambda: wraith.count >= 35,
    "effect_type": "vampire_and_lich_per_wraith_scaling",
    "effect_value": 0.002,
    "description": "Each Wraith reduces the Cost scaling of Vampires and Liches by 0.002."
},
{
    "id": 29,
    "name": "Upgrade #27",
    "cost": 20_000_000,
    "bought": False,
    "requirement": lambda: total_souls_spent >= 80_000_000,
    "effect_type": "souls_gained_on_spend",
    "effect_value": 0.2,
    "description": "Harvest back 20% of the Souls you spend."
},
{
    "id": 30,
    "name": "Upgrade #27",
    "cost": 40_000_000,
    "bought": False,
    "requirement": lambda: wraith.count >= 40,
    "effect_type": "lich_summoning_wraith",
    "effect_value": 1,
    "description": "Each Lich also raises a Wraith."
},
{
    "id": 31,
    "name": "Upgrade #28",
    "cost": 60_000_000,
    "bought": False,
    "requirement": lambda: lich.count >= 10,
    "effect_type": "lich_multiplier",
    "effect_value": 0.04,
    "description": "Each Lich increases Souls harvest of all Undead by 4%."
},
{
    "id": 32,
    "name": "Upgrade #29",
    "cost": 100_000_000,
    "bought": False,
    "requirement": lambda: wraith.count >= 50,
    "effect_type": "skeleton_wraith_power",
    "effect_value": 2,
    "description": "Skeletons and Wraiths harvest 2x more Souls."
},
{
    "id": 33,
    "name": "Final Countdown",
    "cost": 200_000_000,
    "bought": False,
    "requirement": lambda: total_souls_spent >= 500_000_000,
    "effect_type": "souls_tick_multiplier",
    "effect_value": 0.003,
    "description": "Increases the Souls harvest by 0.3% per 10 game Ticks."
},
]

upgrade_buttons = {}