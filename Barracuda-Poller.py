#!python3
# -*- coding: utf-8 -*-
import requests
import json
import re
import sqlite3
import os.path
from bs4 import BeautifulSoup
import time

datet = time.strftime('%Y-%m-%d %H:%M:%S')


# Creates Login Session
session_requests = requests.session()

# Creates DB Connection
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "barracuda.sqlite")
db = sqlite3.connect(db_path)
c = db.cursor()

# Var Definitions
passwd = ""
authType = "Local"
locale = "en_US"
user = "Admin"
params = ""
host = ""
port = "8000"
url = "http://" + host + ":" + port + "/cgi-mod/index.cgi"
RED, BLUE, GREEN, YELLOW, RESET = '\033[31m', '\x1b[1;34;49m', '\033[92m', '\x1b[1;33;49m', '\x1b[0m'
rrdtoolPath = "/usr/bin/rrdtool"
rrdPath = "~/"
rrdFile = host + ".rrd"

f = {}
f.update(
    dict.fromkeys(
        ["xa0", "\\n", "\\t", "\\", "     ", "    ", "[", "]", "\n", "%", "RPM", "°C"], "")
)

# Gets Login Page to pull Encryption key and Epoch from the page.
data = session_requests.get(url)

# Extracts key and Epoch from the page.
soup = BeautifulSoup(data.text, "html.parser")
enckey = soup.findAll('input', {"id": "enc_key"})[0]['value']
et = soup.findAll('input', {"id": "et"})[0]['value']

# Creates Parameters to pass to the login Post Request
parm = {
    'enc_key': enckey,
    'et': et,
    'user=': user,
    'password': passwd,
    'enctype': 'bc',
    'password_entry': '',
    'login_page': '1',
    'login_state': 'out',
    'real_user': 'Admin',
    'locale': locale,
    'form': 'f'
}

loginHeaders = {
    "Host": ""
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept - Language": "en-US,en;q=0.5",
    "Accept - Encoding": "gzip, deflate",
    "Content-type": "application/x-www-form-urlencoded",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "http:///cgi-mod/index.cgi?locale=en_US",
    "Content - Length": "180",
    "Connection": "keep-alive"
}
# Pulls Session Data from url allowing us to login to the service.
data = session_requests.post(url, data=parm, headers=loginHeaders)
jsonPayload = json.loads(data.text)
keyurl = jsonPayload['redirect']

# Remove's the Directory/File from the response.
keyurl = re.sub('/cgi-mod/index.cgi\?', '', keyurl)

