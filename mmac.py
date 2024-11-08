import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import keyboard
import threading
import time
from datetime import datetime
import json

class MouseAutoClicker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MMAC - Minimal Mouse Auto Clicker")
        self.root.resizable(False, False)
        
        # Initialize variables
        self.running = False
        self.click_count = 0
        self.current_thread = None
        self.use_current_position = tk.BooleanVar(value=True)
        
        # Configure PyAutoGUI
        pyautogui.FAILSAFE = True
        
        self.setup_gui()
        self.setup_hotkeys()
        
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Click Type Section
        click_frame = ttk.LabelFrame(main_frame, text="Click Settings", padding="5")
        click_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Mouse Button Selection
        ttk.Label(click_frame, text="Mouse Button:").grid(row=0, column=0, sticky=tk.W)
        self.button_type = ttk.Combobox(click_frame, values=["Left", "Right", "Middle"], state="readonly")
        self.button_type.set("Left")
        self.button_type.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # Click Type Selection
        ttk.Label(click_frame, text="Click Type:").grid(row=1, column=0, sticky=tk.W)
        self.click_type = ttk.Combobox(click_frame, values=["Single", "Double", "Triple"], state="readonly")
        self.click_type.set("Single")
        self.click_type.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # Interval Section
        interval_frame = ttk.LabelFrame(main_frame, text="Interval Settings", padding="5")
        interval_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Interval Input
        ttk.Label(interval_frame, text="Interval:").grid(row=0, column=0, sticky=tk.W)
        self.interval_value = ttk.Entry(interval_frame, width=10)
        self.interval_value.insert(0, "1.0")
        self.interval_value.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        self.interval_unit = ttk.Combobox(interval_frame, 
                                        values=["milliseconds", "seconds", "minutes", "hours"],
                                        state="readonly", width=10)
        self.interval_unit.set("seconds")
        self.interval_unit.grid(row=0, column=2, sticky=tk.W, padx=5)
        
        # Position Section
        position_frame = ttk.LabelFrame(main_frame, text="Position Settings", padding="5")
        position_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Position Type
        ttk.Radiobutton(position_frame, text="Current Position", 
                       variable=self.use_current_position, value=True).grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(position_frame, text="Fixed Position", 
                       variable=self.use_current_position, value=False).grid(row=1, column=0, sticky=tk.W)
        
        # Coordinates Input
        coord_frame = ttk.Frame(position_frame)
        coord_frame.grid(row=1, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(coord_frame, text="X:").grid(row=0, column=0)
        self.x_coord = ttk.Entry(coord_frame, width=6)
        self.x_coord.insert(0, "0")
        self.x_coord.grid(row=0, column=1, padx=2)
        
        ttk.Label(coord_frame, text="Y:").grid(row=0, column=2)
        self.y_coord = ttk.Entry(coord_frame, width=6)
        self.y_coord.insert(0, "0")
        self.y_coord.grid(row=0, column=3, padx=2)
        
        # Get Current Position Button
        ttk.Button(position_frame, text="Get Current Position", 
                  command=self.get_current_position).grid(row=2, column=0, columnspan=2, pady=5)
        
        # Control Section
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="5")
        control_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Start/Stop Button
        self.start_stop_btn = ttk.Button(control_frame, text="Start (F6)", command=self.toggle_clicking)
        self.start_stop_btn.grid(row=0, column=0, padx=5)
        
        # Click Counter
        self.counter_label = ttk.Label(control_frame, text="Clicks: 0")
        self.counter_label.grid(row=0, column=1, padx=5)
        
        # Status
        self.status_label = ttk.Label(control_frame, text="Status: Stopped", foreground="red")
        self.status_label.grid(row=0, column=2, padx=5)
        
    def setup_hotkeys(self):
        keyboard.on_press_key("F6", lambda _: self.toggle_clicking())
        keyboard.on_press_key("F7", lambda _: self.stop_clicking())
        
    def get_current_position(self):
        time.sleep(3)  # Give user time to position the mouse
        x, y = pyautogui.position()
        self.x_coord.delete(0, tk.END)
        self.x_coord.insert(0, str(x))
        self.y_coord.delete(0, tk.END)
        self.y_coord.insert(0, str(y))
        
    def get_interval_in_seconds(self):
        try:
            value = float(self.interval_value.get())
            unit = self.interval_unit.get()
            
            if unit == "milliseconds":
                return value / 1000
            elif unit == "seconds":
                return value
            elif unit == "minutes":
                return value * 60
            elif unit == "hours":
                return value * 3600
                
        except ValueError:
            messagebox.showerror("Error", "Invalid interval value")
            return None
            
    def perform_click(self):
        button = self.button_type.get().lower()
        click_type = self.click_type.get().lower()
        
        if not self.use_current_position.get():
            try:
                x = int(self.x_coord.get())
                y = int(self.y_coord.get())
                pyautogui.moveTo(x, y)
            except ValueError:
                messagebox.showerror("Error", "Invalid coordinates")
                return
        
        clicks = 1
        if click_type == "double":
            clicks = 2
        elif click_type == "triple":
            clicks = 3
            
        pyautogui.click(button=button, clicks=clicks)
        self.click_count += 1
        self.counter_label.config(text=f"Clicks: {self.click_count}")
        
    def clicking_loop(self):
        interval = self.get_interval_in_seconds()
        if interval is None:
            return
            
        while self.running:
            self.perform_click()
            time.sleep(interval)
            
    def toggle_clicking(self):
        if not self.running:
            self.running = True
            self.start_stop_btn.config(text="Stop (F7)")
            self.status_label.config(text="Status: Running", foreground="green")
            self.current_thread = threading.Thread(target=self.clicking_loop)
            self.current_thread.daemon = True
            self.current_thread.start()
        else:
            self.stop_clicking()
            
    def stop_clicking(self):
        self.running = False
        self.start_stop_btn.config(text="Start (F6)")
        self.status_label.config(text="Status: Stopped", foreground="red")
        if self.current_thread:
            self.current_thread.join(timeout=1.0)
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MouseAutoClicker()
    app.run()
