import mysql.connector
import pandas as pd
from getpass import getpass

mydb = mysql.connector.connect(
  host="localhost",
  user=input("Enter SQL server username: "),
  password=getpass("Enter SQL server password: ")
)

print(mydb)

data = pd.read_csv('Auto_Theft_Open_Data.csv')
print(data.head(5))
#sql = 'select * from data limit 5'
df = data.values.tolist()
print(df[0])
cur = mydb.cursor()
lst = []
for i in range(31):
    lst.append('%s')
lst = ', '.join(lst)
print(lst)

cur.execute("DROP DATABASE IF EXISTS car_theft")
cur.execute("CREATE DATABASE car_theft")
cur.execute("USE car_theft")
cur.execute("DROP TABLE IF EXISTS data")
cur.execute("CREATE TABLE data (ID INT)")
for row in df:
    cur.execute("INSERT INTO data VALUES (%s)", [row[2]])
    
mydb.commit()
cur.execute("select count(*) from data")
print(cur.fetchall())