# Just a small app that acts as a mouse jiggler

import pyautogui
import tkinter as tk
from threading import Thread
from random import randrange
import time

class StealthJiggler:
    def __init__(self, root):
        self.root = root
        self.root.title("System Pulse")
        self.root.geometry("250x150")
        self.running = False

        # UI Elements
        self.label = tk.Label(root, text="Status: IDLE", fg="gray")
        self.label.pack(pady=10)

        self.start_btn = tk.Button(root, text="Start Stealth Mode", command=self.start)
        self.start_btn.pack(pady=5)

        self.stop_btn = tk.Button(root, text="Stop", command=self.stop, state=tk.DISABLED)
        self.stop_btn.pack(pady=5)

    def jiggle_logic(self):
        while self.running:
            # Move only 1 pixel in a random direction (virtually invisible)
            x = randrange(-1, 2)
            y = randrange(-1, 2)
            pyautogui.move(x, y, duration=0.1)
            
            # Random wait between 30 and 90 seconds to avoid a rhythmic pattern
            wait_time = randrange(30, 91)
            
            # Check every second if we should stop during the wait period
            for _ in range(wait_time):
                if not self.running:
                    break
                time.sleep(1)

    def start(self):
        self.running = True
        self.label.config(text="Status: ACTIVE (Stealth)", fg="green")
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        # Run the loop in a separate thread so the GUI doesn't freeze
        self.thread = Thread(target=self.jiggle_logic, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        self.label.config(text="Status: IDLE", fg="gray")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = StealthJiggler(root)
    root.mainloop()
