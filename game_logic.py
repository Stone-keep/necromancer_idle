import game_state

def is_upgrade_unlocked(upgrade):
    return upgrade["requirement"]()

def get_available_upgrades():
    available_upgrades = []
    for upgrade in game_state.upgrades:
        if is_upgrade_unlocked(upgrade) and not upgrade["bought"]:
            available_upgrades.append(upgrade)
    return available_upgrades

def can_buy_upgrade(upgrade):
    return is_upgrade_unlocked(upgrade) and game_state.souls >= upgrade["cost"] and not upgrade["bought"]

def apply_upgrade_effect(upgrade):
    if upgrade["effect_type"] == "click_power":
        game_state.click_power *= upgrade["effect_value"]
    elif upgrade["effect_type"] == "skeleton_power":
        game_state.skeleton.power *= upgrade["effect_value"]
    elif upgrade["effect_type"] == "zombie_power":
        game_state.zombie.power *= upgrade["effect_value"]
    elif upgrade["effect_type"] == "wraith_power":
        game_state.wraith.power *= upgrade["effect_value"]
    elif upgrade["effect_type"] == "souls_multiplier":
        game_state.souls_multiplier *= upgrade["effect_value"]
    elif upgrade["effect_type"] == "tick_rate":
        game_state.tick_rate = int(game_state.tick_rate * upgrade["effect_value"])
    elif upgrade["effect_type"] == "skeleton_cost_multiplier":
        game_state.skeleton.cost_multiplier = float(game_state.skeleton.cost_multiplier - upgrade["effect_value"])
        game_state.skeleton.recalculate_cost()
    elif upgrade["effect_type"] == "zombie_cost_multiplier":
        game_state.zombie.cost_multiplier = float(game_state.zombie.cost_multiplier - upgrade["effect_value"])
        game_state.zombie.recalculate_cost()
    elif upgrade["effect_type"] == "skeleton_multiplier":
        game_state.skeleton.global_multiplier += float(upgrade["effect_value"])
    elif upgrade["effect_type"] == "skeleton_zombie_power":
        game_state.skeleton.power *= upgrade["effect_value"]
        game_state.zombie.power *= upgrade["effect_value"]
    elif upgrade["effect_type"] == "wraith_per_zombie_scaling":
        game_state.wraith_per_zombie_scaling += upgrade["effect_value"]
        game_state.wraith.recalculate_cost()
    elif upgrade["effect_type"] == "wraith_multiplier":
        game_state.wraith.global_multiplier += float(upgrade["effect_value"])
    elif upgrade["effect_type"] == "click_passive_scaling":
        game_state.click_passive_scaling += upgrade["effect_value"]
    elif upgrade["effect_type"] == "souls_tick_multiplier":
        game_state.souls_tick_multiplier += upgrade["effect_value"]
    else:
        raise ValueError("Upgrade effect type not found")

def buy_upgrade(upgrade):
    if can_buy_upgrade(upgrade):
        spend_souls(upgrade["cost"])
        upgrade["bought"] = True
        apply_upgrade_effect(upgrade)
        upgrade_id = upgrade["id"]
        if upgrade_id in game_state.upgrade_frames:
            game_state.upgrade_frames[upgrade_id]["frame"].destroy()
            game_state.upgrade_frames.pop(upgrade_id)

def undead_global_multiplier():
    global_multiplier = 1
    for undead in game_state.undead_list:
        global_multiplier *= 1 + (undead.count * undead.global_multiplier)
    return global_multiplier

def total_passive_gain():
    return sum(undead.passive_gain() for undead in game_state.undead_list) * undead_global_multiplier() * (1 + (game_state.tick_count // 10) * game_state.souls_tick_multiplier)

def gain_souls(amount):
    game_state.souls = round(game_state.souls + (amount * game_state.souls_multiplier), 1)
    game_state.total_souls_gained = round(game_state.total_souls_gained + (amount * game_state.souls_multiplier), 1)

def spend_souls(cost):
    game_state.souls = round(game_state.souls - cost, 1)
    game_state.total_souls_spent = round(game_state.total_souls_spent + cost, 1)

def collect_soul_click():
    passive_scaling = game_state.click_passive_scaling * total_passive_gain()
    game_state.click_count += 1
    gain_souls(game_state.click_power + passive_scaling)
    
def buy_undead(undead):
    if game_state.souls >= undead.cost:
        spend_souls(undead.cost)
        undead.buy()
        recalculate_all_undead_cost()

def update_button_state(button, cost):
    if game_state.souls >= cost:
        button.config(state="normal")
    else:
        button.config(state="disabled")

def undead_status_production(undead):
    return f"{undead.passive_gain() * (1000 / game_state.tick_rate) * game_state.souls_multiplier * undead_global_multiplier():.1f}/s"

def undead_button_production(undead):
    return f"Each {undead.name} produces {undead.power * (1000 / game_state.tick_rate) * game_state.souls_multiplier * undead_global_multiplier():.1f} Souls per second"

def true_cost_multiplier(undead):
    multiplier = undead.cost_multiplier

    if undead.name == "Wraith":
        multiplier -= game_state.wraith_per_zombie_scaling * game_state.zombie.count
    
    return max(multiplier, 1.1)

def recalculate_all_undead_cost():
    for undead in game_state.undead_list:
        undead.recalculate_cost()