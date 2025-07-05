import tkinter as tk 
from tkinter import ttk 
from pymongo import MongoClient 
from actions_data import navigations, interactions, assertions, waits, utilities 
import os
import sys

# Add the parent directory of `create_queries` to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from UI.get_url_lists_page import Get_URL_Lists_Page




# Lookup maps 
nav_map = {item["name"]: item for item in navigations} 
int_map = {item["name"]: item for item in interactions} 
assert_map = {item["name"]: item for item in assertions} 
wait_map = {item["name"]: item for item in waits} 
util_map = {item["name"]: item for item in utilities} 

# MongoDB setup 

# Track action entries 
action_widgets = [] 


def save_to_db():
    print("attempting to save to db")

    # Get the collection title
    title = title_entry.get()
    if not title:
        print("Error: Title cannot be empty.")
        return
    
   

    if not action_widgets:
        print("Error: No actions to save.")
        return

    # Connect to MongoDB
    client = MongoClient(os.getenv("MONGODB_URI"))
    db = client["query_db"]
    collection = db["queries"]

    if collection.find_one({"title": title}):
        print(f"Error: A query with the title '{title}' already exists.")
        return


    # Build the list of actions
    actions = []
    for widget in action_widgets:
        action_data = {
            "action": widget["action"],
            "parameters": [entry.get() for entry in widget["param_entries"]]
        }
        print(f"index: {action_data['index']} action: {action_data['action']}")
        for param in action_data["parameters"]:
            print(param)
        actions.append(action_data)

    # Save to MongoDB
    result = collection.insert_one({"title": title, "actions": actions})
    print("Saved to DB. Inserted ID:", result.inserted_id)

# GUI setup 
root = tk.Tk() 
root.title("Create Queries") 
root.geometry("1000x500")
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

main_page = tk.Frame(notebook)
notebook.add(main_page, text="Create Query")

# Expandable columns/rows 
main_page.grid_columnconfigure(0, weight=1) 
main_page.grid_columnconfigure(1, weight=1) 
main_page.grid_rowconfigure(7, weight=1) 
# Title input 
title_label = tk.Label(main_page, text="Collection title") 
title_entry = tk.Entry(main_page) 
title_label.grid(row=0, column=0) 
title_entry.grid(row=0, column=1) 
save_btn= tk.Button(main_page, text="Save Query", command=save_to_db) 
save_btn.grid(row=8) 

# Scrollable frame setup 
canvas = tk.Canvas(main_page, height=400) 
scrollbar = tk.Scrollbar(main_page, orient="vertical", command=canvas.yview) 
canvas.configure(yscrollcommand=scrollbar.set) 
canvas.grid(row=7, column=0, columnspan=2, sticky="nsew") 
scrollbar.grid(row=7,column=2, sticky="ns") 

def on_frame_configure(event): 
    canvas.configure(scrollregion=canvas.bbox("all")) 
scrollable_frame = tk.Frame(canvas) 
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", tags="inner_frame") 
scrollable_frame.bind("<Configure>", on_frame_configure) 
canvas.bind('<Configure>', lambda e: canvas.itemconfig("inner_frame", width=750)) 
scrollable_frame.bind("<Configure>", on_frame_configure) 
# Track row number 
current_row = 0 
def add_parameter_field(param_frame, param_entries): 
    entry = tk.Entry(param_frame, width=25) 
    entry.pack(side=tk.LEFT, padx=5) 
    param_entries.append(entry) 
def on_select(selected_action, method_map): 
    global current_row 
    method = method_map[selected_action] 
    param_count = method["parameter_count"]
    index = len(action_widgets) 
    action_frame = tk.Frame(scrollable_frame, borderwidth=1, relief="groove", pady=5) 
    row_frame = tk.Frame(action_frame) 
    row_frame.pack(fill="x", expand=True, padx=10) 
    label = tk.Label(row_frame, text=f"{index+1}: {selected_action}", width=40) 
    label.pack(side=tk.LEFT, padx=5) 
    param_frame = tk.Frame(row_frame) 
    param_frame.pack(side=tk.LEFT, padx=10) 
    param_entries = [] 
    for _ in range(param_count): 
        add_parameter_field(param_frame, param_entries) 
    def delete_action(): 
        action_frame.destroy() 
        action_widgets.remove(widget_data) 
        refresh_actions() 
    def move_up(): 
        i = action_widgets.index(widget_data) 
        if i > 0: 
            action_widgets[i], action_widgets[i - 1] = action_widgets[i - 1], action_widgets[i] 
            refresh_actions() 
    def move_down(): 
        i = action_widgets.index(widget_data) 
        if i < len(action_widgets) - 1: 
            action_widgets[i], action_widgets[i + 1] = action_widgets[i + 1], action_widgets[i] 
            refresh_actions() 
    # Buttons 
    del_button = tk.Button(row_frame, text="X", command=delete_action, fg="red", width=2) 
    del_button.pack(side=tk.RIGHT, padx=2) 
    down_button = tk.Button(row_frame, text="↓", command=move_down, width=2) 
    down_button.pack(side=tk.RIGHT, padx=2) 
    up_button = tk.Button(row_frame, text="↑", command=move_up, width=2) 
    up_button.pack(side=tk.RIGHT, padx=2) 
    widget_data = {
        "index": index, 
        "action": selected_action, 
        "param_entries": param_entries, 
        "frame": action_frame, 
        "label": label 
        } 
    action_widgets.append(widget_data) 
    refresh_actions()
def refresh_actions(): 
    for idx, widget_data in enumerate(action_widgets): 
        widget_data["index"] = idx 
        widget_data["label"].config(text=f"{idx+1}: {widget_data['action']}") 
        widget_data["frame"].grid(row=idx, column=0, columnspan=2, padx=5, pady=5, sticky="ew") 
def create_dropdown(label_text, values, row, method_map): 
    label = tk.Label(main_page, text=label_text) 
    label.grid(row=row, column=0, sticky="e", padx=10, pady=5) 
    var = tk.StringVar() 
    dropdown = ttk.Combobox(main_page, textvariable=var, values=values, state="readonly") 
    dropdown.grid(row=row, column=1, sticky="ew", padx=10, pady=5) 
    dropdown.bind("<<ComboboxSelected>>", lambda event: on_select(var.get(), method_map))
    return var
     # Dropdowns 
nav_var = create_dropdown("navigation", [item["name"] for item in navigations], 2, nav_map) 
int_var = create_dropdown("interaction", [item["name"] for item in interactions], 3, int_map) 
assert_var = create_dropdown("assertion", [item["name"] for item in assertions], 4, assert_map) 
wait_var = create_dropdown("wait", [item["name"] for item in waits], 5, wait_map) 
util_var = create_dropdown("utility", [item["name"] for item in utilities], 6, util_map) 
root.mainloop()



















