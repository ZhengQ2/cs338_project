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

# pull data into table


def pull(cur):
    df = pd.read_csv('Auto_Theft_Open_Data.csv').drop(columns=['X', 'Y'])
    df.replace([np.nan, 'NSA', 0], None, inplace=True)

    df.iloc[:, 2] = df.iloc[:, 2].str.split('+').str[0]
    df.iloc[:, 3] = df.iloc[:, 3].str.split('+').str[0]

    data = list(df.itertuples(index=False, name=None))

    placeholders = ', '.join(['%s'] * len(df.columns))

    batch_size = 1000
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        cur.executemany(f"INSERT INTO data VALUES ({placeholders})", batch)


def test(cur):
    cur.execute("USE car_theft")
    cur.execute("select count(*) from data")
    assert cur.fetchall()[0][0] == 61216


if __name__ == "__main__":
    con = connect()
    cur = con.cursor()
    reset(cur)
    con.commit()
    pull(cur)
    con.commit()
    test(cur)
    con.close()
