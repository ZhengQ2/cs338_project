import click
import impl

if __name__ == '__main__':
    print("Connecting to database...")
    con = impl.connect()
    cur = con.cursor()
    reset = click.confirm("Do you want to reset the database and repull data into tables?")
    if reset:
        impl.reset(cur)
        con.commit()
        print("Database reset.")
        print("Pulling data into tables...")
        impl.pull(cur)
    else:
        print("Setting up database...")
        cur.execute("USE Auto_Theft")
    
    while True:
        features = """
        We support following features:
        1. List neighborhoods where the number of events is greater than or equal to a specified threshold.
        2. Count the types of outcome for all events.
        3. Rank all communities in terms of the average price of vehicles that got stolen.
        4. Check the latest events captured in the dataset.
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
            value = int(input("Please enter the threshold: "))
        output = impl.features(cur, int(feature), value)
        print(output)

    con.close()