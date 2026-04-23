import game_state
import math

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
        game_state.skeleton_power *= upgrade["effect_value"]
    elif upgrade["effect_type"] == "zombie_power":
        game_state.zombie_power *= upgrade["effect_value"]
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

def undead_passive_gain(undead_count, undead_power):
    return undead_count * undead_power

def total_passive_gain():
    return undead_passive_gain(game_state.skeleton_count, game_state.skeleton_power) + undead_passive_gain(game_state.zombie_count, game_state.zombie_power)
    
def gain_souls(amount):
    game_state.souls = round(game_state.souls + (amount * game_state.souls_multiplier), 1)
    game_state.total_souls_gained = round(game_state.total_souls_gained + (amount * game_state.souls_multiplier), 1)

def spend_souls(cost):
    game_state.souls = round(game_state.souls - cost, 1)
    game_state.total_souls_spent = round(game_state.total_souls_spent + cost, 1)

def collect_soul_click():
    game_state.click_count += 1
    gain_souls(game_state.click_power)
    
def buy_skeleton():
    if game_state.souls >= game_state.skeleton_cost:
        spend_souls(game_state.skeleton_cost)
        game_state.skeleton_count += 1
        game_state.skeleton_cost = math.ceil(game_state.skeleton_cost * 1.3)
       
def buy_zombie():
    if game_state.souls >= game_state.zombie_cost:
        spend_souls(game_state.zombie_cost)
        game_state.zombie_count += 1
        game_state.zombie_cost = math.ceil(game_state.zombie_cost * 1.3)

def build_save_dictionary():
    save_dictionary = {"tick_rate": game_state.tick_rate,
                       "tick_count": game_state.tick_count,
                       "souls": game_state.souls,
                       "souls_multiplier": game_state.souls_multiplier,
                       "total_souls_gained": game_state.total_souls_gained,
                       "total_souls_spent": game_state.total_souls_spent,
                       "click_count": game_state.click_count,
                       "click_power": game_state.click_power,
                       "skeleton_count": game_state.skeleton_count,
                       "skeleton_cost": game_state.skeleton_cost,
                       "skeleton_power": game_state.skeleton_power,
                       "zombie_count": game_state.zombie_count,
                       "zombie_cost": game_state.zombie_cost,
                       "zombie_power": game_state.zombie_power,
                       "upgrades_status": {
                           
                       }
                       }
    upgrades_status = save_dictionary["upgrades_status"]
    for upgrade in game_state.upgrades:
        upgrade_id = upgrade["id"]
        upgrade_bought = upgrade["bought"]
        upgrades_status[str(upgrade_id)] = upgrade_bought
    return save_dictionary

def load_save_from_dictionary(save_dictionary):
    game_state.tick_rate = int(save_dictionary["tick_rate"])
    game_state.tick_count = int(save_dictionary["tick_count"])
    game_state.souls = float(save_dictionary["souls"])
    game_state.souls_multiplier = float(save_dictionary["souls_multiplier"])
    game_state.total_souls_gained = float(save_dictionary["total_souls_gained"])
    game_state.total_souls_spent = float(save_dictionary["total_souls_spent"])
    game_state.click_count = int(save_dictionary["click_count"])
    game_state.click_power = float(save_dictionary["click_power"])
    game_state.skeleton_count = int(save_dictionary["skeleton_count"])
    game_state.skeleton_cost = int(save_dictionary["skeleton_cost"])
    game_state.skeleton_power = float(save_dictionary["skeleton_power"])
    game_state.zombie_count = int(save_dictionary["zombie_count"])
    game_state.zombie_cost = int(save_dictionary["zombie_cost"])
    game_state.zombie_power = float(save_dictionary["zombie_power"])

    upgrades_saved = save_dictionary["upgrades_status"]
    for saved in upgrades_saved:
        saved_id = int(saved)
        saved_status = upgrades_saved[saved]
        upgrade_current = game_state.upgrades[saved_id-1]
        if saved_status:
            upgrade_current["bought"] = True
        else:
            upgrade_current["bought"] = False