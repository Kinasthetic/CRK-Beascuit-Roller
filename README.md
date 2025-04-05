# CRK-Beascuit-Roller

---

Been tired of rolling beascuits mind-numblingly? Hate Devsis for not implementing this by now? Well it's your lucky day, since I did!

A customizable and easy-to-use tool designed to automate specific in-game actions based on stat templates. This program scans the CRK game screen, detects whether you rolled a purple/orange line, and clicks the "reset all" button automatically. This tool provides the flexibility to choose which stat to focus on for the automation.

### Features:
- **Dropdown selection**: Select the stat to track from a predefined list (e.g., ATK, DEF, HP, etc.).
- **Easy UI**: Clean and user-friendly interface with a blue theme.
- **Start/Stop functionality**: Easily start or stop the automation with a simple button click.
- **ESC key support**: Press ESC to stop the clicker at any time.
- **Always on top**: Option to keep the window always on top of other windows.
- **Log display**: See the stats being rolled and high-rarity hits in real-time.

### Requirements:
- **Python 3.x** (Recommended Python 3.7 or higher)
- **Required Libraries**:
  - `pyautogui` - for capturing screen and clicking buttons.
  - `pynput` - to listen for hotkeys.
  - `opencv-python` - for template matching.
  - `customtkinter` - for the GUI.
  - `PIL` - for image processing.

You can install the required libraries with:
```bash
pip install pyautogui pynput opencv-python customtkinter pillow
```

### Installation:
1. Clone or download the repository to your local machine.
2. Install Python and the necessary libraries using the command above.
3. Run the script `crk_beascuit_roller.py`.

### How to Use:

1. **Start the Program**:
   - Open the program and the GUI will appear.
   - The **Select Stat** dropdown will display a list of in-game stats (e.g., ATK, DEF, HP, etc.).
   
2. **Select the Stat**:
   - Choose the stat you wish to track from the dropdown. If no stat is selected, a prompt will appear asking you to select a stat before starting.

3. **Start the Autoclicker**:
   - Press the **▶ Start** button.
   - The button will change to **Press ESC to Stop**.
   - The program will begin scanning for the selected stat and clicking the "reset all" button if the stat matches the high-rarity (purple/orange) conditions.

4. **Stop the Autoclicker**:
   - Press **ESC** on your keyboard to stop the program.
   - The button will change back to **▶ Start**.

5. **Always on Top**:
   - You can check the **Always on top** checkbox to keep the window above all other windows.

### Usage Example:

1. Open the game and position it in the foreground. Make sure the 4 beascuit lines are displaying. If you want to keep it on top, resize it so that the 4 lines are in show.
2. Choose the stat you want to roll (e.g., **Poison DMG**).
3. Start the autoscanning process by clicking **▶ Start**.
4. The program will scan and click "reset all" when the required stat appears with the correct rarity.

### Troubleshooting:
- If the dropdown is not showing the stats, ensure the `stat_templates/` folder is populated with the correct template files.
- If the program doesn't detect the stat properly, try adjusting the template image or the template threshold.

### License:
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
Made with 💖 by rage.00 on Discord/Kinasthetic on CRK (Dark Cacao server)
