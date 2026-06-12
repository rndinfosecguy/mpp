import os
from scapy.all import rdpcap, IP, DNS, DNSQR, Ether
import sqlite3
import time

def parse_credential_file(filename):
    results = []

    with open(filename, "r", encoding="utf-8") as f:
        block = {}

        for line in f:
            line = line.strip()

            # Blank line = end of one record
            if not line:
                if block:
                    results.append(block)
                    block = {}
                continue

            # Match key: value lines
            if ":" in line:
                key, value = map(str.strip, line.split(":", 1))
                if key in ["email", "password", "ip", "hostname"]:
                    block[key] = value

        # Add last block if file doesn't end with newline
        if block:
            results.append(block)

    return results

def print_a_record_requests(pcap_file):
    packets = rdpcap(pcap_file)

    for pkt in packets:
        # Check for IP + DNS query
        if pkt.haslayer(IP) and pkt.haslayer(DNS) and pkt.haslayer(DNSQR):
            dns = pkt[DNS]
            
            src_ip = pkt[IP].src
            mac_addr = pkt[Ether].src
            packet_time = pkt.time

            # qr == 0 means DNS request (not response)
            if dns.qr == 0:
                query = pkt[DNSQR]

                # qtype 1 = A record
                if query.qtype == 1:
                    src_ip = pkt[IP].src
                    domain = query.qname.decode(errors="ignore").rstrip(".")

                    ip = src_ip.strip()
                    # Connect to the SQLite database
                    TmpConn = sqlite3.connect('data.db')
                    TmpCursor = TmpConn.cursor()
                    
                    # insert new target
                    query = """SELECT ip FROM targets WHERE ip=?"""
                    parameters = (ip,)
                    result = TmpCursor.execute(query, parameters).fetchone()
                    if result is None:
                        # Create a new target entry
                        query = """
                            INSERT INTO targets (ip, mac, pcap, date)
                            VALUES (?, ?, ?, ?)
                        """
                        parameters = (ip, mac_addr, pcap_file, str(packet_time))
                        TmpCursor.execute(query, parameters)
                        TmpConn.commit()
                        print()
                        print(f"[+] New target added for {ip}")
                    
                    # insert dns queries in database
                    query_target_id = """SELECT id FROM targets WHERE ip=?"""
                    parameters_ip = (ip,)
                    result_id = TmpCursor.execute(query_target_id, parameters_ip).fetchone()
                    insert_query = "INSERT INTO dns_queries (ip, query) VALUES (?, ?)"
                    parameters_query = (result_id[0], domain)
                    TmpCursor.execute(insert_query, parameters_query)
                    TmpConn.commit()              
                    
                    # look for domain/app
                    query_app = """SELECT searchstring FROM apps """
                    TmpCursor.execute(query_app)
                    result_app = [row[0] for row in TmpCursor.fetchall()]
                    
                    for string in result_app:
                        if string.strip() in domain.lower():
                            print(f"\t[*] Possible match found: {domain} contains '{string.strip()}'")
                            query_target_id = """SELECT id FROM targets WHERE ip=?"""
                            parameters_ip = (ip,)
                            result_id = TmpCursor.execute(query_target_id, parameters_ip).fetchone()
                            if result_id is not None:
                                target_id = result_id[0]
                                
                                query_app_id = """SELECT id FROM apps WHERE searchstring=?""" 
                                parameters_app_id = (string.strip(),)
                                result_app_id = TmpCursor.execute(query_app_id, parameters_app_id).fetchone()
                                result_app_id = result_app_id[0]
                                
                                exists = """SELECT * FROM targetapps WHERE target=? AND appname=?"""
                                exists_parameters = (target_id, result_app_id)
                                # Check if the result of this line is empty
                                exists_result = TmpCursor.execute(exists, exists_parameters).fetchone()
                                if exists_result is not None:
                                    continue
                                
                                # Perform insert statement into targetapps table
                                query_insert_targetapp = """INSERT INTO targetapps (target, appname) VALUES (?, ?)"""
                                parameters_insert_targetapp = (target_id, result_app_id)
                                TmpCursor.execute(query_insert_targetapp, parameters_insert_targetapp)
                                TmpConn.commit()
                    
                    TmpConn.close()
                    
                    # get search strings

