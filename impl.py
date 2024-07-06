import mysql.connector as sql
import pandas as pd
from decimal import Decimal
import hashlib

def connect():
    try:
        con = sql.connect(
            host = "cs338-db.ct2m6kmq4r44.us-east-1.rds.amazonaws.com",
            user = "root",
            password = "cs338-group8"
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

def format_decimal(value):
    if isinstance(value, Decimal):
        return float(value)
    return value

def features(cur, num, input):
    with open(f"sql/feature{num}.sql") as f:
        if input == None:
            sql_commands = f.read().split(';')
        else:
            sql_commands = f.read().format(input).split(';')

    for command in sql_commands:
        if command.strip():
            cur.execute(command.strip())

    try:
        column_names = [i[0] for i in cur.description]
        table_content = [[format_decimal(item) for item in row] for row in cur.fetchall()]
        output = pd.DataFrame(table_content, columns=column_names).to_string(index = False)
        if "Empty DataFrame" in output:
            output = "No results found."

    except sql.connector.errors.InterfaceError:
        pass
    return output

if __name__ == "__main__":
    con = connect()
    cur = con.cursor()
    reset(cur)
    pull(cur)
    con.commit()
    output1 = "Input: 0\n"
    output1 += features(cur, 1, 0)
    output1 += "\n\nInput: 20\n"
    output1 += features(cur, 1, 20)
    output2 = "Input: \"a\"\n"
    output2 += features(cur, 2, "a")
    output2 += "\n\nInput: \"BJKPMZL3XBA85D3XB\"\n"
    output2 += features(cur, 2, "BJKPMZL3XBA85D3XB")
    output3 = features(cur, 3, None)
    output4 = "Input: 10\n"
    output4 += features(cur, 4, 10)
    output4 += "\n\nInput: 0\n"
    output4 += features(cur, 4, 0)
    output5 = features(cur, 5, None)
    output6 = features(cur, 6, None)
    # write output to a file
    for i in range(1, 7):
        with open(f"sample_out/output{i}.txt", "w") as f:
            f.write(eval(f"output{i}") + "\n")
    con.close()
