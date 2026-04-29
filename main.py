import tkinter as tk
from tkinter import ttk
import game_state, game_logic, save_system, style

def game_loop():
    tickrate = game_logic.tickrate_after_vampires(game_state.tick_rate)
    if game_state.game_paused:
        root.after(tickrate, game_loop)
        return
    game_state.tick_count += 1
    passive_gain = game_logic.total_passive_gain()
    game_logic.gain_souls(passive_gain)
    unlock_undead()
    update_ui()
    root.after(tickrate, game_loop)

def auto_save():
    save_system.save_to_json()
    root.after(60000, auto_save)

def close_and_save():
    save_system.save_to_json()
    print("Game saved on exit!")
    root.destroy()

def handle_collect_click():
    game_logic.collect_soul_click()
    update_ui()

def handle_upgrade_button(upgrade):
    game_logic.buy_upgrade(upgrade)
    update_ui()

def handle_buy_undead(undead):
    game_logic.buy_undead(undead)
    update_ui()

def unlock_undead():
    if game_state.vampire.unlocked is False and game_state.wraith.count >= 10:
        game_state.vampire.unlocked = True
        create_notification("You can now raise Vampires", style.notification_undead_color)
    if game_state.lich.unlocked is False and game_state.vampire.count >= 10:
        game_state.lich.unlocked = True
        create_notification("You can now raise Liches", style.notification_undead_color)

def update_ui():
    # Update Game Status Labels
    souls_label.config(text=f"Souls: {game_logic.decimal_or_commas(game_state.souls)}")
    souls_passive.config(text=f"({game_logic.decimal_or_commas(game_logic.total_passive_gain() * (1000 / game_logic.tickrate_after_vampires(game_state.tick_rate)) * game_state.souls_multiplier)}/s)")

    # Create & Update Undead Status
    create_undead_status_labels()
    update_undead_status_labels()

    # Create & Update Undead Buttons/Labels
    create_undead_buttons()
    update_undead_buttons()
    
    # Update Stats Labels
    souls_gained_stat.config(text=f"{game_logic.decimal_or_commas(game_state.total_souls_gained)}")
    souls_spent_stat.config(text=f"{game_logic.decimal_or_commas(game_state.total_souls_spent)}")
    souls_multiplier_stat.config(text=f"{game_state.souls_multiplier * game_logic.souls_for_ticks_multiplier():.2f}x")
    tick_rate_stat.config(text=f"{(1000 / game_logic.tickrate_after_vampires(game_state.tick_rate)):.2f}")
    total_ticks_stat.config(text=f"{game_state.tick_count:,}")
    time_passed_stat.config(text=f"{(game_state.tick_count / (1000 / game_logic.tickrate_after_vampires(game_state.tick_rate)) // 60):.0f} minutes")
    click_power_stat.config(text=f"{game_logic.decimal_or_commas(game_state.click_power + (game_state.click_passive_scaling * game_logic.total_passive_gain()) * game_state.souls_multiplier)}")
    total_clicks_stat.config(text=f"{game_state.click_count:,}")

    # Create Available Upgrades
    create_upgrade_buttons()

# UI (Root)
root = tk.Tk()
root.title("Necromancer Idle")
root.geometry("550x850")
root.resizable(False, False)
root.configure(bg=style.background_color)

# Main Game/Status Frame
status_frame = tk.Frame(root)
status_frame.pack(fill="x")
status_frame.configure(bg=style.background_color)

status_frame.grid_columnconfigure(0, weight=1)
status_frame.grid_columnconfigure(4, weight=1)

souls_label = tk.Label(status_frame, text="Souls: 0", font=style.souls_font, bg=style.background_color, fg=style.soul_color)
souls_label.grid(row=0, column=1, columnspan=3)
souls_passive = tk.Label(status_frame, text="(0/s)", font=style.souls_passive_font, bg=style.background_color, fg=style.text_color)
souls_passive.grid(row=1, column=1, columnspan=3)
collect_button = tk.Button(status_frame, text="Gather Souls", **style.collect_button_style, command=handle_collect_click)
collect_button.grid(row=2, column=1, columnspan=3, ipadx=15, ipady=7, pady=25)

