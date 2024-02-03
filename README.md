# Expired Domains Scraper for simply.com

This Python project scrapes a list of expired domains from a Danish hosting company named Simply.com using web scraping techniques. The domains listed on the webpage are those that have recently expired and are now available for registration. The script utilizes BeautifulSoup for parsing the HTML content and extracting domain names efficiently.

---

## Features
- [x] Supports the use of proxies, including SOCKS proxies, for enhanced privacy and security during web scraping activities.
- [x] Inserts the extracted domain names into a MariaDB database for further analysis or processing.
- [ ] Threading support is not currently implemented.

## Get started
.env
```conf
DEBUG=False
URL="https://www.simply.com/en/ninja/"

# Proxy details
PROXY_HOST='109.201.152.178' #Default for PIA Proxy
PROXY_PORT='1080'            #Default for PIA Proxy
PROXY_USERNAME=''            #Your proxy username
PROXY_PASSWORD=''            #Your proxy password

# MariaDB details
DB_HOST='localhost'         #Database host
DB_USER='root'              #Database username
DB_PASSWORD=''              #Database password
DB_NAME=''                  #Database name
```

---

Database table schema:
```sql
CREATE TABLE scraped_domains (
    id INT AUTO_INCREMENT PRIMARY KEY,
    domain VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

How to export database to csv? See [here](EXPORT.md)