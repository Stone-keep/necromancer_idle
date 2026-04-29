from undead import Undead

# Variables
time_passed_seconds = 0
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

next_upgrade_row = 0

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
    "name": "Braaaains!",
    "cost": 200,
    "bought": False,
    "requirement": lambda: zombie.count >= 10,
    "effect_type": "zombie_power",
    "effect_value": 2,
    "description": "Zombies harvest 2x more Souls."
},
{
    "id": 4,
    "name": "Finger of Death",
    "cost": 150,
    "bought": False,
    "requirement": lambda: click_count >= 300,
    "effect_type": "click_power",
    "effect_value": 10,
    "description": "Gathering Souls (Clicking) is 10x more powerful."
},
{
    "id": 5,
    "name": "Soul Food",
    "cost": 600,
    "bought": False,
    "requirement": lambda: total_souls_gained >= 1500,
    "effect_type": "souls_multiplier",
    "effect_value": 1.4,
    "description": "Harvest 1.4x more Souls from all sources."
},
{
    "id": 6,
    "name": "Gotta Go Fast",
    "cost": 1000,
    "bought": False,
    "requirement": lambda: tick_count >= 200,
    "effect_type": "tick_rate",
    "effect_value": 0.85,
    "description": "Decreases the Tick Rate by 15% (everything becomes faster)."
},
{
    "id": 7,
    "name": "Bare-Bones Budget",
    "cost": 2000,
    "bought": False,
    "requirement": lambda: skeleton.count >= 20,
    "effect_type": "skeleton_cost_multiplier",
    "effect_value": 0.1,
    "description": "Reduces the cost scaling of Skeletons by 0.1."
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
    "name": "28 Souls Later",
    "cost": 5000,
    "bought": False,
    "requirement": lambda: zombie.count >= 20,
    "effect_type": "zombie_cost_multiplier",
    "effect_value": 0.1,
    "description": "Reduces the cost scaling of Zombies by 0.1."
},
{
    "id": 10,
    "name": "Resident Devil",
    "cost": 6666,
    "bought": False,
    "requirement": lambda: click_count >= 1200,
    "effect_type": "click_power",
    "effect_value": 6.66,
    "description": "Gathering Souls (Clicking) is 6.66x more powerful."
},
{
    "id": 11,
    "name": "Don't Dead\nOpen Inside",
    "cost": 10000,
    "bought": False,
    "requirement": lambda: zombie.count >= 30,
    "effect_type": "zombie_power",
    "effect_value": 3,
    "description": "Zombies harvest 3x more Souls."
},
{
    "id": 12,
    "name": "Bone Apple Tea",
    "cost": 15000,
    "bought": False,
    "requirement": lambda: skeleton.count >= 40,
    "effect_type": "skeleton_multiplier",
    "effect_value": 0.01,
    "description": "Each Skeleton increases Soul harvest of all Undead by 1%."
},
{
    "id": 13,
    "name": "Necroeconomics",
    "cost": 13000,
    "bought": False,
    "requirement": lambda: wraith.count >= 6,
    "effect_type": "wraith_per_zombie_scaling",
    "effect_value": 0.001,
    "description": "Each Zombie reduces the cost scaling of Wraiths by 0.001."
},
{
    "id": 14,
    "name": "Phantom Menace",
    "cost": 20000,
    "bought": False,
    "requirement": lambda: wraith.count >= 10,
    "effect_type": "wraith_power",
    "effect_value": 2,
    "description": "Wraiths harvest 2x more Souls."
},
{
    "id": 15,
    "name": "Thriller Night",
    "cost": 35000,
    "bought": False,
    "requirement": lambda: zombie.count >= 35,
    "effect_type": "skeleton_zombie_power",
    "effect_value": 2.5,
    "description": "Skeletons and Zombies harvest 2.5x more Souls."
},
{
    "id": 16,
    "name": "Click or Treat",
    "cost": 33000,
    "bought": False,
    "requirement": lambda: click_count >= 2000,
    "effect_type": "click_passive_scaling",
    "effect_value": 0.03,
    "description": "Gathering Souls now scales with passive Soul harvest (+3%)."
},
{
    "id": 17,
    "name": "Ghost In The Machine",
    "cost": 50000,
    "bought": False,
    "requirement": lambda: vampire.count >= 1,
    "effect_type": "wraith_multiplier",
    "effect_value": 0.02,
    "description": "Each Wraith increases Souls harvest of all Undead by 2%."
},
{
    "id": 18,
    "name": "Tick Tick Boom",
    "cost": 70000,
    "bought": False,
    "requirement": lambda: total_souls_spent >= 400_000,
    "effect_type": "souls_tick_multiplier",
    "effect_value": 0.002,
    "description": "Increases the Soul harvest by 0.2% per 10 game Ticks."
},
{
    "id": 19,
    "name": "Time Warp",
    "cost": 90000,
    "bought": False,
    "requirement": lambda: tick_count >= 1000,
    "effect_type": "tick_rate",
    "effect_value": 0.85,
    "description": "Decreases the Tick Rate by 15% (everything becomes faster)."
},
{
    "id": 20,
    "name": "Soul Survivor",
    "cost": 150_000,
    "bought": False,
    "requirement": lambda: total_souls_gained >= 1_000_000,
    "effect_type": "souls_multiplier",
    "effect_value": 1.4,
    "description": "Harvest 1.4x more Souls from all sources."
},
{
    "id": 21,
    "name": "Stakeholder Value",
    "cost": 300_000,
    "bought": False,
    "requirement": lambda: vampire.count >= 5,
    "effect_type": "skeletons_per_vampire_scaling",
    "effect_value": 0.004,
    "description": "Each Vampire reduces the cost scaling of Skeletons by 0.004."
},
{
    "id": 22,
    "name": "Spooky, Scary\nSkeletons",
    "cost": 500_000,
    "bought": False,
    "requirement": lambda: skeleton.count >= 60,
    "effect_type": "skeleton_power",
    "effect_value": 4,
    "description": "Skeletons harvest 4x more Souls."
},
{
    "id": 23,
    "name": "Graveyard Shift",
    "cost": 800_000,
    "bought": False,
    "requirement": lambda: wraith.count >= 25,
    "effect_type": "vampire_wraith_power",
    "effect_value": 1.5,
    "description": "Vampires and Wraiths harvest 1.5x more Souls."
},
{
    "id": 24,
    "name": "Count von Count",
    "cost": 2_000_000,
    "bought": False,
    "requirement": lambda: vampire.count >= 10,
    "effect_type": "vampire_tick_rate",
    "effect_value": 0.01,
    "description": "Each Vampire decreases the Tick Rate by 1% (multiplicative)."
},
{
    "id": 25,
    "name": "Monster Mash",
    "cost": 3_000_000,
    "bought": False,
    "requirement": lambda: lich.count >= 1,
    "effect_type": "lich_summoning",
    "effect_value": 1,
    "description": "Each Lich also raises a Skeleton and a Zombie."
},
{
    "id": 26,
    "name": "Got Red on You",
    "cost": 4_000_000,
    "bought": False,
    "requirement": lambda: zombie.count >= 60,
    "effect_type": "zombie_power",
    "effect_value": 3,
    "description": "Zombies harvest 3x more Souls."
},
{
    "id": 27,
    "name": "Hand of Glory",
    "cost": 5_000_000,
    "bought": False,
    "requirement": lambda: click_count >= 4500,
    "effect_type": "click_passive_scaling",
    "effect_value": 0.05,
    "description": "Gathering Souls further scales with passive Soul harvest (+5%)."
},
{
    "id": 28,
    "name": "Dragula",
    "cost": 10_000_000,
    "bought": False,
    "requirement": lambda: vampire.count >= 13,
    "effect_type": "vampire_and_lich_per_wraith_scaling",
    "effect_value": 0.002,
    "description": "Each Wraith reduces the cost scaling of Vampires and Liches by 0.002."
},
{
    "id": 29,
    "name": "Harvest Moon",
    "cost": 20_000_000,
    "bought": False,
    "requirement": lambda: total_souls_spent >= 80_000_000,
    "effect_type": "souls_gained_on_spend",
    "effect_value": 0.2,
    "description": "Harvest back 20% of the Souls you spend."
},
{
    "id": 30,
    "name": "Don't Fear\nThe Reaper",
    "cost": 35_000_000,
    "bought": False,
    "requirement": lambda: wraith.count >= 35,
    "effect_type": "lich_summoning_wraith",
    "effect_value": 1,
    "description": "Each Lich also raises a Wraith."
},
{
    "id": 31,
    "name": "Liches Get Riches",
    "cost": 60_000_000,
    "bought": False,
    "requirement": lambda: lich.count >= 10,
    "effect_type": "lich_multiplier",
    "effect_value": 0.04,
    "description": "Each Lich increases Soul harvest of all Undead by 4%."
},
{
    "id": 32,
    "name": "Bone to Be Wild",
    "cost": 100_000_000,
    "bought": False,
    "requirement": lambda: wraith.count >= 50,
    "effect_type": "skeleton_zombie_wraith_power",
    "effect_value": 3,
    "description": "Skeletons, Zombies and Wraiths harvest 3x more Souls."
},
{
    "id": 33,
    "name": "Final Countdown",
    "cost": 200_000_000,
    "bought": False,
    "requirement": lambda: total_souls_spent >= 500_000_000,
    "effect_type": "souls_tick_multiplier",
    "effect_value": 0.003,
    "description": "Increases the Soul harvest by 0.3% per 10 game Ticks."
},
]

upgrade_buttons = {}