undead_status_labels = {}
def create_undead_status_labels():
    new_undead_row = 3 + len(undead_status_labels)
    for undead in game_state.undead_list:
        undead_name = undead.name
        if undead_name in undead_status_labels:
            continue
        name = tk.Label(status_frame, text="", font=style.undead_label_font, bg=style.background_color, fg=style.text_color)
        count = tk.Label(status_frame, text="", font=style.undead_stats_font, bg=style.background_color, fg=style.text_color)
        souls = tk.Label(status_frame, text="", font=style.undead_stats_font, bg=style.background_color, fg=style.text_color)
        undead_status_labels[undead_name] = {
            "name": name,
            "count": count,
            "souls": souls
        }
        name.grid(row=new_undead_row, column=1, sticky="w", padx=(0, 15))
        count.grid(row=new_undead_row, column=2, padx=15)
        souls.grid(row=new_undead_row, column=3, sticky="e", padx=(15, 0))
        new_undead_row += 1

def update_undead_status_labels():
    for undead in game_state.undead_list:
        undead_name = undead.name
        if undead_name not in undead_status_labels:
            continue
        name = undead_status_labels[undead_name]["name"]
        count = undead_status_labels[undead_name]["count"]
        souls = undead_status_labels[undead_name]["souls"]
        if undead.unlocked:
            name.config(text=f"{undead.name_plural}:")
            count.config(text=f"{undead.count}")
            souls.config(text=f"{game_logic.undead_status_production(undead)}")
        else:
            name.config(text="")
            count.config(text="")
            souls.config(text="")
        
# Notifications
notification_frame = tk.Frame(root)
notification_frame.pack(fill="x", pady=(20, 10))
notification_frame.configure(bg=style.background_color)
notification_label = tk.Label(notification_frame, text="", font=style.notification_font, bg=style.background_color)
notification_label.pack()
notification_queue = []
notification_status = False

def create_notification(message, color):
    notification = (message, color)
    notification_queue.append(notification)
    show_next_notification()
    
def show_next_notification():
    global notification_status
    if len(notification_queue) == 0:
        return
    if notification_status is True:
        return
    notification = notification_queue.pop(0)
    message, color = notification
    notification_label.config(text=message, fg=color)
    notification_status = True
    root.after(5000, clear_notification)

def clear_notification():
    global notification_status
    notification_status = False
    notification_label.config(text="")
    if len(notification_queue) > 0:
        root.after(1000, show_next_notification)
        
# Notebook (Tabs)

notebook_style = ttk.Style()
notebook_style.theme_use("default")

notebook_style.configure(
    "TNotebook",
    background=style.background_color,
    borderwidth=0
)

notebook_style.configure(
    "TNotebook.Tab",
    background="#1a1a1a",
    foreground="#e6fff8",
    padding=(10, 5),
    font=("Georgia", 10, "bold")
)

notebook_style.map(
    "TNotebook.Tab",
    background=[("selected", "#25443d")],
    foreground=[("selected", "#9fffe0")]
)

notebook = ttk.Notebook(root)
notebook.pack(fill="x")

undead_tab = tk.Frame(notebook, bg=style.background_color)
upgrades_tab = tk.Frame(notebook, bg=style.background_color)
stats_tab = tk.Frame(notebook, bg=style.background_color)
info_tab = tk.Frame(notebook, bg=style.background_color)

notebook.add(undead_tab, text="Undead")
notebook.add(upgrades_tab, text="Upgrades")
notebook.add(stats_tab, text="Stats")
notebook.add(info_tab, text="Info")

save_was_loaded = save_system.load_from_json()

if save_was_loaded:
    notebook.select(undead_tab)
else:
    notebook.select(info_tab)

# Buy Undead Tab
undead_content = tk.Frame(undead_tab, bg=style.background_color)
undead_content.pack(pady=(10, 0))
undead_content.grid_columnconfigure(0, weight=1)
undead_content.grid_columnconfigure(3, weight=1)

undead_buttons = {}

def create_undead_buttons():
    new_button_row = len(undead_buttons)
    for undead in game_state.undead_list:
        name = undead.name
        if name in undead_buttons:
            continue
        if undead.unlocked:
            button = tk.Button(undead_content, text=f"Raise {undead.name}\n(Cost: {undead.cost:,})", command=lambda current_undead = undead: handle_buy_undead(current_undead), state="disabled", **style.shop_button_style)
            label = tk.Label(undead_content, text=game_logic.undead_button_production(undead), font=style.undead_button_label_font, bg=style.background_color, fg=style.text_color, justify="center", wraplength=250)
            undead_buttons[name] = {
                "button": button,
                "label": label
            }
            button.grid(row=new_button_row, column=1, pady=(10, 0), padx=(0, 30), sticky="w")
            label.grid(row=new_button_row, column=2, pady=(10, 0), padx=(30, 0), sticky="ew")
            new_button_row += 1
    if game_state.total_souls_gained >= 500_000_000 and "undead_king" not in undead_buttons:
        game_state.undead_king_unlocked = True
        victory_button = tk.Button(undead_content, text="Summon The Undead King and Claim Victory\n(Cost: 1,000,000,000)", command=trigger_victory, state="disabled", **style.shop_button_style)
        undead_buttons["undead_king"] = {
            "button": victory_button
            }
        victory_button.grid(row=new_button_row, column=1, columnspan=2, pady=(10, 0), sticky="ew")


