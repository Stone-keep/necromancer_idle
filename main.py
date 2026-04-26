import tkinter as tk
from tkinter import ttk
import game_state, game_logic, save_system, style


def game_loop():
    game_state.tick_count += 1
    passive_gain = game_logic.total_passive_gain()
    game_logic.gain_souls(passive_gain)
    update_ui()
    root.after(game_state.tick_rate, game_loop)

def update_ui():
    # Update Game Status Labels
    souls_label.config(text=f"Souls: {game_state.souls:.1f}")
    souls_passive.config(text=f"({game_logic.total_passive_gain() * (1000 / game_state.tick_rate) * game_state.souls_multiplier:.1f}/s)")

    # Create & Update Undead Status
    create_undead_status_widgets()
    update_undead_status_widgets()

    # Create & Update Undead Buttons/Labels
    
    create_undead_buttons()
    update_undead_buttons()
    
    # Update Stats Labels
    souls_gained_stat.config(text=f"{game_state.total_souls_gained}")
    souls_spent_stat.config(text=f"{game_state.total_souls_spent}")
    souls_multiplier_stat.config(text=f"{game_state.souls_multiplier:.1f}x")
    tick_rate_stat.config(text=f"{(1000 / game_state.tick_rate):.2f}")
    total_ticks_stat.config(text=f"{game_state.tick_count}")
    click_power_stat.config(text=f"{game_state.click_power:.1f}")
    total_clicks_stat.config(text=f"{game_state.click_count}")

    # Update Available Upgrades
    create_upgrade_frames()

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

# UI
root = tk.Tk()
root.title("Necromancer Idle")
root.geometry("500x800")
root.resizable(False, False)
root.configure(bg=style.background_color)

status_frame = tk.Frame(root)
status_frame.pack(fill="x")
status_frame.configure(bg=style.background_color)

# Main Game/Status Frame
status_frame.grid_columnconfigure(0, weight=1)
status_frame.grid_columnconfigure(4, weight=1)

souls_label = tk.Label(status_frame, text="Souls: 0", font=style.souls_font, bg=style.background_color, fg=style.soul_color)
souls_label.grid(row=0, column=1, columnspan=3)
souls_passive = tk.Label(status_frame, text="(0/s)", font=style.souls_passive_font, bg=style.background_color, fg=style.text_color)
souls_passive.grid(row=1, column=1, columnspan=3)
collect_button = tk.Button(status_frame, text="Gather Soul", **style.collect_button_style, command=handle_collect_click)
collect_button.grid(row=2, column=1, columnspan=3, ipadx=15, ipady=7, pady=25)

undead_status_widgets = {}

def create_undead_status_widgets():
    new_undead_row = 3 + len(undead_status_widgets)
    for undead in game_state.undead_list:
        undead_name = undead.name
        if undead_name in undead_status_widgets:
            continue
        if undead.unlocked:
            name = tk.Label(status_frame, text=f"{undead_name}s:", font=style.undead_label_font, bg=style.background_color, fg=style.text_color)
            count = tk.Label(status_frame, text="0", font=style.undead_stats_font, bg=style.background_color, fg=style.text_color)
            souls = tk.Label(status_frame, text="(0/s)", font=style.undead_stats_font, bg=style.background_color, fg=style.text_color)
            undead_status_widgets[undead_name] = {
                "name": name,
                "count": count,
                "souls": souls
            }
            name.grid(row=new_undead_row, column=1, sticky="w", padx=5)
            count.grid(row=new_undead_row, column=2, padx=5)
            souls.grid(row=new_undead_row, column=3, sticky="e", padx=5)
            new_undead_row += 1

def update_undead_status_widgets():
    for undead in game_state.undead_list:
        undead_name = undead.name
        if undead_name not in undead_status_widgets:
            continue
        count = undead_status_widgets[undead_name]["count"]
        souls = undead_status_widgets[undead_name]["souls"]
        count.config(text=f"{undead.count}")
        souls.config(text=f"{game_logic.undead_status_production(undead)}")
        
# Notification

notification_frame = tk.Frame(root)
notification_frame.pack(fill="x", pady=(20, 10))
notification_frame.configure(bg=style.background_color)

notification_label = tk.Label(notification_frame, text="", font=style.notification_font, bg=style.background_color, fg=style.notification_color)
notification_label.pack()

notification_queue = []
notification_status = False

def create_notification(message):
    notification_queue.append(message)
    show_next_notification()
    
def show_next_notification():
    global notification_status
    if len(notification_queue) == 0:
        return
    if notification_status is True:
        return
    message = notification_queue.pop(0)
    notification_label.config(text=message, fg=style.notification_color)
    notification_status = True
    root.after(5000, clear_notification)

def clear_notification():
    global notification_status
    notification_status = False
    notification_label.config(text="")
    if len(notification_queue) > 0:
        root.after(1000, show_next_notification)
        

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

