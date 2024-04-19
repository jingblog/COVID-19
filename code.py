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
 
# 网站解析
name = "us"
url = 'https://www.worldometers.info/coronavirus/'
res = requests.get(url=url, headers=headers).content.decode()
html = etree.HTML(res)

# 分别表示美国总感染人数，单日新增确诊人数，现有确诊人数，总死亡人数，单日新增死亡人数
fname=["Total Cases of " + name,"Daily New Cases of " + name,"Active Cases of " + name,"Total Deaths of " + name,"Daily Deaths of " + name]
 

# 打开文件
tname = "true data.csv"
if os.path.exists(tname):
    os.remove(tname)
f=open(tname, "a", newline="")
writer = csv.writer(f)

# 尝试发送请求
try:
    data = html.xpath(f'/html/body/div/div[2]/div[1]/div[1]/div/script/text()')[0]
except:
    print("数据获取失败----xpath错误",name)
    sys.exit()

# 获取日期
compiles_date = re.compile("categories: \[(.*?)\]")
data1=compiles_date.findall(data)[0]
lex = shlex.shlex(data1)
lex.whitespace=','
lex.quotes='"'
lex.whitespace_split = True
itemlist=list(lex)

# 把 " 去掉
for i in list(range(0, len(itemlist))):
    itemlist[i]=itemlist[i].strip('"')
date=itemlist
date.insert(0,"")
# 写入日期
try:
    writer.writerow(date)
except:
    print("写入日期失败",name)
    sys.exit()

# 循环遍历每一组数据
for choice in range(0,5,1):
    # 尝试发送请求
    try:
        data = html.xpath(f'/html/body/div/div[2]/div[1]/div[{choice+1}]/div/script/text()')[0]
    except:
        print("数据获取失败----xpath错误",fname[choice])
        sys.exit()

    # 正则匹配
    compiles_count = re.compile("data: \[(.*?)\]")

    # 尝试发送请求
    try:
        counts = compiles_count.findall(data)[0]
    except:
        print("数据获取失败----data正则匹配错误",fname[choice])
        sys.exit()

    # 分割成列表
    counts_list=counts.split(",")
    counts_list.insert(0,fname[choice])
    # 写入感染人数
    try:
        writer.writerow(counts_list)
    except:
        print("写入人数失败",fname[choice])
        sys.exit()

    print("数据获取成功", fname[choice])
# 关闭文件
f.close()
