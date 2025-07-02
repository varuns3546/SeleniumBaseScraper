import sqlite3
import json

conn = sqlite3.connect('data.db')

cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

for table_name in tables:
    cursor.execute(f"DROP TABLE IF EXISTS {table_name[0]}")


cursor.execute('''
    CREATE TABLE IF NOT EXISTS query_types (
        id INTEGER PRIMARY KEY,
        title TEXT UNIQUE NOT NULL
    )
    ''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS query_type_fields (
        id INTEGER PRIMARY KEY,
        query_type_id INTEGER NOT NULL,
        field_name TEXT NOT NULL,
        field_type TEXT NOT NULL,
        FOREIGN KEY (query_type_id) REFERENCES query_types(id) ON DELETE CASCADE
    )
    ''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS queries (
        id INTEGER PRIMARY KEY,
        query_type_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        parameters_json TEXT,
        FOREIGN KEY (query_type_id) REFERENCES query_types(id) ON DELETE CASCADE
    )
    ''')
    
cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY,
        query_id INTEGER NOT NULL,
        title TEXT,
        data_json TEXT,
        FOREIGN KEY (query_id) REFERENCES queries(id) ON DELETE CASCADE
    )
''')

cursor.execute("INSERT INTO query_types (title) VALUES (?)", ("get_url_list",))

# Get the query_type_id for "get_url_list"
cursor.execute("SELECT id FROM query_types WHERE title = ?", ("get_url_list",))
row = cursor.fetchone()

query_type_id = row[0]

fields = [
    ("title", "string"),
    ("url", "string"),
    ("sleep_time", "float"),
    ("item_selector", "string"),
    ("pagination", "string"),
    ("scroll_rate", "int"),
    ("pagination_button_selector", "string"),
]

for field_name, field_type in fields:
    cursor.execute(
        "INSERT OR IGNORE INTO query_type_fields (query_type_id, field_name, field_type) VALUES (?, ?, ?)",
        (query_type_id, field_name, field_type)
    )
parameters = {
    "title": "Amazon Home and Kitchen Best Sellers",
    "url": "https://www.amazon.com/Best-Sellers-Home-Kitchen/zgbs/home-garden/ref=zg_bs_pg_*_home-garden?_encoding=UTF8&pg=*",
    "sleep_time": ".75",
    "item_selector": 'a.a-link-normal.aok-block[role="link"]:not(.a-text-normal)',
    "pagination": "url",
    "scroll_rate": "",
    "pagination_button_selector": ""
}

# Convert dict to JSON string
parameters_json = json.dumps(parameters)

# Insert new query into queries table
cursor.execute(
    "INSERT INTO queries (query_type_id, title, parameters_json) VALUES (?, ?, ?)",
    (query_type_id, "Amazon Best Sellers in Home and Kitchen", parameters_json)
)
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cursor.fetchall())

conn.commit()
conn.close()
