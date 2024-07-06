import mysql.connector as sql
import pandas as pd
from getpass import getpass
import hashlib

def connect(password=None):
    try:
        con = sql.connect(
            host = "cs338-db.ct2m6kmq4r44.us-east-1.rds.amazonaws.com",
            user = "root",
            password = password if password else getpass("Enter the database password: ")
        )
    except sql.ProgrammingError:
        print("Error: Connection to the database failed.")
        exit(1)
    return con

# RESET DATABASE
def reset(cur):
    with open("sql/create.sql") as f:
        sql_commands = f.read().split(';')

    for command in sql_commands:
        if command.strip():  # Skip any empty statements
            cur.execute(command.strip())

# pull data into table
def pull(cur, path="sample"):
    # Iterate through all the csv files in the data folder
    tables = ["department", "event", "vehicle", "got_stolen", "human", "police_officer", "handled", "insurance", "owner", "own"]
    files = ["{}/{}.csv".format(path, f) for f in tables]
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
    
    owner = pd.read_csv(path+'/owner.csv')['SIN'][0]
    police = pd.read_csv(path+'/police_officer.csv')['SIN'][0]
    register(cur, owner, 'owner', 'owner')
    register(cur, police, 'police', 'police')
    
def register(cur, sin, username, password):
    cur.execute("INSERT INTO ACCOUNT VALUES (%s, %s, %s)", [sin, username, encode(password)])

def encode(input):
    return hashlib.md5(input.encode()).hexdigest()

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
    # write output to a file
    for i in range(1, 7):
        with open(f"sample_out/output{i}.txt", "w") as f:
            f.write(eval(f"output{i}") + "\n")
    con.close()
