import config, csv
from faker import Faker
from faker_vehicle import VehicleProvider
from numpy import random
import pandas as pd
import time

fake = Faker('en_CA')
fake.add_provider(VehicleProvider)
Faker.seed(config.seed)
random.seed(config.seed)

def writecsv(filename, header, data):
    with open(config.path + filename + '.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)
        csvwriter.writerows(data)

def rhuman(num):
    "int num: number of people, >0"
    start = time.time()
    columns = ['SIN','Birth_date','FName','LName','Phone','Email']
    human = []

    for i in range(num):
        sin = fake.unique.ssn()
        bdate = fake.date(end_datetime = config.owner_bdate_end)
        fname = fake.first_name()
        lname = fake.last_name()
        phone = fake.phone_number()
        email = fake.email()
        human.append([sin, bdate, fname, lname, phone, email])

    writecsv('human', columns, human)
    print('rhuman run time:', time.time()-start)

def rdepartment(num):
    "int num: number of department, 0 < num < number of human"
    start = time.time()
    columns = ['Dept_ID', 'Dname']
    deparment = []

    for i in range(num):
        dept_id = i+1
        dname = fake.unique.street_name() + ' Division'
        deparment.append([dept_id, dname])
    
    writecsv('department', columns, deparment)
    print('rdepartment run time:', time.time()-start)

def roccupation(p):
    """use after rhuman and rdepartment
    float p = probability of being owner, 0 ≤ p ≤ 1"""
    start = time.time()
    owner, officer = [],[]
    sins = pd.read_csv(config.path+'human.csv')['SIN'].tolist()
    departments = pd.read_csv(config.path+'department.csv')['Dept_ID'].tolist()
    dpmt_unused = departments.copy()

    for sin in sins:
        if dpmt_unused != []: #prioritize officer/department
            officer.append([sin, dpmt_unused.pop()])
        elif random.binomial(n=1, p=p) == 1:
            salary_group = random.choice(config.salary_group, p=config.salary_group_p)
            owner.append([sin, salary_group])
        else:
            department = random.choice(departments)
            officer.append([sin, department])

    writecsv('owner', ['SIN', 'Salary_group'], owner)
    writecsv('police_officer', ['SIN', 'Department'], officer)
    print('roccupation run time:', time.time()-start)

def rvehicle(num):
    "int num: number of vehicle, num>0"
    start = time.time()
    columns = ['VIN','Make','Price','Purchase_Method']
    vehicle = []

    for i in range(num):
        vin = fake.unique.vin()
        make = fake.vehicle_make()
        price = random.randint(config.vehicle_price_min, config.vehicle_price_max) * 10000
        pmethod = random.choice(config.purchase_method, p=config.purchase_method_p)
        vehicle.append([vin, make, price, pmethod])

    writecsv('vehicle', columns, vehicle)
    print('rvehicle run time:', time.time()-start)

def rinsurance(p):
    """use after rvihicle
    float p = probability to cover a random extra vehicle, 0 ≤ p ≤ 1"""
    start = time.time()
    columns = ['Policy_Number','VIN','Payment_Amount']
    insurance = []
    vehicles = pd.read_csv(config.path+'vehicle.csv')[["VIN", "Price"]].values.tolist()
    vnum = len(vehicles)
    for vehicle in vehicles:
        pnum = fake.unique.ean8()
        payment = round(vehicle[1]*random.rand(), 2) #0% to 100%, 2 decimal places
        insurance.append([pnum,vehicle[0], payment])
        if random.binomial(n=1, p=p) == 1:
            extra = vehicles[random.randint(0, vnum-1)]
            if extra != vehicle:
                payment = round(extra[1]*random.rand(), 2)
                insurance.append([pnum, extra[0], payment])
        
    writecsv('insurance', columns, insurance)
    print('rinsurance run time:', time.time()-start)

def rown():
    "use after rvehicle and rowner"
    start = time.time()
    columns = ['SIN','VIN']
    own = []
    sins = pd.read_csv(config.path+'owner.csv')['SIN'].tolist()
    vins = pd.read_csv(config.path+'vehicle.csv')['VIN'].tolist()
    
    sin_filled, vin_filled = False, False
    sin_unused = sins.copy()
    vin_unused = vins.copy()

    while not sin_filled or not vin_filled:
        own.append([sin_unused.pop(), vin_unused.pop()])
        if sin_unused == []:
            sin_filled = True
            sin_unused = sins.copy()
        if vin_unused == []:
            vin_filled = True
            vin_unused = vins.copy()

    writecsv('own', columns, own)
    print('rown run time:', time.time()-start)

def revent(num):
    "int num: number of events, num > 0"
    start = time.time()
    columns = ['Event_Code','Outcome','Year','Month','Day','Hour','Neighbourhood']
    event = []

    for i in range(num):
        outcome = random.choice(config.event_outcome, p=config.event_outcome_p)
        year, month, day, hour = fake.date_time_ad(start_datetime=config.event_startdate).strftime('%Y %m %d %H').split()
        neighbourhood = fake.street_name()
        event.append([i, outcome, year, month, day, hour, neighbourhood])

    writecsv('event', columns, event)
    print('revent run time:', time.time()-start)

def rstolen():
    start = time.time()
    columns = ['Event_Code','VIN']
    stolen = []
    events = pd.read_csv(config.path+'event.csv')['Event_Code'].tolist()
    vins = pd.read_csv(config.path+'vehicle.csv')['VIN'].tolist()
    event_filled, vin_filled = False, False
    event_unused = events.copy()
    vin_unused = vins.copy()

    while not event_filled or not vin_filled:
        stolen.append([event_unused.pop(), vin_unused.pop()])
        if event_unused == []:
            event_filled = True
            event_unused = events.copy()
        if vin_unused == []:
            vin_filled = True
            vin_unused = vins.copy()

    writecsv('got_stolen', columns, stolen)
    print('rstolen run time:', time.time()-start)

def rhandled():
    start = time.time()
    columns = ['Police_SIN', 'Event_Code']
    handled = []
    sins = pd.read_csv(config.path+'police_officer.csv')['SIN'].tolist()
    events = pd.read_csv(config.path+'event.csv')['Event_Code'].tolist()

    for i in events:
        sin = random.choice(sins)
        handled.append([sin, i])

    writecsv('handled', columns, handled)
    print('rhandled run time:', time.time()-start)

if __name__ == "__main__":
    rhuman(100)
    rdepartment(3)
    roccupation(0.9)
    rvehicle(100)
    rinsurance(0.5)
    rown()
    revent(100)
    rstolen()
    rhandled()