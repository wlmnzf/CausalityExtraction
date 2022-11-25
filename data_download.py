from distutils.command.clean import clean
from py2neo import Graph,Node,Relationship
import json
import os
from py2neo.matching import *

KGraph = Graph(
    "http://nju.csuncle.com:7474", 
    auth=("neo4j","wlm94929")
)


import csv


#################CVE###############
matcher = NodeMatcher(KGraph)
result = matcher.match('CVE').all()

# 1. 创建文件对象
f = open('CVE.csv','w',encoding='utf-8')
csv_writer = csv.writer(f)
index=0

for node in result:
    CVE_ID=node["CVE_ID"]
    CVE_Description=node["CVE_Description"]
    # 2. 基于文件对象构建 csv写入对象
    csv_writer.writerow([str(index),CVE_ID,CVE_Description])
    index+=1
    
f.close()


#################ATT&CK###############
result = matcher.match('ATT&CK').all()

# 1. 创建文件对象
f = open('ATT&CK.csv','w',encoding='utf-8')
csv_writer = csv.writer(f)
index=0
x_set=set()
for node in result:
    TTP_ID=node["TTP_id_unique"]
    Examples=node["Examples"]
    if Examples=='':
        continue
    Examples_split=Examples.split("\t")
    for eg in Examples_split:
        eg_split=eg.split("#")
        # if len(eg_split)==4:
        E_ID=eg_split[0]
        E_Name=eg_split[2]
        E_Description=eg_split[3]
        csv_writer.writerow([str(index),TTP_ID,E_ID,E_Name,E_Description])
        index+=1
        # else:
        #     # print(TTP_ID)x
        #     x_set.add(TTP_ID)

print(x_set)

f.close()
