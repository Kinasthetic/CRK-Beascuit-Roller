import customtkinter as ctk
import threading
import keyboard
import pyautogui
import time
import numpy as np
from PIL import Image
from tkinter import simpledialog
import cv2
import os

# ---- Color Detection Settings ---- #
TEMPLATE_DIR = "stat_templates"
TEMPLATE_THRESHOLD = 0.7

def match_template(crop, template_path):
    crop_gray = cv2.cvtColor(np.array(crop.convert("RGB")), cv2.COLOR_RGB2GRAY)
    template = cv2.imread(template_path, 0)
    if template is None:
        return False
    res = cv2.matchTemplate(crop_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(res)
    print(f"🔍 Matching with {os.path.basename(template_path)}: {max_val:.3f}")
    return max_val >= TEMPLATE_THRESHOLD


VALUE_BOXES = [
    (1240, 490, 80, 35),
    (1240, 590, 80, 35),
    (1240, 690, 80, 35),
    (1240, 790, 80, 35),
]
RESET_ALL_POS = (1125, 940)


def get_bright_average_color(rgb_array, threshold=50):
    bright_pixels = rgb_array[(rgb_array > threshold).any(axis=-1)]
    return tuple(np.mean(bright_pixels, axis=0).astype(int)) if len(bright_pixels) > 0 else (0, 0, 0)


def is_purple(rgb):
    r, g, b = rgb
    return b > 100 and r > 40 and b > r + 20


def is_orange(rgb):
    r, g, b = rgb
    return r > 90 and g > 40 and b < 60


# ---- Autoclicker Logic ---- #
class AutoClicker(threading.Thread):  # Updated with stop flag fix
    def __init__(self, log_callback, update_counter_callback, selected_stat):
        super().__init__()
        self.running = False
        self.stop_requested = False
        self.log = log_callback
        self.update_counter = update_counter_callback
        self.selected_stat = selected_stat

    def run(self):
        self.running = True
        self.stop_requested = False
        self.log("\n▶ Starting in 5 seconds... switch to the game.")
        time.sleep(5)

        while self.running:

            screenshot = pyautogui.screenshot()
            hits = 0
            self.log("\n———————— New Roll ————————")

            for i, box in enumerate(VALUE_BOXES):
                x, y, w, h = 535, 480 + i * 100, 500, 80
                name_crop = screenshot.crop((x, y, x + w, y + h))
                matched = False
                selected = self.selected_stat.lower().replace(" ", "_").replace(".", "")
                for file in os.listdir(TEMPLATE_DIR):
                    if not file.lower().startswith(selected):
                        continue
                    template_path = os.path.join(TEMPLATE_DIR, file)
                    if match_template(name_crop, template_path):
                        matched = True
                        break
                if not matched:
                    self.log(f"[Row {i + 1}] ❌ No stat match. Skipping.")
                    continue

                x, y, w, h = box
                val_crop = screenshot.crop((x, y, x + w, y + h))
                rgb_array = np.array(val_crop.convert("RGB"))
                avg_color = get_bright_average_color(rgb_array)
                msg = f"[Row {i + 1}] Avg: ({avg_color[0]:>3}, {avg_color[1]:>3}, {avg_color[2]:>3})"

                if is_purple(avg_color):
                    msg += " → 🟣 PURPLE"
                    hits += 1
                elif is_orange(avg_color):
                    msg += " → 🟠 ORANGE"
                    hits += 1
                else:
                    msg += " → ⚪ Common"

                self.log(msg)

            self.log(f"— Total: {hits} high-rarity stats —")
            self.update_counter(hits)

            if hits >= 2:
                self.log("✨ Success! Requirement met.")
                self.stop_requested = True
                self.running = False
                break

            if self.stop_requested:
                break
            pyautogui.click(RESET_ALL_POS)
            time.sleep(1.0)

        self.log("⛔ Autoclicker stopped.")

    def stop(self):
        self.stop_requested = True
        self.running = False


# ---- GUI Layout ---- #
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Beascuit Autoclicker")
        self.geometry("700x625")
        self.credit_label = ctk.CTkLabel(self, text="💖 Made with love by rage.00 | Kinasthetic", font=("Courier", 12))
        self.credit_label.pack(side="bottom", anchor="se", pady=(5, 10), padx=10)
        # Always on top checkbox
        self.pin_var = ctk.BooleanVar(value=True)
        self.pin_checkbox = ctk.CTkCheckBox(self, text="📌 Always on top", variable=self.pin_var,
                                            command=self.toggle_pin)
        self.pin_checkbox.pack(pady=(10, 0))
        self.wm_attributes("-topmost", self.pin_var.get())  # Keep window always on top
        self.resizable(True, True)

        self.clicker = None
        self.bind("<Escape>", lambda event: self.stop_clicker())

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.start_btn = ctk.CTkButton(self, text="▶ Start", command=self.start_clicker)
        self.start_btn.pack(pady=(0, 10))

        self.log_box = ctk.CTkTextbox(self, width=600, height=360, font=("Courier", 12))
        self.log_box.pack(padx=10, pady=(10, 5))
        self.log_box.configure(state="disabled")

        self.counter_label = ctk.CTkLabel(self, text="High-rarity hits: 0", font=("Courier", 14))
        self.counter_label.pack(pady=(10, 5))

        self.template_selector_label = ctk.CTkLabel(self, text="Select Stat:")
        self.template_selector_label.pack(pady=(15, 0), before=self.start_btn)

        self.selected_stat = ctk.StringVar()
        all_stats = [
            "ATK", "DEF", "HP", "ATK SPD", "CRIT%", "DMG Resist", "CRIT Resist", "Cooldown",
            "Amplify Buff", "Debuff Resist", "DMG Resist Bypass",
            "Dark DMG", "Elec DMG", "Fire DMG", "Earth DMG",
            "Poison DMG", "Light DMG"
        ]
        self.stat_menu = ctk.CTkOptionMenu(self, variable=self.selected_stat, values=all_stats)
        self.stat_menu.pack(pady=(0, 15), before=self.start_btn)

    def log(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def update_counter(self, count):
        self.counter_label.configure(text=f"High-rarity hits: {count}")

    def start_clicker(self):
        selected_stat = self.selected_stat.get()

        # Check if a stat is selected
        if not selected_stat:
            simpledialog.messagebox.showwarning("Select a Stat", "Please select a stat before starting.")
            return  # Don't continue if a stat isn't selected

        if not self.clicker or not self.clicker.running:
            self.clicker = AutoClicker(self.log, self.update_counter, selected_stat)
            self.clicker.start()
            self.log("🟢 Autoclicker started.")
            self.start_btn.configure(text="Press ESC to Stop")

    # Change text and command

    def toggle_pin(self):
        self.wm_attributes("-topmost", self.pin_var.get())

    def stop_clicker(self):
        if self.clicker:
            self.clicker.stop()
            self.log("🛑 Stop requested.")
            self.start_btn.configure(text="▶ Start")  # Revert to Start button


def hotkey_listener(app_ref):
    def on_f12():
        print("F12 pressed - stopping clicker")
        app_ref.after(0, app_ref.stop_clicker)  # Global hotkey; schedule on main thread

    def on_escape():
        print("Escape pressed - stopping clicker")
        app_ref.after(0, app_ref.stop_clicker)  # Schedule on main thread

    keyboard.add_hotkey("f12", on_f12)
    keyboard.add_hotkey("escape", on_escape)
    keyboard.wait()

if __name__ == "__main__":
    app = App()
    threading.Thread(target=hotkey_listener, args=(app,), daemon=True).start()
    app.mainloop()
