import mysql.connector as sql
import pandas as pd
from numpy import nan
from getpass import getpass

#if server not enabled
#sudo /usr/local/mysql/bin/mysqld_safe
con = sql.connect(
  host = "localhost",
  user = "root",
  password = getpass("Enter SQL server password: ")
)
cur = con.cursor()

#RESET DATABASE
def reset():
  cur.execute("DROP DATABASE IF EXISTS car_theft")
  cur.execute("CREATE DATABASE car_theft")
  cur.execute("USE car_theft")
  cur.execute("DROP TABLE IF EXISTS data")
  cur.execute("""CREATE TABLE data (
              OBJECTID INT,
              EVENT_UNIQUE_ID TEXT,
              REPORT_DATE DATETIME,
              OCC_DATE DATETIME,
              REPORT_YEAR SMALLINT,
              REPORT_MONTH TEXT,
              REPORT_DAY SMALLINT,
              REPORT_DOY SMALLINT,
              REPORT_DOW TEXT,
              REPORT_HOUR SMALLINT,
              OCC_YEAR SMALLINT,
              OCC_MONTH TEXT,
              OCC_DAY SMALLINT,
              OCC_DOY SMALLINT,
              OCC_DOW TEXT,
              OCC_HOUR SMALLINT,
              DIVISION TEXT,
              LOCATION_TYPE TEXT,
              PREMISES_TYPE TEXT,
              UCR_CODE SMALLINT,
              UCR_EXT SMALLINT,
              OFFENCE TEXT,
              MCI_CATEGORY TEXT,
              HOOD_158 SMALLINT,
              NEIGHBOURHOOD_158 TEXT,
              HOOD_140 SMALLINT,
              NEIGHBOURHOOD_140 TEXT,
              LONG_WGS84 FLOAT,
              LAT_WGS84 FLOAT
              )""")
  con.commit()

#pull data into table
def pull():
  df = pd.read_csv('Auto_Theft_Open_Data.csv').drop(columns = ['X', 'Y'])
  df = df.replace([nan, 'NSA', 0], None)

  data = df.values.tolist()

  lst = []
  for i in range(len(data[0])):
      lst.append('%s')
  lst = ', '.join(lst)

  for i in range(len(data)):
    for j in [2, 3]:
      data[i][j] = data[i][j].split('+')[0]

  cur.executemany(f"INSERT INTO data VALUES ({lst})", data)
  con.commit()

reset()
pull()
cur.execute("select count(*) from data")
print(cur.fetchall())