loot_folder = "/mmc/root/loot/mpp/"
credentials_file = "/mmc/root/logs/credentials.json"
hostnames_file = "/mmc/root/logs/hostnames.csv"
   
print("[*] Checking for database file...")
if not os.path.exists('data.db'):
    print("\t[-] Database file does not exist, creating it...")
    os.system("python3 create_database.py")
else:
    print("\t[+] Database file already exists. No action taken.")

print()

# Connect to the SQLite database
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

pcap_files = [file for file in os.listdir(loot_folder) if file.endswith('.pcap')]

print(f"[+] Found {len(pcap_files)} PCAP files: {', '.join(pcap_files)}")

# Query the 'integrated' table for existing pcap file names
query = "SELECT pcap FROM integrated"
cursor.execute(query)

# Get the list of existing pcap files from the database
existing_pcap_files = [row[0] for row in cursor.fetchall()]

# Identify new PCAP files that are not in the database
new_pcap_files = set(pcap_files) - set(existing_pcap_files)

conn.close()

for pcapFile in new_pcap_files:
    print_a_record_requests(loot_folder + pcapFile) 
    
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    query = "INSERT INTO integrated (pcap) VALUES (?)"
    cursor.execute(query, (pcapFile,))
    conn.commit()
    conn.close()

# check for credentials
print()
print("[*] Checking for credentials")
creds = parse_credential_file(credentials_file) 
conn = sqlite3.connect('data.db')
c = conn.cursor()
for cred in creds:
    c.execute("SELECT id FROM targets where ip=\"" + cred["ip"] + "\"")
    ip_id = c.fetchone()
    if ip_id is None:
        query = "INSERT INTO targets (ip, mac, pcap, date) VALUES (?, ?, ?, ?)"
        c.execute(query, (cred["ip"], "00:00:00:00:00:00", "n/a", str(time.time())))
        conn.commit()
        
        c.execute("SELECT id FROM targets where ip=\"" + cred["ip"] + "\"")
        ip_id = c.fetchone()
    
    c.execute("SELECT count(id), username FROM credentials WHERE target=" + str(ip_id[0]))
    row = c.fetchone()
    count = row[0]
    username = row[1]
    if count == 0:
        query = "INSERT INTO credentials (username, password, target, hostname) VALUES (?, ?, ?, ?)"
        c.execute(query, (cred['email'], cred['password'], str(ip_id[0]), cred['hostname']))
        conn.commit()
        print("\t[+] Added credentials -> " + cred["email"] + ":" + cred["password"])
    if username == "NONE":
        query = "UPDATE credentials SET username=?, password=? WHERE target=?"
        c.execute(query, (cred['email'], cred['password'], str(ip_id[0])))
        conn.commit()
        print("\t[+] Added credentials -> " + cred["email"] + ":" + cred["password"])

# check for hostnames
print()
print("[*] Checking for hostnames")
f = open(hostnames_file, "r")
hostnames = f.readlines()
f.close()

unique_hostnames = set()
for hostname in hostnames:
    hostname = hostname.strip()
    unique_hostnames.add(hostname)

for hostname in unique_hostnames:
    mac, name = hostname.split(",")
    c.execute("SELECT id FROM targets where mac=\"" + mac + "\"")
    mac_id = c.fetchone()
    
    if mac_id is not None:
        c.execute("SELECT count(id) FROM credentials WHERE target=" + str(mac_id[0]))
        row = c.fetchone()
        row = row[0]
        if row == 0:
            query = "INSERT INTO credentials (username, password, target, hostname) VALUES (?, ?, ?, ?)"
            c.execute(query, ("NONE", "NONE", str(mac_id[0]), name))
            conn.commit()
            print("\t[+] Added hostname -> " + name)

c.close()
