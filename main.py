import tkinter as tk
from tkinter import ttk
import game_state, game_logic, save_system

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
    skeleton_count.config(text=f"{game_state.skeleton.count}")
    skeleton_souls.config(text=f"({game_state.skeleton.passive_gain() * (1000 / game_state.tick_rate) * game_state.souls_multiplier:.1f}/s)")
    
    zombie_count.config(text=f"{game_state.zombie.count}")
    zombie_souls.config(text=f"({game_state.zombie.passive_gain() * (1000 / game_state.tick_rate) * game_state.souls_multiplier:.1f}/s)")

    # Undead
    buy_skeleton_button.config(text=f"Buy Skeleton (Cost: {game_state.skeleton.cost})")
    skeleton_production.config(text=f"Each Skeleton produces {game_state.skeleton.power * (1000 / game_state.tick_rate) * game_state.souls_multiplier:.1f} Souls per second")
    update_button_state(buy_skeleton_button, game_state.skeleton.cost)
    buy_zombie_button.config(text=f"Buy Zombie (Cost: {game_state.zombie.cost})")
    zombie_production.config(text=f"Each Zombie produces {game_state.zombie.power * (1000 / game_state.tick_rate) * game_state.souls_multiplier:.1f} Souls per second")
    update_button_state(buy_zombie_button, game_state.zombie.cost)
    
    

    # Stats Labels
    souls_gained_stat.config(text=f"{game_state.total_souls_gained}")
    souls_spent_stat.config(text=f"{game_state.total_souls_spent}")
    souls_multiplier_stat.config(text=f"{game_state.souls_multiplier:.1f}x")
    tick_rate_stat.config(text=f"{game_state.tick_rate}ms")
    total_ticks_stat.config(text=f"{game_state.tick_count}")
    click_power_stat.config(text=f"{game_state.click_power:.1f}")
    total_clicks_stat.config(text=f"{game_state.click_count}")

    create_upgrade_frames()

def auto_save():
    save_system.save_to_json()
    root.after(60000, auto_save)

def close_and_save():
    save_system.save_to_json()
    print("Game saved on exit!")
    root.destroy()


def create_upgrade_frames():
    available_upgrades = game_logic.get_available_upgrades()
    for upgrade in available_upgrades:
        upgrade_id = upgrade["id"]
        name = upgrade["name"]
        cost = upgrade["cost"]
        description = upgrade["description"]
        if upgrade_id in game_state.upgrade_frames:
            update_button_state(game_state.upgrade_frames[upgrade_id]["button"], cost)
            continue
        frame = tk.Frame(upgrades_tab)
        button = tk.Button(frame, text=f"{name} (Cost: {cost})", command=lambda current_upgrade = upgrade: handle_upgrade_button(current_upgrade), state="disabled")
        label = tk.Label(frame, text=f"{description}")
        game_state.upgrade_frames[upgrade_id] = {
            "frame": frame,
            "button": button,
            "label": label
        }
        
        frame.pack(pady=(0, 10))
        button.pack()
        label.pack()
        update_button_state(button, cost)

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
    game_logic.buy_undead(game_state.skeleton)
    update_ui()

def handle_buy_zombie():
    game_logic.buy_undead(game_state.zombie)
    update_ui()

# UI
root = tk.Tk()
root.title("Necromancer Idle")
root.geometry("500x800")

status_frame = tk.Frame(root)
status_frame.pack(fill="x")

# Main Game/Status Frame
status_frame.grid_columnconfigure(0, weight=1)
status_frame.grid_columnconfigure(4, weight=1)

souls_label = tk.Label(status_frame, text="Souls: 0", font=("Arial", 20, "bold"))
souls_label.grid(row=0, column=1, columnspan=3)
souls_passive = tk.Label(status_frame, text="(0/s)", font=("Arial", 16))
souls_passive.grid(row=1, column=1, columnspan=3)
collect_button = tk.Button(status_frame, text="Collect Soul", font=("Arial", 14, "bold"), command=handle_collect_click)
collect_button.grid(row=2, column=1, columnspan=3, ipadx=15, ipady=7, pady=25)

skeleton_name = tk.Label(status_frame, text="Skeletons:", font=("Arial", 12, "bold"))
skeleton_name.grid(row=4, column=1, sticky="w", padx=5)
skeleton_count = tk.Label(status_frame, text="0", font=("Arial", 12))
skeleton_count.grid(row=4, column=2, padx=5)
skeleton_souls = tk.Label(status_frame, text="(0/s)", font=("Arial", 12))
skeleton_souls.grid(row=4, column=3, sticky="e", padx=5)

