import mysql.connector as sql
import pandas as pd
from getpass import getpass

def connect():
    con = sql.connect(
        host = "cs338-db.ct2m6kmq4r44.us-east-1.rds.amazonaws.com",
        user = "root",
        # password = getpass("Enter SQL server password: ")
        password = "cs338-group8"
    )
    return con

# RESET DATABASE
def reset(cur):
    with open("sql/create.sql") as f:
        sql_commands = f.read().split(';')

    for command in sql_commands:
        if command.strip():  # Skip any empty statements
            cur.execute(command.strip())

# pull data into table
def pull(cur):
    # Iterate through all the csv files in the data folder
    tables = ["department", "event", "vehicle", "got_stolen", "human", "police_officer", "handled", "insurance", "owner", "own"]
    files = ["data/{}.csv".format(f) for f in tables]
    for table, file in zip(tables, files):
        # Read the csv file into a pandas dataframe
        df = pd.read_csv(file)
        # Convert the dataframe to a list of tuples
        data = [tuple(x) for x in df.values]
        # Get the column names
        columns = df.columns
        # Create the insert statement
        insert = "INSERT INTO {} ({}) VALUES ({})".format(
            table.upper(),
            ", ".join(columns),
            ", ".join(["%s" for _ in columns])
        )
        # Insert the data into the table
        cur.executemany(insert, data)

def features(cur, num, input):
    with open(f"sql/feature{num}.sql") as f:
        if input == None:
            sql_commands = f.read().split(';')
        else:
            sql_commands = f.read().format(input).split(';')

    for command in sql_commands:
        if command.strip():
            cur.execute(command.strip())

    output = ""
    try:
        result = cur.fetchall()
        for row in result:
            output += str(row) + "\n"
    except sql.connector.errors.InterfaceError:
        pass
    return output

if __name__ == "__main__":
    con = connect()
    cur = con.cursor()
    reset(cur)
    pull(cur)
    con.commit()
    output1 = features(cur, 1, 0)
    output2 = features(cur, 2, None)
    output3 = features(cur, 3, None)
    output4 = features(cur, 4, None)
    output5 = features(cur, 5, None)
    output6 = features(cur, 6, None)
    con.close()
