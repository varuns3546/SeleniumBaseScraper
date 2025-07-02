import tkinter as tk
from tkinter import ttk
import sqlite3

class Get_URL_Lists_Page:
    def __init__(self, root, handlers):
        self.page = tk.Frame(root)
    
        self.on_query_selected = handlers["on_query_selected"]
        self.on_start = handlers["on_start"]
        self.save_query = handlers["save_query"]
        self.delete_query = handlers["delete_query"]
        self.load_queries = handlers["load_queries"]

        self.create_page()

    
    def create_page(self):    
        self.query_dropdown_label = tk.Label(self.page, text="Load Saved Query")
        self.title_label = tk.Label(self.page, text="Query Title")
        self.url_label = tk.Label(self.page, text="URL Template (with * for pagination):")
        self.sleep_label = tk.Label(self.page, text="Sleep Time")
        self.item_selector_label = tk.Label(self.page, text="Item Selector")
        self.pagination_label = tk.Label(self.page, text="Select Pagination")
        self.scroll_label = tk.Label(self.page, text="Scroll Rate")
        self.pag_btn_selector_label = tk.Label(self.page, text="Button Pagination Selector")

        self.saved_queries = self.load_queries()
        query_options = None
        if self.saved_queries:
            query_options = ["New Query"] + [q['title'] for q in self.saved_queries]
        else:
            query_options = ["New Query"]

        self.selected_query = tk.StringVar(value=query_options[0])
        self.query_dropdown = ttk.OptionMenu(self.page, self.selected_query, query_options[0], *query_options, command=self.on_query_selected)

        self.title_entry = tk.Entry(self.page, width=80)
        self.url_entry = tk.Entry(self.page, width=150)
        self.sleep_entry = tk.Entry(self.page, width=80)
        self.item_selector_entry =tk.Entry(self.page, width=80)

        self.scroll_entry=tk.Entry(self.page, width=80)
        self.pag_btn_selector_entry = tk.Entry(self.page, width=80)

        self.pagination_options = ["URL", "Button", "Vertical Scroll", "Horizontal Scroll"]
        self.selected_pagination = tk.StringVar(value=self.pagination_options[0])
        self.selected_pagination.trace_add("write", self.on_pagination_changed)
        self.pagination_dropdown = ttk.OptionMenu(self.page, self.selected_pagination, self.pagination_options[0], *self.pagination_options)

        self.start_btn = tk.Button(self.page, text="Start Scraper", command=self.on_start)
        self.save_btn = tk.Button(self.page, text="Save Query", command=self.save_query)
        self.delete_btn = tk.Button(self.page, text="Delete Query", command=self.delete_query)
        self.query_dropdown_label.grid(row=0, column=0)
        self.title_label.grid(row=1, column=0)
        self.url_label.grid(row=2, column=0)
        self.sleep_label.grid(row=3, column=0)
        self.item_selector_label.grid(row=4, column=0)
        self.pagination_label.grid(row=5, column=0)
        self.scroll_label.grid(row=6, column=0)

        self.query_dropdown.grid(row=0, column=1, sticky="w")
        self.title_entry.grid(row=1, column=1, sticky="w")
        self.url_entry.grid(row=2, column=1, sticky="w")
        self.sleep_entry.grid(row=3, column=1, sticky="w")
        self.item_selector_entry.grid(row=4, column=1, sticky="w")
        self.pagination_dropdown.grid(row=5, column=1, sticky='w')
        self.scroll_entry.grid(row=6, column=1, sticky='w')


        self.start_btn.grid(row=9, column=0)
        self.save_btn.grid(row=9, column=1)
        self.delete_btn.grid(row=9, column=2)


    def on_pagination_changed(self, *args):
        if self.selected_pagination.get() == "Button":
            self.pag_btn_selector_label.grid(row=7, column=0)
            self.pag_btn_selector_entry.grid(row=7, column=1, sticky='w')
        else:
            self.pag_btn_selector_label.grid_remove()
            self.pag_btn_selector_entry.grid_remove()

    
