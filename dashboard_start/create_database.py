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
    ("Spotify", "spotify"),
    ("Huawei", "huawei"),
    ("Tencent", "tencent"),
    ("Samsung", "samsung"),
    ("Android", "connectivitycheck.gstatic"),
    ("Android", "android.clients.google"),
    ("Android", "play.googleapis"),
    ("Android", "time.android"),
    ("Android", "connectivitycheck.cbg-app.huawei"),
    ("Android", "connectivitycheck.platform.hicloud"),
    ("Android", "connectivitycheck.platform.hihonorcloud"),
    ("Android", "connectivitycheck.unisoc"),
    ("Amazon", "amazon"),
    ("Rewe", "rewe"),
    ("Google", "google"),
    ("Google", "gstatic"),
    ("YouTube", "youtube"),
    ("Xiaomi", "xiaomi"),
    ("Baidu", "baidu"),
    ("iOS", "captive.apple"),
    ("iOS", "courier.push.apple"),
    ("iOS", "gs-loc.apple"),
    ("iOS", "mesu.apple"),
    ("iOS", "guzzoni.apple"),
    ("iOS", "init.push.apple"),
    ("iOS", "xp.apple"),
    ("iOS", "setup.icloud"),
    ("iOS", "apple-relay.cloudflare"),
    ("iOS", "fmipalservice"),
    ("iOS", "ontology.health.apple"),
    ("iOS", "configuration.apple"),
    ("Snapchat", "snapchat"),
    ("Soundcloud", "soundcloud"),
    ("Amazon", "amazon"),
    ("Duolingo", "duolingo"),
    ("Firefox", "firefox"),
    ("Signal", "signal"),
    ("ChatGPT", "chatgpt"),
    ("Samsung", "www.goooooooooooooooooooooooooooooooooooooooooooooooooooooooooogle.com"),
    ("Claude", "claude.ai"),
    ("Claude", "anthropic"),
    # Messaging & Social
    ("Pinterest", "pinimg"),
    ("Viber", "viber"),
    ("Zalo", "zalo"),
    ("Badoo", "badoo"),
    ("Slack", "slack"),
    ("Microsoft Teams", "teams.microsoft"),
    # AI Assistants
    ("Character.AI", "character.ai"),
    # Entertainment & Media
    ("Deezer", "deezer"),
    ("Tidal", "tidal"),
    ("CapCut", "capcut"),
    ("Zing MP3", "zingmp3"),
    # Shopping
    ("Temu", "temu"),
    ("Otto", "otto"),
    # Finance
    ("Revolut", "revolut"),
    # Transport
    ("BVG", "bvg"),
    ("Citymapper", "citymapper"),
    ("Voi", "voiapp"),
    ("Bolt", "boltsvc"),
    # Utilities
    ("DeepL", "deepl"),
    ("Bookbeat", "bookbeat"),
    ("Life360", "life360"),
    ("AccuWeather", "accuweather"),
    ("Weather.com", "weather.com"),
    # Security & VPN
    ("Norton", "norton"),
    ("Bitdefender", "bitdefender"),
    ("Avast", "avast"),
    ("Private Internet Access", "privateinternetaccess"),
]

cursor.executemany(
    "INSERT INTO apps (app, searchstring) VALUES (?, ?)",
    apps
)

# Commit changes
conn.commit()

# Close the connection
conn.close()
