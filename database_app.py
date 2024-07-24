import click, impl, time, getpass, os

def login(cur, username, password):
    with open("sql/account_verification.sql") as f:
        cur.execute(f.read(),[username, impl.encode(password)])
    return cur.fetchone()[0] == 1

def register(con, cur, sin, username, password):
    cur.execute("SELECT COUNT(*) FROM ACCOUNT WHERE SIN = %s", [sin])
    if cur.fetchone()[0] == 1:
        print("You already have an account")
        return
    cur.execute("SELECT COUNT(*) FROM HUMAN WHERE SIN = %s", [sin])
    if cur.fetchone()[0] == 0:
        print("Invalid SIN")
        return
    cur.execute("SELECT COUNT(*) FROM ACCOUNT WHERE username = %s", [username])
    if cur.fetchone()[0] == 1:
        print("Username already exist")
        return
    
    impl.register(con, cur, sin, username, password)
    print("Success")
    
if __name__ == '__main__':
    os.system('clear')
    print("Connecting to database...")
    con = impl.connect()
    cur = con.cursor()

    reset = click.confirm("Do you want to reset the database and repull data into tables?")
    if reset:
        impl.reset(cur)
        print("Database reset.")
        print("Pulling data into tables...")
        impl.pull(con, cur)
        con.commit()
    else:
        cur.execute("USE Auto_Theft")
    
    while True:
        os.system('clear')
        if click.confirm("Register?"):
            sin = input("SIN: ")
            username = input("Username: ")
            password = input("Password: ")
            register(con, cur, sin, username, password)
            input("Press any key to continue...")
        else:
            break

    while True:
        os.system('clear')
        username = input('Username: ')
        password = getpass.getpass('Password: ')
        if not login(cur, username, password):
            input('wrong login\nPrint any key to continue...')
        else:
            break
    try:
        while True:
            os.system('clear')
            features = """We support following features:
1. List neighborhoods where the number of events is greater than or equal to a specified threshold.
2. List owner's personal information for a specific vehicle VIN.
3. List automobile minimum and maximum price and total vehicle of all communities, ranked by average price of vehicles that got stolen.
4. Check the latest events captured in the dataset based on input.
5. Generate a report ranking police officers within their departments based on the number of events they have handled.
6. Provide information on the police officers' SIN and the events they have handled.
Please select a feature to run (1-6) or type anything else to quit:"""
            print(features)
            feature = input()
            if feature not in ['1', '2', '3', '4', '5', '6']:
                print("Exiting...")
                break
            value = None

            if feature == '1':
                try:
                    value = int(input("Please enter the threshold: "))
                except ValueError:
                    print("Invalid input. Please enter an integer.")
                    continue
            elif feature == '2':
                value = input("Please enter the VIN: ")
            elif feature == '4':
                try:
                    value = int(input("Please enter the number of events you want to see: "))
                except ValueError:
                    print("Invalid input. Please enter an integer.")
                    continue

            start = time.time()
            output = impl.features(cur, int(feature), value)
            print(output)
            print('run time:', time.time()-start)
            input("Press enter to continue...")
    except KeyboardInterrupt:
        print("Exiting...")

    con.close()