import tkinter as tk
from tkinter import messagebox
from threading import Thread
import subprocess
import sys
import os

def run_scraper(url_template):
    try:
        subprocess.run(
            [sys.executable, "-m", "pytest", "scraper.py"],
            check=True,
            env={**os.environ, "URL_TEMPLATE": url_template}
        )
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Scraper failed.\n{e}")

def on_start():
    url_template = url_entry.get().strip()
    thread = Thread(target=run_scraper, args=(url_template,))
    thread.start()

# --- GUI ---
root = tk.Tk()
root.title("Amazon Scraper")
root.geometry("500x220")

label = tk.Label(root, text="Enter Amazon URL Template (with *):", font=("Arial", 12))
label.pack(pady=10)

url_entry = tk.Entry(root, width=70)
url_entry.insert(0, "https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry/zgbs/fashion/ref=zg_bs_pg_*_fashion?_encoding=UTF8&pg=*")
url_entry.pack(pady=5)

start_button = tk.Button(root, text="Start Scraper", command=on_start, font=("Arial", 12))
start_button.pack(pady=10)

root.mainloop()