notebook.add(undead_tab, text="Undead")
notebook.add(upgrades_tab, text="Upgrades")
notebook.add(stats_tab, text="Stats")


# Buy Undead Tab
undead_content = tk.Frame(undead_tab, bg=style.background_color)
undead_content.pack(pady=(10, 0))
undead_content.grid_columnconfigure(0, weight=1)
undead_content.grid_columnconfigure(2, weight=1)

undead_buttons = {}

def create_undead_buttons():
    new_button_row = len(undead_buttons) * 2
    for undead in game_state.undead_list:
        name = undead.name
        if name in undead_buttons:
            continue
        if undead.unlocked:
            button = tk.Button(undead_content, text=f"Buy {undead.name} (Cost: {undead.cost})", command=lambda current_undead = undead: handle_buy_undead(current_undead), state="disabled", **style.shop_button_style)
            label = tk.Label(undead_content, text=game_logic.undead_button_production(undead), font=style.stats_dynamic_font, bg=style.background_color, fg=style.text_color)
            undead_buttons[name] = {
                "button": button,
                "label": label
            }
            button.grid(row=new_button_row, column=1, pady=(10, 0))
            label.grid(row=new_button_row+1, column=1)
            new_button_row += 2

def update_undead_buttons():
    for undead in game_state.undead_list:
        name = undead.name
        if name not in undead_buttons:
            continue
        button = undead_buttons[name]["button"]
        label = undead_buttons[name]["label"]
        button.config(text=f"Buy {undead.name} (Cost: {undead.cost})")
        label.config(text=game_logic.undead_button_production(undead))    
        game_logic.update_button_state(button, undead.cost)


# Upgrades Tab

upgrades_content = tk.Frame(upgrades_tab, bg=style.background_color)
upgrades_content.pack(pady=(10, 0))

def create_upgrade_frames():
    available_upgrades = game_logic.get_available_upgrades()
    for upgrade in available_upgrades:
        upgrade_id = upgrade["id"]
        name = upgrade["name"]
        cost = upgrade["cost"]
        description = upgrade["description"]
        if upgrade_id in game_state.upgrade_frames:
            game_logic.update_button_state(game_state.upgrade_frames[upgrade_id]["button"], cost)
            continue
        frame = tk.Frame(upgrades_content, bg=style.background_color)
        button = tk.Button(frame, text=f"{name} (Cost: {cost})", command=lambda current_upgrade = upgrade: handle_upgrade_button(current_upgrade), state="disabled", **style.shop_button_style)
        label = tk.Label(frame, text=f"{description}", font=style.stats_dynamic_font, bg=style.background_color, fg=style.text_color)
        game_state.upgrade_frames[upgrade_id] = {
            "frame": frame,
            "button": button,
            "label": label
        }
        
        frame.pack(pady=(0, 10))
        button.pack()
        label.pack()
        create_notification(f"New Upgrade Available: {name}")
        game_logic.update_button_state(button, cost)
        
# Stats
stats_content = tk.Frame(stats_tab, bg=style.background_color)
stats_content.pack(pady=(10, 0))
stats_content.grid_columnconfigure(0, weight=1)
stats_content.grid_columnconfigure(3, weight=1)

for row in range(7):
    stats_content.grid_rowconfigure(row, pad=4)

souls_gained_label = tk.Label(stats_content, text="Total Souls Gained:", font=style.stats_label_font, bg=style.background_color, fg=style.text_color)
souls_gained_label.grid(row=0, column=1, sticky="w", padx=(0, 35))
souls_gained_stat = tk.Label(stats_content, text="0", font=style.stats_dynamic_font, bg=style.background_color, fg=style.text_color)
souls_gained_stat.grid(row=0, column=2, sticky="e", padx=(35, 0))
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
click_power_label = tk.Label(stats_content, text="Click Power:", font=style.stats_label_font, bg=style.background_color, fg=style.text_color)
click_power_label.grid(row=5, column=1, sticky="w")
click_power_stat = tk.Label(stats_content, text="0.1", font=style.stats_dynamic_font, bg=style.background_color, fg=style.text_color)
click_power_stat.grid(row=5, column=2, sticky="e")
total_clicks_label = tk.Label(stats_content, text="Total Clicks:", font=style.stats_label_font, bg=style.background_color, fg=style.text_color)
total_clicks_label.grid(row=6, column=1, sticky="w")
total_clicks_stat = tk.Label(stats_content, text="0", font=style.stats_dynamic_font, bg=style.background_color, fg=style.text_color)
total_clicks_stat.grid(row=6, column=2, sticky="e")

save_system.load_from_json()
update_ui()
game_loop()
auto_save()
root.protocol("WM_DELETE_WINDOW", close_and_save)
root.mainloop()