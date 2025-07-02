import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from threading import Thread
import subprocess
import sys
import os
import sqlite3 

from UI.get_url_lists_page import Get_URL_Lists_Page
def run_scraper(title):
    conn = sqlite3.connect('queries.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM queries WHERE title = ?", (title,))
    #query id is first item in tuple from cursor.fetchone()
    query_id = str(cursor.fetchone()[0])

    conn.close()

    try:
        subprocess.run(
            [sys.executable, "-m", "pytest", "-s", "test_scraper.py"],
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

    global saved_queries
    saved_queries = load_queries()
    query_options = ["New Query"] + [q['title'] for q in saved_queries]
        
    # Rebuild the dropdown menu
    menu = query_dropdown["menu"]
    menu.delete(0, "end")
    for option in query_options:
        menu.add_command(label=option, command=lambda value=option: (selected_query.set(value), on_query_selected()))

    selected_query.set(title)
    on_query_selected()

def delete_query():
    selected_title = selected_query.get()

    if selected_title == "No saved queries":
        messagebox.showwarning("Warning", "No query selected to delete.")
        return

    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{selected_title}'?")
    if not confirm:
        return

    conn = sqlite3.connect('queries.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM get_url_list_queries WHERE title = ?", (selected_title,))
    conn.commit()
    conn.close()
    
    global saved_queries
    saved_queries = load_queries()
    query_options = None
    if saved_queries:
        query_options = ["New Query"] + [q['title'] for q in saved_queries]
    else:
        query_options = ["New Query"]    
    
    selected_query.set(query_options[0])

    on_query_selected()  # <-- Manually trigger the callback

    # Rebuild the dropdown menu
    menu = query_dropdown["menu"]
    menu.delete(0, "end")
    for option in query_options:
        menu.add_command(label=option, command=lambda value=option: (selected_query.set(value), on_query_selected()))


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

    if selected_title == "New Query":
        clear_fields()
    else:
        for query in saved_queries:
            if query['title'] == selected_title:
                clear_fields()
                title_entry.insert(0, query['title'])
                url_entry.insert(0, query['url_template'])
                sleep_entry.insert(0, query['sleep_time'])
                item_selector_entry.insert(0, query['item_selector'])
                pagination_dropdown.setvar(query["pagination"])
                scroll_entry.insert(0, query['scroll_rate'])
                pag_btn_selector_entry.insert(0, query['pagination_button_selector'])
                break

def clear_fields():
    title_entry.delete(0, tk.END)
    url_entry.delete(0, tk.END)
    sleep_entry.delete(0, tk.END)
    item_selector_entry.delete(0, tk.END)
    scroll_entry.delete(0, tk.END)
    pag_btn_selector_entry.delete(0, tk.END)
    pagination_dropdown.setvar(selected_pagination._name, pagination_options[0])


handlers = {
    "on_query_selected": on_query_selected,
    "on_start": on_start,
    "save_query": save_query,
    "delete_query": delete_query,
    "load_queries": load_queries
}

# --- GUI ---
root = tk.Tk()
root.title("Web Scraper")
root.geometry("1000x400")
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

get_url_lists_page = Get_URL_Lists_Page(notebook, handlers)

title_entry = get_url_lists_page.title_entry
url_entry = get_url_lists_page.url_entry
sleep_entry = get_url_lists_page.sleep_entry
item_selector_entry = get_url_lists_page.item_selector_entry
scroll_entry = get_url_lists_page.scroll_entry
pag_btn_selector_label = get_url_lists_page.pag_btn_selector_label
pag_btn_selector_entry = get_url_lists_page.pag_btn_selector_entry
pagination_options = get_url_lists_page.pagination_options
pagination_dropdown = get_url_lists_page.pagination_dropdown
selected_pagination = get_url_lists_page.selected_pagination
query_dropdown = get_url_lists_page.query_dropdown
selected_query = get_url_lists_page.selected_query
saved_queries = get_url_lists_page.saved_queries

notebook.add(get_url_lists_page.page, text="Get URL Lists")

root.mainloop()