def update_undead_buttons():
    undead_king_button = undead_buttons["undead_king"]["button"]
    for undead in game_state.undead_list:
        name = undead.name
        if name not in undead_buttons:
            continue
        button = undead_buttons[name]["button"]
        label = undead_buttons[name]["label"]
        button.config(text=f"Raise {undead.name}\n(Cost: {undead.cost:,})")
        label.config(text=game_logic.undead_button_production(undead))    
        game_logic.update_button_state(button, undead.cost)
    if "undead_king" in undead_buttons and game_state.victory_achieved is False:
        game_logic.update_button_state(undead_king_button, 1_000_000_000)
    elif game_state.victory_achieved is True:
        undead_king_button.config(text="Undead King Has Risen\nTo Rule Over The World", state="disabled")

# Upgrades Tab
upgrades_content = tk.Frame(upgrades_tab, bg=style.background_color)
upgrades_content.pack(pady=(10, 0))
upgrades_content.grid_columnconfigure(0, weight=1)
upgrades_content.grid_columnconfigure(1, weight=1)

def create_upgrade_buttons():
    new_button_row = len(game_state.upgrade_buttons)
    available_upgrades = game_logic.get_available_upgrades()
    for upgrade in available_upgrades:
        upgrade_id = upgrade["id"]
        name = upgrade["name"]
        cost = upgrade["cost"]
        description = upgrade["description"]
        if upgrade_id in game_state.upgrade_buttons:
            game_logic.update_button_state(game_state.upgrade_buttons[upgrade_id]["button"], cost)
            continue
        button = tk.Button(upgrades_content, text=f"{name}\n(Cost: {cost:,})", command=lambda current_upgrade = upgrade: handle_upgrade_button(current_upgrade), state="disabled", **style.shop_button_style)
        label = tk.Label(upgrades_content, text=f"{description}", font=style.undead_button_label_font, bg=style.background_color, fg=style.text_color, wraplength=250, justify="center")
        game_state.upgrade_buttons[upgrade_id] = {
            "button": button,
            "label": label
        }
        
        button.grid(row=new_button_row, column=0, pady=(10, 0), padx=(0, 30), sticky="w")
        label.grid(row=new_button_row, column=1, pady=(10, 0), padx=(30, 0), sticky="ew")
        new_button_row += 1
        create_notification(f"New Upgrade Available: {name}", style.notification_upgrade_color)
        game_logic.update_button_state(button, cost)
        
# Stats Tab
stats_content = tk.Frame(stats_tab, bg=style.background_color)
stats_content.pack(pady=(10, 0))
stats_content.grid_columnconfigure(0, weight=1)
stats_content.grid_columnconfigure(3, weight=1)

for row in range(7):
    stats_content.grid_rowconfigure(row, pad=4)