dataHeaders = {
    "Host": "",
    "User-Agent": "Mozilla/5.0 (Windows NT10.0;WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip,deflate",
    "Referer": "http:///cgi-mod/index.cgi?locale=en_US",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

data = session_requests.get(url, params=keyurl)

# Exits app if HTTP Response is not 200
if data.status_code != 200:
    print(data.status_code, "\n Exiting...")
    exit()

print("Connection to:", BLUE, host + ":" + port, RESET, "-", GREEN, "Successful", RESET, "\n")

#####################
# Get's footer Data #
#####################

print("Host Name:", BLUE, host, RESET)
soup = BeautifulSoup(data.text, "html.parser")
footer = soup.findAll('div', {"id": "cui-footer"})
soup = BeautifulSoup(str(footer), "html.parser")
footer = soup.get_text()
footer = footer.split("\n")
footer[4] = footer[4].replace(" More...", "")
print(footer[4], '\n', footer[3], "\n")

######################
# Get's Health Stats #
######################

# Gathers Health Data from response - Performance Statistics Section
soup = BeautifulSoup(data.text, "html.parser")
deviceHealth = soup.findAll('div', {"id": "health_module"})

# Need to extract 2nd time to get field/Data Combo from html
deviceHealth = str(deviceHealth)
soup = BeautifulSoup(deviceHealth, "html.parser")
deviceHealth = soup.findAll('dl', {"class": "cui-dl"})

# Need to Extract 3rd Time to get Field Titles from html
deviceHealth = str(deviceHealth)
soup = BeautifulSoup(deviceHealth, "html.parser")
healthTitles = soup.findAll('dt', {"class": "cui-dt"})
healthValues = soup.findAll('dd', {"class": "cui-dd"})

# Initilized Lists for Data
healthT, healthV = [], []

# Loops through Titles and loads them into list
for x in healthTitles:
    soup = BeautifulSoup(str(x), "html.parser")
    rtn = str(soup.get_text())
    for key in f:
        rtn = str(rtn).replace(key, "")
    healthT.insert(0, rtn)

# Loops through Data and loads them into list
for x in healthValues:
    soup = BeautifulSoup(str(x), "html.parser")
    rtn = str(soup.get_text())
    for key in f:
        rtn = str(rtn).replace(key, "")
    healthV.insert(0, rtn)

print("Health Statistics")
for x in reversed(range(0, len(healthT))):
    if healthT[x] == 'In/Out Queue Size:':
        temp = str(healthV[x]).split("/")
        print(healthT[x], RESET, end='')
        t = 0
        for z in temp:
            z = int(z)
            if z <= 10 or z == 0:
                print(GREEN, z, RESET, end='')
            else:
                if z > 25:
                    print(YELLOW, z, RESET, end='')
                else:
                    if z >= 50:
                        print(RED, z, RESET, end='')
                    else:
                        # failsafe reverts output to white on black
                        print(RESET, z, end='')
            if t == 0:
                print("/", end='')
            t += 1
        print()
        continue
    print(healthT[x], healthV[x])

sql = "INSERT INTO main.Health VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);"

c.execute(
    sql,
    (
        datet, str.split(healthV[11], "/")[0], str.split(healthV[11], "/")[1], str.split(healthV[10], " ")[0],
        str.split(healthV[9], " ")[0],
        healthV[8], healthV[7], healthV[6], healthV[5],
        healthV[4], healthV[3], healthV[2], healthV[1]
    )
)

db.commit()

# Gathers Inbound Email Statistics Data from response - Performance Statistics Section
soup = BeautifulSoup(data.text, "html.parser")
inboundStats = soup.findAll('div', {"id": "inbound_stats"})

# Needed to extract 2nd time to get field/Data Combo from html
inboundStats = str(inboundStats)
soup = BeautifulSoup(inboundStats, "html.parser")
inboundStats = soup.findAll('tr', {"class": "config_module_tr"})
soup = BeautifulSoup(str(inboundStats), "html.parser")
inboundStats = soup.find_all("td")

# Needed to Extract 3rd Time to get Field Titles from html
inboundStats = str(inboundStats)
soup = BeautifulSoup(inboundStats, "html.parser")
inStatTitles = soup.findAll(
    'td', {
        "class": "label",
        "style": "font-weight:bold; overflow:hidden; padding:0 3px; padding-right:3px; white-space:nowrap"
    }
)
soup = BeautifulSoup(str(inStatTitles), "html.parser")

# Needed to extract Values from html
soup = BeautifulSoup(inboundStats, "html.parser")
inStatValues = soup.findAll('td', {"align": "right"})
soup = BeautifulSoup(str(inStatValues), "html.parser")

inStatTitles.append("Total Received")

# Initilized Lists for Data
inboundT, inboundV, inboundTemp = [], [], []

for x in inStatTitles:
    soup = BeautifulSoup(str(x), "html.parser")
    rtn = str(soup.get_text())
    rtn = rtn.replace("\n", "")
    inboundT.insert(len(inStatTitles), rtn)

for x in inStatValues:
    soup = BeautifulSoup(str(x), "html.parser")
    rtn = str(soup.get_text())
    rtn = rtn.replace("\n", "")
    rtn = rtn.replace(",", "")
    inboundTemp.insert(0, rtn)

# Loads Values into array
y, t = [0, 1]

for x in reversed(inboundTemp):
    if t == 2 or t == 6 or t == 10 or t == 14 or t == 18 or t == 22 or t == 26:
        inboundV.insert(y, x)
    y += 1
    t += 1

print("\nInbound Statistics")
for x in range(0, len(inboundT)):
    y = x * 1
    print(inboundT[x], ":", inboundV[y])

sql = "INSERT INTO main.InStats VALUES (?,?,?,?,?,?,?,?);"

c.execute(
    sql,
    (
        inboundV[0], inboundV[1], inboundV[2], inboundV[3], inboundV[4], inboundV[5], inboundV[6], datet
    )
)

db.commit()


#######################
# Outbound Statistics #
#######################

# Gathers Outbound Email Statistics Data from response - Performance Statistics Section
soup = BeautifulSoup(data.text, "html.parser")
outboundStats = soup.findAll('div', {"id": "outbound_stats"})

# Needed to extract 2nd time to get field/Data Combo from html
outboundStats = str(outboundStats)
soup = BeautifulSoup(outboundStats, "html.parser")
outboundStats = soup.findAll('tr', {"class": "config_module_tr"})
soup = BeautifulSoup(str(outboundStats), "html.parser")
outboundStats = soup.find_all("td")

# Needed to Extract 3rd Time to get Field Titles from html
outboundStats = str(outboundStats)
soup = BeautifulSoup(outboundStats, "html.parser")
outStatTitles = soup.findAll(
    'td',
    {
        "class": "label",
        "style": "font-weight:bold; overflow:hidden; padding:0 3px; padding-right:3px; white-space:nowrap"
    }
)
soup = BeautifulSoup(str(outStatTitles), "html.parser")

# Needed to extract Values from html
soup = BeautifulSoup(outboundStats, "html.parser")
outStatValues = soup.findAll('td', {"align": "right"})
soup = BeautifulSoup(str(outStatValues), "html.parser")

outStatTitles.append("Total Sent")

# Initilized Lists for Data
outboundT, outboundV, outboundTemp = [], [], []

for x in outStatTitles:
    soup = BeautifulSoup(str(x), "html.parser")
    rtn = str(soup.get_text())
    rtn = rtn.replace("\n", "")
    outboundT.insert(len(outStatTitles), rtn)

for x in outStatValues:
    soup = BeautifulSoup(str(x), "html.parser")
    rtn = str(soup.get_text())
    rtn = rtn.replace("\n", "")
    rtn = rtn.replace(",", "")
    outboundTemp.insert(0, rtn)

# Loads Values into array
y, t = [0, 1]

for x in reversed(outboundTemp):
    if t == 2 or t == 6 or t == 10 or t == 14 or t == 18 or t == 22 or t == 26 or t == 30 or t == 34:
        outboundV.insert(y, x)
    y += 1
    t += 1

print("\nOutbound Statistics")
for x in range(0, len(outboundT)):
    y = x * 1
    print(outboundT[y], ":", outboundV[y])

sql = "INSERT INTO main.outStats VALUES (?,?,?,?,?,?,?,?,?,?);"

c.execute(
    sql,
    (
        outboundV[0], outboundV[1], outboundV[2], outboundV[3], outboundV[4], outboundV[5], outboundV[6], outboundV[7],
        outboundV[8], datet
    )
)

db.commit()
#######################
# Subscription Status #
#######################

soup = BeautifulSoup(data.text, "html.parser")
subStats = soup.findAll('div', {"id": "subscription_module"})
parm = keyurl.split("&", 5)
parm.append("half_width=")
parm.append("screen_name=status")
t = 0
for x in parm:
    params = params + str(parm[t]) + "&"
    t += 1

url = "http://" + host + ":" + port + "/cgi-mod/build_status_expiration_display_content.cgi?" + params
data = session_requests.get(url, headers=loginHeaders)

soup = BeautifulSoup(data.text, "html.parser")
subStats = soup.find_all("dt")
soup = BeautifulSoup(str(subStats), "html.parser")
subTitle = soup.get_text()

for key in f:
    subTitle = str(subTitle).replace(key, "")
subTitle = subTitle.split(",", 2)

soup = BeautifulSoup(data.text, "html.parser")
subStats = soup.find_all("dd")
soup = BeautifulSoup(str(subStats), "html.parser")
subValue = soup.get_text()

for key in f:
    subValue = str(subValue).replace(key, "")
subValue = subValue.split(",", 2)

print("\nSubscription Status")

for x in range(0, 2):
    print(subTitle[x], subValue[x])

db.close()
