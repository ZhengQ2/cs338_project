import mysql.connector as sql
import pandas as pd
import numpy as np
from getpass import getpass


def connect():
    con = sql.connect(
        host="cs338-db.ct2m6kmq4r44.us-east-1.rds.amazonaws.com",
        user="root",
        # password = getpass("Enter SQL server password: ")
        password="cs338-group8"
    )
    return con

# RESET DATABASE
def reset(cur):
    cur.execute("DROP DATABASE IF EXISTS car_theft")
    cur.execute("CREATE DATABASE car_theft")
    cur.execute("USE car_theft")
    cur.execute("DROP TABLE IF EXISTS data")
    cur.execute("""CREATE TABLE data (
                OBJECTID INT,
                EVENT_UNIQUE_ID TEXT,
                REPORT_DATE DATE,
                OCC_DATE DATE,
                REPORT_HOUR SMALLINT,
                OCC_HOUR SMALLINT,
                DIVISION TEXT,
                LOCATION_TYPE TEXT,
                PREMISES_TYPE TEXT,
                UCR_CODE SMALLINT,                  /* only 2135 */
                UCR_EXT SMALLINT,                   /* only 210 */
                OFFENCE TEXT,                       /* only "Theft Of Motor Vehicle" */
                MCI_CATEGORY TEXT,                  /* only "Auto Theft" */
                HOOD_158 SMALLINT,
                NEIGHBOURHOOD_158 TEXT,
                HOOD_140 SMALLINT,
                NEIGHBOURHOOD_140 TEXT,
                LONG_WGS84 FLOAT,
                LAT_WGS84 FLOAT
                )""")

    cur.execute("DROP VIEW IF EXISTS data_full")
    cur.execute("""CREATE VIEW data_full AS SELECT
                OBJECTID,
                EVENT_UNIQUE_ID,

                REPORT_DATE,
                YEAR(REPORT_DATE) AS REPORT_YEAR,
                MONTH(REPORT_DATE) AS REPORT_MONTH,
                DAY(REPORT_DATE) AS REPORT_DAY,
                DAYOFYEAR(REPORT_DATE) AS REPORT_DOY,
                DAYOFWEEK(REPORT_DATE) AS REPORT_DOW,
                REPORT_HOUR,

                OCC_DATE,
                YEAR(OCC_DATE) AS OCC_YEAR,
                MONTH(OCC_DATE) AS OCC_MONTH,
                DAY(OCC_DATE) AS OCC_DAY,
                DAYOFYEAR(OCC_DATE) AS OCC_DOY,
                DAYOFWEEK(OCC_DATE) AS OCC_DOW,
                OCC_HOUR,

                DIVISION,
                LOCATION_TYPE,
                PREMISES_TYPE,
                UCR_CODE,
                UCR_EXT,
                OFFENCE,
                MCI_CATEGORY,
                HOOD_158,
                NEIGHBOURHOOD_158,
                HOOD_140,
                NEIGHBOURHOOD_140,
                LONG_WGS84,
                LAT_WGS84
                FROM data
                """)

# pull data into table
def pull(cur):
    df = pd.read_csv('data/Auto_Theft_Open_Data.csv').drop(columns=['X', 'Y', 'REPORT_YEAR', 'REPORT_MONTH', 'REPORT_DAY', 'REPORT_DOY', 'REPORT_DOW', 'OCC_YEAR', 'OCC_MONTH', 'OCC_DAY', 'OCC_DOY', 'OCC_DOW'])
    df.replace([np.nan, 'NSA', 0], None, inplace=True)

    df.iloc[:, 2] = df.iloc[:, 2].str.split().str[0]
    df.iloc[:, 3] = df.iloc[:, 3].str.split().str[0]

    data = list(df.itertuples(index=False, name=None))

    placeholders = ', '.join(['%s'] * len(df.columns))

    batch_size = 1000
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        cur.executemany(f"INSERT INTO data VALUES ({placeholders})", batch)


def test(cur):
    cur.execute("USE car_theft")
    cur.execute("select count(*) from data_full")
    assert cur.fetchall()[0][0] == 61216

if __name__ == "__main__":
    con = connect()
    cur = con.cursor()
    # reset(cur)
    # con.commit()
    # pull(cur)
    # con.commit()
    # test(cur)
    con.close()
    
    while True: 
        print("Hello World! Please enter your command:")
        a = input()
        if a == 1:
            pass
        elif a == 2:
            pass
        else:
            print("Program Doesn't Support")

