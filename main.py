import requests
from bs4 import BeautifulSoup
import pymysql.cursors
import socks
import socket
import os
from dotenv import load_dotenv
load_dotenv()

# Proxy details
proxy_host = os.getenv('PROXY_HOST')
proxy_port = os.getenv('PROXY_PORT')
proxy_username = os.getenv('PROXY_USERNAME')
proxy_password = os.getenv('PROXY_PASSWORD')

# MariaDB details
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

# Database connection
connection = pymysql.connect(host=db_host,
                             user=db_user,
                             password=db_password,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def debugPrint(msg):
    if(os.getenv('DEBUG') == True):
        print(msg)

# Function to scrape domain names from a page and insert into the database
def scrape_and_insert_domains(url):
    try:
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, proxy_host, int(proxy_port), True, proxy_username, proxy_password)
        socket.socket = socks.socksocket
    except Exception as e:
        debugPrint(f"[-]: Failed to set up SOCKS proxy: {e}")
    
    debugPrint("[*]: Requesting URL")
    response = requests.get(url)
    if response.status_code == 200:
        debugPrint("[*]: Request successful")
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table')
        rows = table.find_all('tr')
        domain_number = 0
        print("\n[+] Scraping has started... Wait for script to exit.\n")
        for row in rows:
            th_element = row.find('th')
            if th_element:
                domain = th_element.text.strip()
                if(domain == 'Domæne'): # Skip the header
                    continue
                if(domain == 'Domain'): #Skip the header
                    continue
                domain_number=domain_number+1
                debugPrint(f"[+]: #{domain_number} - {domain}")
                # Insert domain into the database
                with connection.cursor() as cursor:
                    sql = "INSERT INTO scraped_domains (domain) VALUES (%s)"
                    cursor.execute(sql, (domain,))
                    connection.commit()
                    if(cursor.lastrowid > 0):
                        debugPrint("[+] Domain inserted into the database")

print(""" ____                        _         ____                                 
|  _ \  ___  _ __ ___   __ _(_)_ __   / ___|  ___ _ __ __ _ _ __   ___ _ __ 
| | | |/ _ \| '_ ` _ \ / _` | | '_ \  \___ \ / __| '__/ _` | '_ \ / _ \ '__|
| |_| | (_) | | | | | | (_| | | | | |  ___) | (__| | | (_| | |_) |  __/ |   
|____/ \___/|_| |_| |_|\__,_|_|_| |_| |____/ \___|_|  \__,_| .__/ \___|_|   
                                                           |_|              """)
print("github.com/ha1fdan - ha1fdan.xyz")

# Call the function to scrape and insert domain names
debugPrint("[*]: Starting script")
scrape_and_insert_domains(os.getenv('URL'))

# Close database connection
connection.close()
debugPrint("[*]: Database connection closed")