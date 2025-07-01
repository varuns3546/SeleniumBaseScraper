import sqlite3

conn = sqlite3.connect('queries.db')

cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS get_url_list_queries")

cursor.execute('''
    CREATE TABLE IF NOT EXISTS get_url_list_queries (
        id INTEGER PRIMARY KEY,
        title TEXT UNIQUE NOT NULL,
        url_template TEXT NOT NULL,
        sleep_time FLOAT NOT NULL,
        item_selector TEXT NOT NULL,
        pagination TEXT,
        scroll_rate FLOAT,
        pagination_button_selector TEXT
    )
    ''')
    
try:
    cursor.execute("DROP TABLE IF EXISTS items")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY,
            query_id INTEGER NOT NULL,
            title TEXT,
            url TEXT UNIQUE NOT NULL,
            FOREIGN KEY (query_id) REFERENCES queries(id) ON DELETE CASCADE
        )
    ''')
except sqlite3.Error as e:
    print("Error creating query_urls:", e)


cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cursor.fetchall())

conn.commit()
conn.close()
