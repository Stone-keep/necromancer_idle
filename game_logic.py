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
    elif upgrade["effect_type"] == "souls_multiplier":
        game_state.souls_multiplier *= upgrade["effect_value"]
    elif upgrade["effect_type"] == "tick_rate":
        game_state.tick_rate = int(game_state.tick_rate * upgrade["effect_value"])
    else:
        raise ValueError("Upgrade effect type not found")

def buy_upgrade(upgrade):
    if can_buy_upgrade(upgrade):
        spend_souls(upgrade["cost"])
        upgrade["bought"] = True
        apply_upgrade_effect(upgrade)
        upgrade_id = upgrade["id"]
        if upgrade_id in game_state.upgrade_buttons:
            game_state.upgrade_buttons[upgrade_id].destroy()
            game_state.upgrade_buttons.pop(upgrade_id)

def total_passive_gain():
    return game_state.skeleton.passive_gain() + game_state.zombie.passive_gain()
    
def gain_souls(amount):
    game_state.souls = round(game_state.souls + (amount * game_state.souls_multiplier), 1)
    game_state.total_souls_gained = round(game_state.total_souls_gained + (amount * game_state.souls_multiplier), 1)

def spend_souls(cost):
    game_state.souls = round(game_state.souls - cost, 1)
    game_state.total_souls_spent = round(game_state.total_souls_spent + cost, 1)

def collect_soul_click():
    game_state.click_count += 1
    gain_souls(game_state.click_power)
    
def buy_undead(undead):
    if game_state.souls >= undead.cost:
        spend_souls(undead.cost)
        undead.buy()