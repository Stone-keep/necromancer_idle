import tkinter as tk

# Game variables
souls = 0
skeleton_count = 0
skeleton_cost = 1

# Functions
def game_loop():
    root.after(1000, game_loop)

def collect_soul():
    global souls
    souls = round(souls + 0.1, 1)
    souls_label.config(text=f"Souls: {souls:.1f}")

def buy_skeleton():
    global souls
    global skeleton_cost
    global skeleton_count
    if souls >= skeleton_cost:
        souls = round(souls - skeleton_cost, 1)
        skeleton_count += 1
        souls_label.config(text=f"Souls: {souls:.1f}")
        skeletons_label.config(text=f"Skeletons: {skeleton_count}")


# UI setup
root = tk.Tk()
root.title("Necromancer Idle")
root.geometry("300x200")

souls_label = tk.Label(root, text="Souls: 0", font=("Arial", 16))
souls_label.pack(pady=20)

skeletons_label = tk.Label(root, text="Skeletons: 0", font=("Arial", 16))
skeletons_label.pack(pady=20)

collect_button = tk.Button(root, text="Collect Soul", command=collect_soul)
collect_button.pack()

buy_skeleton_button = tk.Button(root, text="Buy Skeleton", command=buy_skeleton)
buy_skeleton_button.pack()

game_loop()
root.mainloop()