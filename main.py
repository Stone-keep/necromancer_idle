import tkinter as tk
import math

# Game variables
souls = 0
skeleton_count = 0
skeleton_cost = 1
zombie_count = 0
zombie_cost = 10

# Functions
def game_loop():
    global souls
    souls = round(souls + (skeleton_count * 0.1) + (zombie_count * 0.5), 1)
    update_ui()

    root.after(1000, game_loop)

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

def collect_soul():
    global souls
    souls = round(souls + 0.1, 1)
    update_ui()

def buy_skeleton():
    global souls, skeleton_cost, skeleton_count
    if souls >= skeleton_cost:
        souls = round(souls - skeleton_cost, 1)
        skeleton_count += 1
        skeleton_cost = math.ceil(skeleton_cost * 1.5)
        update_ui()

def buy_zombie():
    global souls, zombie_cost, zombie_count
    if souls >= zombie_cost:
        souls = round(souls - zombie_cost, 1)
        zombie_count += 1
        zombie_cost = math.ceil(zombie_cost * 1.5)
        update_ui()

# UI setup
root = tk.Tk()
root.title("Necromancer Idle")
root.geometry("500x800")

souls_label = tk.Label(root, text="Souls: 0", font=("Arial", 16))
souls_label.pack(pady=20)

skeletons_label = tk.Label(root, text="Skeletons: 0", font=("Arial", 16))
skeletons_label.pack(pady=20)

zombies_label = tk.Label(root, text="Zombies: 0", font=("Arial", 16))
zombies_label.pack(pady=20)

collect_button = tk.Button(root, text="Collect Soul", command=collect_soul)
collect_button.pack()

buy_skeleton_button = tk.Button(root, text="Buy Skeleton (Cost: 1)", command=buy_skeleton, state="disabled")
buy_skeleton_button.pack()

buy_zombie_button = tk.Button(root, text="Buy Zombie (Cost: 10)", command=buy_zombie, state="disabled")
buy_zombie_button.pack()

update_ui()
game_loop()
root.mainloop()