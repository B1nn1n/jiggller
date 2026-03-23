# Just a small app that acts as a mouse jiggler

import pyautogui
import tkinter as tk
from threading import Thread
from random import randrange
import time
import sys
import pystray
from PIL import Image, ImageDraw

class StealthJiggler:
    def __init__(self, root):
        self.root = root
        self.root.title("System Pulse")
        self.root.geometry("300x150")
        self.running = False

        # UI Elements
        self.label = tk.Label(root, text="Status: IDLE", font=("Arial", 10))
        self.label.pack(pady=20)

        self.start_btn = tk.Button(root, text="Start Stealth Mode", command=self.start, width=20)
        self.start_btn.pack(pady=5)

        # Handle window closing (minimize to tray instead of quitting)
        self.root.protocol('WM_DELETE_WINDOW', self.hide_window)

    def create_image(self):
        # Generate a simple icon for the system tray (a blue circle)
        width, height = 64, 64
        image = Image.new('RGB', (width, height), (255, 255, 255))
        dc = ImageDraw.Draw(image)
        dc.ellipse((10, 10, 54, 54), fill=(0, 120, 215))
        return image

    def jiggle_logic(self):
        while self.running:
            # Micro-movement (1 pixel)
            x, y = randrange(-1, 2), randrange(-1, 2)
            pyautogui.move(x, y, duration=0.1)
            
            # Random sleep (30-90s) for non-robotic behavior
            wait_time = randrange(30, 91)
            for _ in range(wait_time):
                if not self.running:
                    break
                time.sleep(1)

    def start(self):
        if not self.running:
            self.running = True
            self.label.config(text="Status: ACTIVE", fg="green")
            self.start_btn.config(text="Stop Jiggler", command=self.stop)
            self.thread = Thread(target=self.jiggle_logic, daemon=True)
            self.thread.start()

    def stop(self):
        self.running = False
        self.label.config(text="Status: IDLE", fg="black")
        self.start_btn.config(text="Start Stealth Mode", command=self.start)

    def hide_window(self):
        self.root.withdraw() # Hide the taskbar window
        self.setup_tray()

    def show_window(self):
        self.tray_icon.stop() # Stop the tray icon
        self.root.after(0, self.root.deiconify) # Bring window back

    def quit_app(self):
        self.running = False
        self.tray_icon.stop()
        self.root.quit()

    def setup_tray(self):
        menu = (
            pystray.MenuItem('Show Settings', self.show_window),
            pystray.MenuItem('Quit', self.quit_app)
        )
        self.tray_icon = pystray.Icon("SystemPulse", self.create_image(), "System Pulse", menu)
        # Run tray icon in its own thread
        Thread(target=self.tray_icon.run, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = StealthJiggler(root)
    root.mainloop()
