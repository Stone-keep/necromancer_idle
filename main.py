import tkinter as tk
from tkinter import ttk
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

upgrade_buttons = {}

# Functions
def game_loop():
    global tick_count
    tick_count += 1
    passive_gain = total_passive_gain()
    gain_souls(passive_gain)
    update_ui()
    root.after(tick_rate, game_loop)

def update_ui():
    souls_label.config(text=f"Souls: {souls:.1f}")
    souls_passive.config(text=f"({total_passive_gain() * (1000 / tick_rate):.1f}/s)")
    skeletons_label.config(text=f"Skeletons: {skeleton_count} ({undead_passive_gain(skeleton_count, skeleton_power) * (1000 / tick_rate):.1f}/s)")
    zombies_label.config(text=f"Zombies: {zombie_count} ({undead_passive_gain(zombie_count, zombie_power) * (1000 / tick_rate):.1f}/s)")
    buy_skeleton_button.config(text=f"Buy Skeleton (Cost: {skeleton_cost})")
    buy_zombie_button.config(text=f"Buy Zombie (Cost: {zombie_cost})")
    update_button_state(buy_zombie_button, zombie_cost)
    update_button_state(buy_skeleton_button, skeleton_cost)
    create_upgrade_buttons()

def create_upgrade_buttons():
    available_upgrades = get_available_upgrades()
    for upgrade in available_upgrades:
        upgrade_id = upgrade["id"]
        name = upgrade["name"]
        cost = upgrade["cost"]
        if upgrade_id in upgrade_buttons:
            update_button_state(upgrade_buttons[upgrade_id], cost)
            continue
        upgrade_buttons[upgrade_id] = tk.Button(upgrades_tab, text=f"{name} (Cost: {cost})", command=lambda current_upgrade = upgrade: buy_upgrade(current_upgrade), state="disabled")
        upgrade_buttons[upgrade_id].pack()
        update_button_state(upgrade_buttons[upgrade_id], cost)

def update_button_state(button, cost):
    if souls >= cost:
        button.config(state="normal")
    else:
        button.config(state="disabled")

def is_upgrade_unlocked(upgrade):
    return upgrade["requirement"]()

def get_available_upgrades():
    global upgrades
    available_upgrades = []
    for upgrade in upgrades:
        if is_upgrade_unlocked(upgrade) and not upgrade["bought"]:
            available_upgrades.append(upgrade)
    return available_upgrades

def can_buy_upgrade(upgrade):
    return is_upgrade_unlocked(upgrade) and souls >= upgrade["cost"] and not upgrade["bought"]

def apply_upgrade_effect(upgrade):
    global click_power, skeleton_power, zombie_power, souls_multiplier, tick_rate
    if upgrade["effect_type"] == "click_power":
        click_power *= upgrade["effect_value"]
    elif upgrade["effect_type"] == "skeleton_power":
        skeleton_power *= upgrade["effect_value"]
    elif upgrade["effect_type"] == "zombie_power":
        zombie_power *= upgrade["effect_value"]
    elif upgrade["effect_type"] == "souls_multiplier":
        souls_multiplier *= upgrade["effect_value"]
    elif upgrade["effect_type"] == "tick_rate":
        tick_rate = int(tick_rate * upgrade["effect_value"])
    else:
        raise ValueError("Upgrade effect type not found")

def buy_upgrade(upgrade):
    if can_buy_upgrade(upgrade):
        spend_souls(upgrade["cost"])
        upgrade["bought"] = True
        apply_upgrade_effect(upgrade)
        upgrade_id = upgrade["id"]
        if upgrade_id in upgrade_buttons:
            upgrade_buttons[upgrade_id].destroy()
            upgrade_buttons.pop(upgrade_id)
        update_ui()

def undead_passive_gain(undead_count, undead_power):
    return undead_count * undead_power * souls_multiplier

def total_passive_gain():
    return undead_passive_gain(skeleton_count, skeleton_power) + undead_passive_gain(zombie_count, zombie_power)
    
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
        skeleton_cost = math.ceil(skeleton_cost * 1.3)
        update_ui()
       
def buy_zombie():
    global zombie_cost, zombie_count
    if souls >= zombie_cost:
        spend_souls(zombie_cost)
        zombie_count += 1
        zombie_cost = math.ceil(zombie_cost * 1.3)
        update_ui()

# UI
root = tk.Tk()
root.title("Necromancer Idle")
root.geometry("500x800")

status_frame = tk.Frame(root)
status_frame.pack()

souls_label = tk.Label(status_frame, text="Souls: 0", font=("Arial", 16))
souls_label.pack(pady=20)

souls_passive = tk.Label(status_frame, text="(0/s)", font=("Arial", 16))
souls_passive.pack(pady=20)

skeletons_label = tk.Label(status_frame, text="Skeletons: 0", font=("Arial", 12))
skeletons_label.pack(pady=20)

zombies_label = tk.Label(status_frame, text="Zombies: 0", font=("Arial", 12))
zombies_label.pack(pady=20)

collect_button = tk.Button(status_frame, text="Collect Soul", command=collect_soul_click)
collect_button.pack()

notebook = ttk.Notebook(root)
notebook.pack()

undead_tab = tk.Frame(notebook)
upgrades_tab = tk.Frame(notebook)

notebook.add(undead_tab, text="Undead")
notebook.add(upgrades_tab, text="Upgrades")

buy_skeleton_button = tk.Button(undead_tab, text="Buy Skeleton (Cost: 1)", command=buy_skeleton, state="disabled")
buy_skeleton_button.pack()

buy_zombie_button = tk.Button(undead_tab, text="Buy Zombie (Cost: 10)", command=buy_zombie, state="disabled")
buy_zombie_button.pack()



update_ui()
game_loop()
root.mainloop()