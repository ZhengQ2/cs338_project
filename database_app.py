import click, impl
from impl import encode 
import getpass

def exist(cur, username, password):
    cur.execute(f"SELECT COUNT(*) FROM ACCOUNT WHERE Username = '{username}' AND Password = '{encode(password)}'")
    return cur.fetchone()[0] == 1
    
if __name__ == '__main__':
    print("Connecting to database...")
    con = impl.connect()
    cur = con.cursor()

    reset = click.confirm("Do you want to reset the database and repull data into tables?")
    if reset:
        impl.reset(cur)
        print("Database reset.")
        print("Pulling data into tables...")
        impl.pull(cur)
        con.commit()
    else:
        print("Setting up database...")
        cur.execute("USE Auto_Theft")

    while True:
        username = input('Username: ')
        password = getpass.getpass('Password: ')
        if not exist(cur, username, password):
            print('wrong login')
        else:
            break

    while True:
        features = """
        We support following features:
        1. List neighborhoods where the number of events is greater than or equal to a specified threshold.
        2. List owner's personal information for a specific vehicle VIN.
        3. Rank all communities in terms of the average price of vehicles that got stolen.
        4. Check the latest events captured in the dataset based on input.
        5. Check insurance payments for vehicles that got stolen. 
        6. Check police resposible for handled events.
        Please select a feature to run (1-6) or type anything else to quit:
        """
        print(features)
        feature = input()
        if feature not in ['1', '2', '3', '4', '5', '6']:
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
            value = input("Please enter the number of events you want to see: ")

        output = impl.features(cur, int(feature), value)
        print(output)

    con.close()