import tkinter as tk
from tkinter import ttk
import game_state, game_logic

def game_loop():
    game_state.tick_count += 1
    passive_gain = game_logic.total_passive_gain()
    game_logic.gain_souls(passive_gain)
    update_ui()
    root.after(game_state.tick_rate, game_loop)

def update_ui():
    # Game Status Labels
    souls_label.config(text=f"Souls: {game_state.souls:.1f}")
    souls_passive.config(text=f"({game_logic.total_passive_gain() * (1000 / game_state.tick_rate) * game_state.souls_multiplier:.1f}/s)")
    skeletons_label.config(text=f"Skeletons: {game_state.skeleton_count} ({game_logic.undead_passive_gain(game_state.skeleton_count, game_state.skeleton_power) * (1000 / game_state.tick_rate) * game_state.souls_multiplier:.1f}/s)")
    zombies_label.config(text=f"Zombies: {game_state.zombie_count} ({game_logic.undead_passive_gain(game_state.zombie_count, game_state.zombie_power) * (1000 / game_state.tick_rate) * game_state.souls_multiplier:.1f}/s)")

    # Buttons
    buy_skeleton_button.config(text=f"Buy Skeleton (Cost: {game_state.skeleton_cost})")
    buy_zombie_button.config(text=f"Buy Zombie (Cost: {game_state.zombie_cost})")
    update_button_state(buy_zombie_button, game_state.zombie_cost)
    update_button_state(buy_skeleton_button, game_state.skeleton_cost)
    create_upgrade_buttons()

    # Stats Labels
    souls_gained_stat.config(text=f"Total Souls Gained: {game_state.total_souls_gained}")
    souls_spent_stat.config(text=f"Total Souls Spent: {game_state.total_souls_spent}")
    souls_multiplier_stat.config(text=f"Souls Multiplier: {game_state.souls_multiplier:.1f}x")
    tick_rate_stat.config(text=f"Tick Rate: {game_state.tick_rate}ms")
    total_ticks_stat.config(text=f"Total Ticks: {game_state.tick_count}")
    click_power_stat.config(text=f"Click Power: {game_state.click_power:.1f}")
    total_clicks_stat.config(text=f"Total Clicks: {game_state.click_count}")

def create_upgrade_buttons():
    available_upgrades = game_logic.get_available_upgrades()
    for upgrade in available_upgrades:
        upgrade_id = upgrade["id"]
        name = upgrade["name"]
        cost = upgrade["cost"]
        if upgrade_id in game_state.upgrade_buttons:
            update_button_state(game_state.upgrade_buttons[upgrade_id], cost)
            continue
        game_state.upgrade_buttons[upgrade_id] = tk.Button(upgrades_tab, text=f"{name} (Cost: {cost})", command=lambda current_upgrade = upgrade: handle_upgrade_button(current_upgrade), state="disabled")
        game_state.upgrade_buttons[upgrade_id].pack()
        update_button_state(game_state.upgrade_buttons[upgrade_id], cost)

def update_button_state(button, cost):
    if game_state.souls >= cost:
        button.config(state="normal")
    else:
        button.config(state="disabled")

def handle_collect_click():
    game_logic.collect_soul_click()
    update_ui()

def handle_upgrade_button(upgrade):
    game_logic.buy_upgrade(upgrade)
    update_ui()

def handle_buy_skeleton():
    game_logic.buy_skeleton()
    update_ui()

def handle_buy_zombie():
    game_logic.buy_zombie()
    update_ui()

# UI
root = tk.Tk()
root.title("Necromancer Idle")
root.geometry("500x800")

status_frame = tk.Frame(root)
status_frame.pack()

# Main Game/Status Frame
souls_label = tk.Label(status_frame, text="Souls: 0", font=("Arial", 16))
souls_label.pack()
souls_passive = tk.Label(status_frame, text="(0/s)", font=("Arial", 16))
souls_passive.pack()
collect_button = tk.Button(status_frame, text="Collect Soul", command=handle_collect_click)
collect_button.pack()
skeletons_label = tk.Label(status_frame, text="Skeletons: 0", font=("Arial", 12))
skeletons_label.pack(pady=20)
zombies_label = tk.Label(status_frame, text="Zombies: 0", font=("Arial", 12))
zombies_label.pack(pady=20)


notebook = ttk.Notebook(root)
notebook.pack()

undead_tab = tk.Frame(notebook)
upgrades_tab = tk.Frame(notebook)
stats_tab = tk.Frame(notebook)

notebook.add(undead_tab, text="Undead")
notebook.add(upgrades_tab, text="Upgrades")
notebook.add(stats_tab, text="Stats")


# Buy Undead Buttons
buy_skeleton_button = tk.Button(undead_tab, text="Buy Skeleton (Cost: 1)", command=handle_buy_skeleton, state="disabled")
buy_skeleton_button.pack()
buy_zombie_button = tk.Button(undead_tab, text="Buy Zombie (Cost: 10)", command=handle_buy_zombie, state="disabled")
buy_zombie_button.pack()

# Stats
souls_gained_stat = tk.Label(stats_tab, text="Total Souls Gained: 0", font=("Arial", 10))
souls_gained_stat.pack()
souls_spent_stat = tk.Label(stats_tab, text="Total Souls Spent: 0", font=("Arial", 10))
souls_spent_stat.pack()
souls_multiplier_stat = tk.Label(stats_tab, text="Souls Multiplier: 1x", font=("Arial", 10))
souls_multiplier_stat.pack()
tick_rate_stat = tk.Label(stats_tab, text="Tick Rate: 1000ms", font=("Arial", 10))
tick_rate_stat.pack()
total_ticks_stat = tk.Label(stats_tab, text="Total Ticks: 0", font=("Arial", 10))
total_ticks_stat.pack()
click_power_stat = tk.Label(stats_tab, text="Click Power: 0.1", font=("Arial", 10))
click_power_stat.pack()
total_clicks_stat = tk.Label(stats_tab, text="Total Clicks: 0", font=("Arial", 10))
total_clicks_stat.pack()


update_ui()
game_loop()
root.mainloop()