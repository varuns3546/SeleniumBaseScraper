import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from threading import Thread
import subprocess
import sys
import os
import sqlite3 

def run_scraper(title):
    conn = sqlite3.connect('queries.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM get_url_list_queries WHERE title = ?", (title,))
    #query id is first item in tuple from cursor.fetchone()
    query_id = str(cursor.fetchone()[0])

    conn.close()

    try:
        subprocess.run(
            [sys.executable, "-m", "pytest", "-s", "scraper.py"],
            check=True,
            env={**os.environ,
                 "QUERY_ID": query_id
                }
        )
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Scraper failed.\n{e}")

def on_start():
    title = title_entry.get()
    url_template = url_entry.get().strip()
    sleep_time = sleep_entry.get().strip()
    item_selector = item_selector_entry.get().replace(" ", ".")
    pagination = selected_pagination.get().lower()
    
    
    if not url_template or not item_selector or not pagination:
        messagebox.showerror("Input Error", "missing fields")
        return

    try:
        float(sleep_time)
    except ValueError:
        messagebox.showerror("Input Error", "Sleep time must be a number.")
        return

    save_query()
    
    thread = Thread(target=run_scraper(title))
    thread.start()

def save_query():
    title = title_entry.get()
    url_template = url_entry.get().strip()
    sleep_time = sleep_entry.get().strip()
    item_selector = item_selector_entry.get().replace(" ", ".")
    pagination = selected_pagination.get().lower()
    scroll_rate = scroll_entry.get()
    pag_btn_selector = pag_btn_selector_entry.get() 
    conn = sqlite3.connect('queries.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM get_url_list_queries WHERE title = ?", (title,))
    result = cursor.fetchone()

    if result:
        cursor.execute("""
            UPDATE get_url_list_queries
            SET url_template = ?, sleep_time = ?, item_selector = ?, pagination = ?,
                       scroll_rate = ?, pagination_button_selector = ?
                       WHERE title = ?
        """, (url_template, sleep_time, item_selector, pagination, scroll_rate, pag_btn_selector, title))
    else:
        cursor.execute("""
            INSERT INTO get_url_list_queries (title, url_template, sleep_time, item_selector, 
                       pagination, scroll_rate, pagination_button_selector)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (title, url_template, sleep_time, item_selector, pagination, scroll_rate, pag_btn_selector))
    conn.commit()
    conn.close()

def load_queries():
    conn = sqlite3.connect('queries.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title, url_template, sleep_time, item_selector, pagination, " \
    "scroll_rate, pagination_button_selector FROM get_url_list_queries")
    rows = cursor.fetchall()

    queries = []
    for row in rows:
        queries.append({'title': row[0], 'url_template': row[1], 'sleep_time': row[2], 'item_selector': row[3], 
                        'pagination': row[4], 'scroll_rate': row[5], 'pagination_button_selector': row[6]})
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

            item_selector_entry.delete(0, tk.END)
            item_selector_entry.insert(0, query['item_selector'])
            
            pagination_dropdown.setvar(query["pagination"])
           
            scroll_entry.delete(0, tk.END)
            scroll_entry.insert(0, query['scroll_rate'])

            pag_btn_selector_entry.delete(0, tk.END)
            pag_btn_selector_entry.insert(0, query['pagination_button_selector'])

            break

# --- GUI ---
root = tk.Tk()
root.title("Web Scraper")
root.geometry("1000x400")
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

url_list_tab = ttk.Frame(notebook)
notebook.add(url_list_tab, text="Get URL List")

query_dropdown_label = tk.Label(url_list_tab, text="Load Saved Query")
title_label = tk.Label(url_list_tab, text="Query Title")
url_label = tk.Label(url_list_tab, text="URL Template (with * for pagination):")
sleep_label = tk.Label(url_list_tab, text="Sleep Time")
item_selector_label = tk.Label(url_list_tab, text="Item Selector")
pagination_label = tk.Label(url_list_tab, text="Select Pagination")
scroll_label = tk.Label(url_list_tab, text="Scroll Rate")
pag_btn_selector_label = tk.Label(url_list_tab, text="Button Pagination Selector")

saved_queries = load_queries()
query_options = [q['title'] for q in saved_queries] if saved_queries else ["No saved queries"]

selected_query = tk.StringVar(value=query_options[0])
query_dropdown = ttk.OptionMenu(url_list_tab, selected_query, query_options[0], *query_options, command=on_query_selected)

title_entry = tk.Entry(url_list_tab, width=80)
url_entry = tk.Entry(url_list_tab, width=150)
sleep_entry = tk.Entry(url_list_tab, width=80)
item_selector_entry =tk.Entry(url_list_tab, width=80)
pagination_options = ["URL", "Button", "Vertical Scroll", "Horizontal Scroll"]
selected_pagination = tk.StringVar(value=pagination_options[0])
pagination_dropdown = ttk.OptionMenu(url_list_tab, selected_pagination, pagination_options[0], *pagination_options)
scroll_entry=tk.Entry(url_list_tab, width=80)
pag_btn_selector_entry = tk.Entry(url_list_tab, width=80)
start_btn = tk.Button(url_list_tab, text="Start Scraper", command=on_start, font=("Arial", 12))
save_btn = tk.Button(url_list_tab, text="Save Query", command=save_query, font=("Arial", 12))

query_dropdown_label.grid(row=0, column=0)
title_label.grid(row=1, column=0)
url_label.grid(row=2, column=0)
sleep_label.grid(row=3, column=0)
item_selector_label.grid(row=4, column=0)
pagination_label.grid(row=5, column=0)
scroll_label.grid(row=6, column=0)
pag_btn_selector_label.grid(row=7, column=0)

query_dropdown.grid(row=0, column=1, sticky="w")
title_entry.grid(row=1, column=1, sticky="w")
url_entry.grid(row=2, column=1, sticky="w")
sleep_entry.grid(row=3, column=1, sticky="w")
item_selector_entry.grid(row=4, column=1, sticky="w")
pagination_dropdown.grid(row=5, column=1, sticky='w')
scroll_entry.grid(row=6, column=1, sticky='w')
pag_btn_selector_entry.grid(row=7, column=1, sticky='w')


start_btn.grid(row=9, column=0)
save_btn.grid(row=9, column=1)



root.mainloop()
