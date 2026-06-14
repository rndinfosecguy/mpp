import sqlite3

db_file = "data.db"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS targets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip TEXT NOT NULL,
    mac TEXT NOT NULL,
    pcap TEXT NOT NULL,
    date TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS dns_queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip INTEGER NOT NULL,
    query TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS credentials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    target INTEGER,
    hostname TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS targetapps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    appname INTEGER NOT NULL,
    target INTEGER NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS apps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    app TEXT NOT NULL,
    searchstring TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS integrated (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pcap TEXT NOT NULL
)
""")

# Insert data into the table
apps = [
    ("Instagram", "instagram"),
    ("Facebook", "facebook"),
    ("Facebook", "meta"),
    ("WhatsApp", "whatsapp"),
    ("TikTok", "tiktok"),
    ("WeChat", "weixin"),
    ("WeChat", "wechat"),
    ("Twitter", "twitter"),
    ("Telegram", "telegram"),
    ("iCloud", "apple"),
    ("Spotify", "spotify"),
    ("Huawei", "huawei"),
    ("Tencent", "tencent"),
    ("Samsung", "samsung"),
    ("Android", "android"),
    ("Amazon", "amazon"),
    ("Rewe", "rewe"),
    ("Google", "google"),
    ("Google", "gstatic"),
    ("YouTube", "youtube"),
    ("Xiaomi", "xiaomi"),
    ("Baidu", "baidu"),
    ("iPhone", "captive.apple"),
    ("Snapchat", "snapchat"),
    ("Soundcloud", "soundcloud"),
    ("Amazon", "amazon"),
    ("Duolingo", "duolingo"),
    ("Firefox", "firefox"),
    ("Signal", "signal"),
    ("ChatGPT", "chatgpt"),
    ("Samsung", "www.goooooooooooooooooooooooooooooooooooooooooooooooooooooooooogle.com")
]

cursor.executemany(
    "INSERT INTO apps (app, searchstring) VALUES (?, ?)",
    apps
)

# Commit changes
conn.commit()

# Close the connection
conn.close()