zombie_name = tk.Label(status_frame, text="Zombies:", font=("Arial", 12, "bold"))
zombie_name.grid(row=5, column=1, sticky="w", padx=5)
zombie_count = tk.Label(status_frame, text="0", font=("Arial", 12))
zombie_count.grid(row=5, column=2, padx=5)
zombie_souls = tk.Label(status_frame, text="(0/s)", font=("Arial", 12))
zombie_souls.grid(row=5, column=3, sticky="e", padx=5)


notebook = ttk.Notebook(root)
notebook.pack(fill="x")

undead_tab = tk.Frame(notebook)
upgrades_tab = tk.Frame(notebook)
stats_tab = tk.Frame(notebook)

notebook.add(undead_tab, text="Undead")
notebook.add(upgrades_tab, text="Upgrades")
notebook.add(stats_tab, text="Stats")


# Buy Undead Tab
undead_tab.grid_columnconfigure(0, weight=1)
undead_tab.grid_columnconfigure(2, weight=1)

buy_skeleton_button = tk.Button(undead_tab, text="Buy Skeleton (Cost: 1)", command=handle_buy_skeleton, state="disabled")
buy_skeleton_button.grid(row=0, column=1)
skeleton_production = tk.Label(undead_tab, text="Each Skeleton produces 0.2 Souls per second")
skeleton_production.grid(row=1, column=1)
buy_zombie_button = tk.Button(undead_tab, text="Buy Zombie (Cost: 10)", command=handle_buy_zombie, state="disabled")
buy_zombie_button.grid(row=2, column=1, pady=(10, 0))
zombie_production = tk.Label(undead_tab, text="Each Zombie produces 0.6 Souls per second")
zombie_production.grid(row=3, column=1)

upgrades_info = tk.Label(upgrades_tab, text="Hint: Upgrades are unlocked dynamically once certain conditions (number of undead or clicks, total souls generated, time passed etc.) are met. Buying an upgrade permanently unlocks the bonus.")

# Stats
stats_tab.grid_columnconfigure(0, weight=1)
stats_tab.grid_columnconfigure(3, weight=1)

stats_label_font = ("Arial", 10, "bold")
stats_dynamic_font = ("Arial", 10)

souls_gained_label = tk.Label(stats_tab, text="Total Souls Gained:", font=stats_label_font)
souls_gained_label.grid(row=0, column=1, sticky="w")
souls_gained_stat = tk.Label(stats_tab, text="0", font=stats_dynamic_font)
souls_gained_stat.grid(row=0, column=2, sticky="e")
souls_spent_label = tk.Label(stats_tab, text="Total Souls Spent:", font=stats_label_font)
souls_spent_label.grid(row=1, column=1, sticky="w")
souls_spent_stat = tk.Label(stats_tab, text="0", font=stats_dynamic_font)
souls_spent_stat.grid(row=1, column=2, sticky="e")
souls_multiplier_label = tk.Label(stats_tab, text="Souls Multiplier:", font=stats_label_font)
souls_multiplier_label.grid(row=2, column=1, sticky="w")
souls_multiplier_stat = tk.Label(stats_tab, text="1x", font=stats_dynamic_font)
souls_multiplier_stat.grid(row=2, column=2, sticky="e")
tick_rate_label = tk.Label(stats_tab, text="Tick Rate:", font=stats_label_font)
tick_rate_label.grid(row=3, column=1, sticky="w")
tick_rate_stat = tk.Label(stats_tab, text="1000ms", font=stats_dynamic_font)
tick_rate_stat.grid(row=3, column=2, sticky="e")
total_ticks_label = tk.Label(stats_tab, text="Total Ticks:", font=stats_label_font)
total_ticks_label.grid(row=4, column=1, sticky="w")
total_ticks_stat = tk.Label(stats_tab, text="0", font=stats_dynamic_font)
total_ticks_stat.grid(row=4, column=2, sticky="e")
click_power_label = tk.Label(stats_tab, text="Click Power:", font=stats_label_font)
click_power_label.grid(row=5, column=1, sticky="w")
click_power_stat = tk.Label(stats_tab, text="0.1", font=stats_dynamic_font)
click_power_stat.grid(row=5, column=2, sticky="e")
total_clicks_label = tk.Label(stats_tab, text="Total Clicks:", font=stats_label_font)
total_clicks_label.grid(row=6, column=1, sticky="w")
total_clicks_stat = tk.Label(stats_tab, text="0", font=stats_dynamic_font)
total_clicks_stat.grid(row=6, column=2, sticky="e")

save_system.load_from_json()
update_ui()
game_loop()
auto_save()
root.protocol("WM_DELETE_WINDOW", close_and_save)
root.mainloop()