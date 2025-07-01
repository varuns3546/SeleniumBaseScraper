import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from threading import Thread
import subprocess
import sys
import os
import csv

def run_scraper(url_template, sleep_time):
    try:
        subprocess.run(
            [sys.executable, "-m", "pytest", "scraper.py"],
            check=True,
            env={**os.environ,
                 "URL_TEMPLATE": url_template,
                 "SLEEP_TIME": sleep_time,
                }
        )
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Scraper failed.\n{e}")

def on_start():
    title = title_entry.get()
    url_template = url_entry.get().strip()
    sleep_time = sleep_entry.get().strip()
    
    if not url_template:
        messagebox.showerror("Input Error", "URL template required")
        return

    try:
        float(sleep_time)
    except ValueError:
        messagebox.showerror("Input Error", "Sleep time must be a number.")
        return

    save_query(title, url_template, sleep_time)
    
    thread = Thread(target=run_scraper)
    thread.start()

def save_query(title, url_template, sleep_time):
    file_exists = os.path.isfile('queries.csv')
    with open('queries.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['title', 'url_template', 'sleep_time'])
        writer.writerow([title, url_template, sleep_time])

# Function to load saved queries and populate dropdown
def load_queries():
    queries = []
    if os.path.exists('queries.csv'):
        with open('queries.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                queries.append(row)
    return queries

def on_query_selected(event=None):
    selected_title = selected_query.get()
    for query in saved_queries:
        if query['title'] == selected_title:
            title_entry.delete(0, tk.END)
            title_entry.insert(0, query['title'])

            url_entry.delete(0, tk.END)
            url_entry.insert(0, query['url_template'])

            sleep_entry.delete(0, tk.END)
            sleep_entry.insert(0, query['sleep_time'])
            break

# --- GUI ---
root = tk.Tk()
root.title("Amazon Scraper")
root.geometry("500x220")

title_label = tk.Label(root, text="Query Title")
url_label = tk.Label(root, text="Enter Amazon URL Template (with * for pagination):")
sleep_label = tk.Label(root, text="Sleep Time")
item_selector_label = tk.Label(root, text="Item Selector")
vert_scroll_label = tk.Label(root, text="Vertical Scroll")
horiz_scroll_label = tk.Label(root, text="Horizontal Scroll")
pag_selector_label = tk.Label(root, text="Button Pagination Selector")

title_entry = tk.Entry(root, width=30)
url_entry = tk.Entry(root, width=70)
sleep_entry = tk.Entry(root, width=30)
item_selector_entry =tk.Entry(root, width=50)
pag_selector_entry = tk.Entry(root, width=50)
url_pag_cb = tk.Checkbutton(root, text="URL Pagination")



start_button = tk.Button(root, text="Start Scraper", command=on_start, font=("Arial", 12))

# Load queries and setup dropdown
saved_queries = load_queries()
query_titles = [q['title'] for q in saved_queries] if saved_queries else ["No saved queries"]

selected_query = tk.StringVar(value=query_titles[0])
query_dropdown = ttk.OptionMenu(root, selected_query, query_titles[0], *query_titles, command=on_query_selected)

dropdown_label = tk.Label(root, text="Load Saved Query")

dropdown_label.grid(row=0, column=0)
title_label.grid(row=1, column=0)
url_label.grid(row=2, column=0)
sleep_label.grid(row=3, column=0)
item_selector_label.grid(row=4, column=0)


query_dropdown.grid(row=0, column=1)
title_entry.grid(row=1, column=1)
url_entry.grid(row=2, column=1)
sleep_entry.grid(row=3, column=1)
item_selector_entry.grid(row=4, column=1)

start_button.grid(row=7, column=0)


root.mainloop()
