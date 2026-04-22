import tkinter as tk
import math

# Game variables
tick_rate = 1000
tick_count = 0
souls = 0
souls_multiplier = 1
total_souls_gained = 0
total_souls_spent = 0
click_count = 0
click_power = 0.1
skeleton_count = 0
skeleton_cost = 1
skeleton_power = 0.1
zombie_count = 0
zombie_cost = 10
zombie_power = 0.5

# Upgrades
upgrades = [
{
    "id": 1,
    "name": "Upgrade #1",
    "cost": 20,
    "bought": False,
    "requirement": lambda: click_count >= 100,
    "effect_type": "click_power",
    "effect_value": 10
},
{
    "id": 2,
    "name": "Upgrade #2",
    "cost": 50,
    "bought": False,
    "requirement": lambda: skeleton_count >= 10,
    "effect_type": "skeleton_power",
    "effect_value": 2
},
{
    "id": 3,
    "name": "Upgrade #3",
    "cost": 300,
    "bought": False,
    "requirement": lambda: zombie_count >= 10,
    "effect_type": "zombie_power",
    "effect_value": 2
},
{
    "id": 4,
    "name": "Upgrade #4",
    "cost": 500,
    "bought": False,
    "requirement": lambda: total_souls_gained >= 1000,
    "effect_type": "souls_multiplier",
    "effect_value": 1.2
},
{
    "id": 5,
    "name": "Upgrade #5",
    "cost": 1000,
    "bought": False,
    "requirement": lambda: tick_count >= 300,
    "effect_type": "tick_rate",
    "effect_value": 0.9
}
]


# Functions
def game_loop():
    global tick_count
    tick_count += 1
    passive_gain = (skeleton_count * skeleton_power) + (zombie_count * zombie_power)
    gain_souls(passive_gain)
    update_ui()
    print(get_available_upgrades(upgrades))
    root.after(tick_rate, game_loop)

def update_ui():
    souls_label.config(text=f"Souls: {souls:.1f}")
    skeletons_label.config(text=f"Skeletons: {skeleton_count}")
    zombies_label.config(text=f"Zombies: {zombie_count}")
    buy_skeleton_button.config(text=f"Buy Skeleton (Cost: {skeleton_cost})")
    buy_zombie_button.config(text=f"Buy Zombie (Cost: {zombie_cost})")
    update_button_state(buy_zombie_button, zombie_cost)
    update_button_state(buy_skeleton_button, skeleton_cost)

def update_button_state(button, cost):
    if souls >= cost:
        button.config(state="normal")
    else:
        button.config(state="disabled")

def is_upgrade_unlocked(upgrade):
    return upgrade["requirement"]()

def get_available_upgrades(upgrades):
    available_upgrades = []
    for upgrade in upgrades:
        if is_upgrade_unlocked(upgrade) and upgrade["bought"] == False:
            available_upgrades.append(upgrade)
    return available_upgrades

def gain_souls(amount):
    global souls, total_souls_gained
    souls = round(souls + (amount * souls_multiplier), 1)
    total_souls_gained = round(total_souls_gained + (amount * souls_multiplier), 1)

def spend_souls(cost):
    global souls, total_souls_spent
    souls = round(souls - cost, 1)
    total_souls_spent = round(total_souls_spent + cost, 1)

def collect_soul_click():
    global click_count
    click_count += 1
    gain_souls(click_power)
    update_ui()

def buy_skeleton():
    global skeleton_cost, skeleton_count
    if souls >= skeleton_cost:
        spend_souls(skeleton_cost)
        skeleton_count += 1
        skeleton_cost = math.ceil(skeleton_cost * 1.5)
        update_ui()
       
def buy_zombie():
    global zombie_cost, zombie_count
    if souls >= zombie_cost:
        spend_souls(zombie_cost)
        zombie_count += 1
        zombie_cost = math.ceil(zombie_cost * 1.5)
        update_ui()

# UI
root = tk.Tk()
root.title("Necromancer Idle")
root.geometry("500x800")

souls_label = tk.Label(root, text="Souls: 0", font=("Arial", 16))
souls_label.pack(pady=20)

skeletons_label = tk.Label(root, text="Skeletons: 0", font=("Arial", 16))
skeletons_label.pack(pady=20)

zombies_label = tk.Label(root, text="Zombies: 0", font=("Arial", 16))
zombies_label.pack(pady=20)

collect_button = tk.Button(root, text="Collect Soul", command=collect_soul_click)
collect_button.pack()

buy_skeleton_button = tk.Button(root, text="Buy Skeleton (Cost: 1)", command=buy_skeleton, state="disabled")
buy_skeleton_button.pack()

buy_zombie_button = tk.Button(root, text="Buy Zombie (Cost: 10)", command=buy_zombie, state="disabled")
buy_zombie_button.pack()

update_ui()
game_loop()
root.mainloop()