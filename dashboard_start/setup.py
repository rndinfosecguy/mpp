import os
import sqlite3
import time

from scapy.all import rdpcap, IP, DNS, DNSQR, Ether


def parse_credential_file(filename):
    results = []
    with open(filename, "r", encoding="utf-8") as f:
        block = {}
        for line in f:
            line = line.strip()
            if not line:
                if block:
                    results.append(block)
                    block = {}
                continue
            if ":" in line:
                key, value = map(str.strip, line.split(":", 1))
                if key in ["email", "password", "ip", "hostname"]:
                    block[key] = value
        if block:
            results.append(block)
    return results


def process_pcap(conn, pcap_file, app_searchstrings):
    packets = rdpcap(pcap_file)
    cursor = conn.cursor()
    target_cache = {}

    for pkt in packets:
        if not (pkt.haslayer(IP) and pkt.haslayer(DNS) and pkt.haslayer(DNSQR)):
            continue

        dns = pkt[DNS]
        if dns.qr != 0:
            continue

        query = pkt[DNSQR]
        if query.qtype != 1:
            continue

        src_ip = pkt[IP].src.strip()
        mac_addr = pkt[Ether].src
        packet_time = pkt.time
        domain = query.qname.decode(errors="ignore").rstrip(".")

        if src_ip not in target_cache:
            cursor.execute("SELECT id FROM targets WHERE ip=?", (src_ip,))
            row = cursor.fetchone()
            if row is None:
                cursor.execute(
                    "INSERT INTO targets (ip, mac, pcap, date) VALUES (?, ?, ?, ?)",
                    (src_ip, mac_addr, pcap_file, str(packet_time)),
                )
                conn.commit()
                print(f"\n[+] New target added for {src_ip}")
                cursor.execute("SELECT id FROM targets WHERE ip=?", (src_ip,))
                row = cursor.fetchone()
            target_cache[src_ip] = row[0]

        target_id = target_cache[src_ip]

        cursor.execute(
            "INSERT INTO dns_queries (ip, query) VALUES (?, ?)",
            (target_id, domain),
        )

        domain_lower = domain.lower()
        for searchstring, app_id in app_searchstrings:
            if searchstring in domain_lower:
                print(f"\t[*] Possible match found: {domain} contains '{searchstring}'")
                cursor.execute(
                    "SELECT 1 FROM targetapps WHERE target=? AND appname=?",
                    (target_id, app_id),
                )
                if cursor.fetchone() is None:
                    cursor.execute(
                        "INSERT INTO targetapps (target, appname) VALUES (?, ?)",
                        (target_id, app_id),
                    )

    conn.commit()


def process_credentials(conn, credentials_file):
    creds = parse_credential_file(credentials_file)
    cursor = conn.cursor()

    for cred in creds:
        cursor.execute("SELECT id FROM targets WHERE ip=?", (cred["ip"],))
        row = cursor.fetchone()
        if row is None:
            cursor.execute(
                "INSERT INTO targets (ip, mac, pcap, date) VALUES (?, ?, ?, ?)",
                (cred["ip"], "00:00:00:00:00:00", "n/a", str(time.time())),
            )
            conn.commit()
            cursor.execute("SELECT id FROM targets WHERE ip=?", (cred["ip"],))
            row = cursor.fetchone()

        target_id = row[0]
        cursor.execute(
            "SELECT count(id), username FROM credentials WHERE target=?", (target_id,)
        )
        row = cursor.fetchone()
        count, username = row[0], row[1]

        if count == 0:
            cursor.execute(
                "INSERT INTO credentials (username, password, target, hostname) VALUES (?, ?, ?, ?)",
                (cred["email"], cred["password"], str(target_id), cred["hostname"]),
            )
            conn.commit()
            print(f"\t[+] Added credentials -> {cred['email']}:{cred['password']}")
        elif username == "NONE":
            cursor.execute(
                "UPDATE credentials SET username=?, password=? WHERE target=?",
                (cred["email"], cred["password"], str(target_id)),
            )
            conn.commit()
            print(f"\t[+] Added credentials -> {cred['email']}:{cred['password']}")


def process_hostnames(conn, hostnames_file):
    cursor = conn.cursor()

    with open(hostnames_file, "r") as f:
        hostnames = f.readlines()

    unique_hostnames = {line.strip() for line in hostnames}

    for hostname in unique_hostnames:
        mac, name = hostname.split(",")
        cursor.execute("SELECT id FROM targets WHERE mac=?", (mac,))
        row = cursor.fetchone()
        if row is not None:
            target_id = row[0]
            cursor.execute(
                "SELECT count(id) FROM credentials WHERE target=?", (target_id,)
            )
            if cursor.fetchone()[0] == 0:
                cursor.execute(
                    "INSERT INTO credentials (username, password, target, hostname) VALUES (?, ?, ?, ?)",
                    ("NONE", "NONE", str(target_id), name),
                )
                conn.commit()
                print(f"\t[+] Added hostname -> {name}")

loot_folder = "/mmc/root/loot/mpp/"
credentials_file = "/mmc/root/logs/credentials.json"
hostnames_file = "/mmc/root/logs/hostnames.csv"

print("[*] Checking for database file...")
if not os.path.exists("data.db"):
    print("\t[-] Database file does not exist, creating it...")
    os.system("python3 create_database.py")
else:
    print("\t[+] Database file already exists. No action taken.")
print()

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

pcap_files = [f for f in os.listdir(loot_folder) if f.endswith(".pcap")]
print(f"[+] Found {len(pcap_files)} PCAP files: {', '.join(pcap_files)}")

cursor.execute("SELECT pcap FROM integrated")
existing_pcap_files = {row[0] for row in cursor.fetchall()}
new_pcap_files = set(pcap_files) - existing_pcap_files

cursor.execute("SELECT searchstring, id FROM apps")
app_searchstrings = [(row[0].strip(), row[1]) for row in cursor.fetchall()]

for pcap_file in new_pcap_files:
    process_pcap(conn, loot_folder + pcap_file, app_searchstrings)
    cursor.execute("INSERT INTO integrated (pcap) VALUES (?)", (pcap_file,))
    conn.commit()

print()
print("[*] Checking for credentials")
process_credentials(conn, credentials_file)

print()
print("[*] Checking for hostnames")
process_hostnames(conn, hostnames_file)

conn.close()
