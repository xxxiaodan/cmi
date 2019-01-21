import csv
import datetime
from pymongo import MongoClient
CONN_ADDR1 = 'dds-wz90b1624e4f6af41110-pub.mongodb.rds.aliyuncs.com:3717'
CONN_ADDR2 = 'dds-wz90b1624e4f6af42967-pub.mongodb.rds.aliyuncs.com:3717'
REPLICAT_SET = 'mgset-12242833'
username = 'root'
password = 'Xxb13981101105'
try:
    client = MongoClient([CONN_ADDR1, CONN_ADDR2], replicaSet=REPLICAT_SET, )
    client.admin.authenticate(username, password)
    print "connect successful"
except EnvironmentError:
    print "connect error!"
db = client["cmi"]

now_time = datetime.datetime.now()
now_day= now_time.strftime('%Y-%m-%d')

colname = '2018-11-27'
tmp_date = datetime.datetime.strptime(colname, "%Y-%m-%d")
date_count = []

while tmp_date <= now_time:
    count = db[colname].count()
    print colname + ":" + str(count)
    date_count.append([colname,count])
    tmp_date += datetime.timedelta(days=1)
    colname = tmp_date.strftime("%Y-%m-%d")
    
with open('cmi_count.csv', 'wb') as f:
    writer = csv.writer(f)
    for row in date_count:
        writer.writerow(row)