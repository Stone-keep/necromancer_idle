background_color = "black"
soul_color = "#9fe8d8"
text_color = "#e6fff8"
button_background = "#1a1a1a"
button_active_background = "#25443d"
notification_upgrade_color = "#7CFF7C"
notification_undead_color = "#ce4141"
souls_font = ("Cambria", 25, "bold")
souls_passive_font = ("Cambria", 20)
collect_button_font = ("Cambria", 18, "bold")
button_font = ("Cambria", 12, "bold")
undead_label_font = ("Cambria", 16, "bold")
undead_stats_font = ("Cambria", 16)
stats_label_font = ("Cambria", 14, "bold")
stats_dynamic_font = ("Cambria", 14)
undead_button_label_font = ("Cambria", 12)
info_font = ("Cambria", 13)
notification_font = ("Cambria", 12, "bold")

collect_button_style = {
    "bg": button_background,
    "fg": soul_color,
    "activebackground": button_active_background,
    "activeforeground": "white",
    "relief": "ridge",
    "bd": 2,
    "font": collect_button_font,
    "padx": 10,
    "pady": 6
}

shop_button_style = {
    "bg": button_background,
    "fg": "#e6fff8",
    "activebackground": button_active_background,
    "activeforeground": "white",
    "relief": "ridge",
    "bd": 2,
    "font": button_font,
    "width": 18
}

info_text = """Welcome, aspiring necromancer. Your goal is to gather one billion souls to summon the Undead King and harness his power to rule the world.

First you need to collect Souls manually (by clicking "Gather Souls" button). Use those Souls to raise Undead minions (you will unlock more as the game goes on). They will do your bidding, passively generating Souls... which you can spend to raise more of them, or buy permanent upgrades.

New upgrades show up in "Upgrades" tab when certain conditions are met (such as raising 10 of a specific Undead, clicking X times or after a certain amount of time passes). You will get notified whenever a new upgrade is available.

You can also view your progress in "Stats" tab.

This is my first personal project created with Python/Tkinter. If you want to learn more, check out README.md. Enjoy!"""