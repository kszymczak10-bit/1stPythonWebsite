import sqlite3

DB_PATH = "app.db"

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        password_hash TEXT NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS wheels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand TEXT NOT NULL,
        diameter INTEGER NOT NULL,
        width REAL NOT NULL,
        pcd TEXT NOT NULL
    );
    """)
    
    cur.execute("DELETE FROM wheels")
    cur.execute("INSERT INTO wheels (brand, diameter, width, pcd) VALUES (?, ?, ?, ?)", ("BBS", 18, 8.0, "5x112"))
    cur.execute("INSERT INTO wheels (brand, diameter, width, pcd) VALUES (?, ?, ?, ?)", ("OZ", 19, 8.5, "5x112"))
    cur.execute("INSERT INTO wheels (brand, diameter, width, pcd) VALUES (?, ?, ?, ?)", ("Ronal", 18, 8.0, "5x112"))
    cur.execute("INSERT INTO wheels (brand, diameter, width, pcd) VALUES (?, ?, ?, ?)", ("Japan Racing", 18, 9.0, "5x100"))

    conn.commit()
    conn.close()
    print("OK")

if __name__ == "__main__":
    main()
