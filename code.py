import requests
from lxml import etree
import re
import csv
import shlex
import sys
import os
 
headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.55"
}
 
# 1. Website Parsing
# Using a web scraper to fetch all COVID-19 infection data for the United Kingdom.
name = "us"
url = 'https://www.worldometers.info/coronavirus/' + name + "/"
res = requests.get(url=url, headers=headers).content.decode()
html = etree.HTML(res)

# Representing the total number of infections in the United States, daily new confirmed cases, current confirmed cases, total deaths, and daily new deaths.
fname=["Total Cases of " + name,"Daily New Cases of " + name,"Active Cases of " + name,"Total Deaths of " + name,"Daily Deaths of " + name]
 

# open file
tname = "true data.csv"
if os.path.exists(tname):
    os.remove(tname)
f=open(tname, "a", newline="")
writer = csv.writer(f)

# 2. try to Send Request
try:
    data = html.xpath(f'/html/body/div/div[2]/div[1]/div[1]/div/script/text()')[0]
except:
    print("Data retrieval failed—XPath error",name)
    sys.exit()

# Get Date
compiles_date = re.compile("categories: \[(.*?)\]")
data1=compiles_date.findall(data)[0]
lex = shlex.shlex(data1)
lex.whitespace=','
lex.quotes='"'
lex.whitespace_split = True
itemlist=list(lex)

# Remove the " symbol
for i in list(range(0, len(itemlist))):
    itemlist[i]=itemlist[i].strip('"')
date=itemlist
date.insert(0,"")
# Writing Date
try:
    #print(date)
    writer.writerow(date)
except:
    print("Writing Date Failed",name)
    sys.exit()

# 3. Iterating through each set of data
for choice in range(0,5,1):
    # Attempting to Send Request
    try:
        data = html.xpath(f'/html/body/div/div[2]/div[1]/div[{choice+1}]/div/script/text()')[0]
    except:
        print("Data retrieval failed—XPath error",fname[choice])
        sys.exit()

    # Regex Matching
    compiles_count = re.compile("data: \[(.*?)\]")

    # Attempting to Send Request
    try:
        counts = compiles_count.findall(data)[0]
    except:
        print("Data retrieval failed—Data regex matching error",fname[choice])
        sys.exit()

    # Splitting into Lists
    counts_list=counts.split(",")
    counts_list.insert(0,fname[choice])
    # Writing Infected Cases
    try:
        writer.writerow(counts_list)
    except:
        print("Writing Case Numbers Failed",fname[choice])
        sys.exit()

    print("Data Retrieval Successful", fname[choice])
# Close File
f.close()
