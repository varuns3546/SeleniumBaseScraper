import tkinter as tk
from tkinter import simpledialog, messagebox
import json

def get_config():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    base_url = simpledialog.askstring("Base URL", "Enter the base URL:")
    sleep_time = simpledialog.askfloat("Sleep Time", "Enter sleep time in seconds:", minvalue=0.1)

    if not base_url or sleep_time is None:
        messagebox.showerror("Input Error", "Both fields are required.")
        return

    config = {
        "base_url": base_url,
        "sleep_time": sleep_time
    }

    with open("config.json", "w") as f:
        json.dump(config, f)

    messagebox.showinfo("Saved", "Configuration saved successfully!")

if __name__ == "__main__":
    get_config()
