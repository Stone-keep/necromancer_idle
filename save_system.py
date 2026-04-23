import game_state

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