souls_gained_label = tk.Label(stats_content, text="Total Souls Gained:", font=style.stats_label_font, bg=style.background_color, fg=style.text_color)
souls_gained_label.grid(row=0, column=1, sticky="w", padx=(0, 40))
souls_gained_stat = tk.Label(stats_content, text="0", font=style.stats_dynamic_font, bg=style.background_color, fg=style.text_color)
souls_gained_stat.grid(row=0, column=2, sticky="e", padx=(40, 0))
souls_spent_label = tk.Label(stats_content, text="Total Souls Spent:", font=style.stats_label_font, bg=style.background_color, fg=style.text_color)
souls_spent_label.grid(row=1, column=1, sticky="w")
souls_spent_stat = tk.Label(stats_content, text="0", font=style.stats_dynamic_font, bg=style.background_color, fg=style.text_color)
souls_spent_stat.grid(row=1, column=2, sticky="e")
souls_multiplier_label = tk.Label(stats_content, text="Souls Multiplier:", font=style.stats_label_font, bg=style.background_color, fg=style.text_color)
souls_multiplier_label.grid(row=2, column=1, sticky="w")
souls_multiplier_stat = tk.Label(stats_content, text="1x", font=style.stats_dynamic_font, bg=style.background_color, fg=style.text_color)
souls_multiplier_stat.grid(row=2, column=2, sticky="e")
tick_rate_label = tk.Label(stats_content, text="Ticks Per Second:", font=style.stats_label_font, bg=style.background_color, fg=style.text_color)
tick_rate_label.grid(row=3, column=1, sticky="w")
tick_rate_stat = tk.Label(stats_content, text="1", font=style.stats_dynamic_font, bg=style.background_color, fg=style.text_color)
tick_rate_stat.grid(row=3, column=2, sticky="e")
total_ticks_label = tk.Label(stats_content, text="Total Ticks:", font=style.stats_label_font, bg=style.background_color, fg=style.text_color)
total_ticks_label.grid(row=4, column=1, sticky="w")
total_ticks_stat = tk.Label(stats_content, text="0", font=style.stats_dynamic_font, bg=style.background_color, fg=style.text_color)
total_ticks_stat.grid(row=4, column=2, sticky="e")
time_passed_label = tk.Label(stats_content, text="Time Passed:", font=style.stats_label_font, bg=style.background_color, fg=style.text_color)
time_passed_label.grid(row=5, column=1, sticky="w")
time_passed_stat = tk.Label(stats_content, text="0s", font=style.stats_dynamic_font, bg=style.background_color, fg=style.text_color)
time_passed_stat.grid(row=5, column=2, sticky="e")
click_power_label = tk.Label(stats_content, text="Click Power:", font=style.stats_label_font, bg=style.background_color, fg=style.text_color)
click_power_label.grid(row=6, column=1, sticky="w")
click_power_stat = tk.Label(stats_content, text="0.1", font=style.stats_dynamic_font, bg=style.background_color, fg=style.text_color)
click_power_stat.grid(row=6, column=2, sticky="e")
total_clicks_label = tk.Label(stats_content, text="Total Clicks:", font=style.stats_label_font, bg=style.background_color, fg=style.text_color)
total_clicks_label.grid(row=7, column=1, sticky="w")
total_clicks_stat = tk.Label(stats_content, text="0", font=style.stats_dynamic_font, bg=style.background_color, fg=style.text_color)
total_clicks_stat.grid(row=7, column=2, sticky="e")

# Info Tab
info_content = tk.Frame(info_tab, bg=style.background_color)
info_content.pack(pady=(10, 0))
info_label = tk.Label(info_content, text=style.info_text, font=style.info_font, bg=style.background_color, fg=style.text_color, justify="left", wraplength=530)
info_label.pack()

# Victory Pop-Up
def trigger_victory():
    if game_state.souls < 1_000_000_000:
        return
    game_logic.spend_souls(1_000_000_000)
    game_state.victory_achieved = False
    game_state.game_paused = True
    def continue_after_victory():
        victory_window.destroy()
        game_state.game_paused = False

    # Create Victory Window
    victory_window = tk.Toplevel(root)  
    victory_window.title("Victory!")
    victory_window.resizable(False, False)
    victory_window.configure(bg=style.border_color)
    victory_window.grab_set()
    victory_content = tk.Frame(victory_window, bg=style.background_color, padx=20, pady=20)
    victory_content.pack(padx=3, pady=3, fill="both")

    # Victory Text
    victory_title = tk.Label(victory_content, text="The Undead King Has Risen", font=style.victory_title_font, bg=style.background_color, fg=style.notification_undead_color, justify="center")
    victory_title.pack(pady=(0, 10))
    victory_flavor = tk.Label(victory_content, text=style.victory_text_flavor, font=style.victory_text_font, bg=style.background_color, fg=style.text_color, justify="left", wraplength=350)
    victory_flavor.pack()
    victory_meta = tk.Label(victory_content, text=style.victory_text_meta, font=style.victory_text_font, bg=style.background_color, fg=style.text_color, justify="left", wraplength=350)
    victory_meta.pack()

    # Victory Buttons
    continue_button = tk.Button(victory_content, text="Continue", command=continue_after_victory, **style.collect_button_style)
    continue_button.pack()
    exit_button = tk.Button(victory_content, text="Exit", command=close_and_save, **style.collect_button_style)
    exit_button.pack(pady=(20, 0))

    # Resize Victory Window
    root.update_idletasks()
    victory_window.update_idletasks()
    root_x = root.winfo_rootx()
    root_y = root.winfo_rooty()
    root_width = root.winfo_reqwidth()
    root_height = root.winfo_reqheight()
    popup_width = victory_window.winfo_reqwidth()
    popup_height = victory_window.winfo_reqheight()
    popup_x = root_x + (root_width // 2) - (popup_width // 2) + 15
    popup_y = root_y + (root_height // 2) - (popup_height // 2)
    victory_window.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}")
    victory_window.transient(root)
    victory_window.overrideredirect(True)


update_ui()
game_loop()
auto_save()
root.protocol("WM_DELETE_WINDOW", close_and_save)
root.mainloop()