import datetime, config, string, csv
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

def rhuman(num): #random human list
    start = time.time()
    columns = ['sin','birth_date','fname','lname','phone','email']
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
    start = time.time()
    columns = ['dept_id', 'dname']
    deparment = []

    for i in range(num):
        dept_id = 'D' + str(i+1)
        dname = fake.unique.street_name() + ' Division'
        deparment.append([dept_id, dname])
    
    writecsv('department', columns, deparment)
    print('rdepartment run time:', time.time()-start)

def roccupation(p):
    """use after rhuman and rdepartment
    p = probability of being owner"""
    start = time.time()
    owner, officer = [],[]
    sins = pd.read_csv(config.path+'human.csv')['sin'].tolist()
    departments = pd.read_csv(config.path+'department.csv')['dept_id'].tolist()

    for sin in sins:
        if random.binomial(n=1, p=p) == 1:
            salary_group = random.choice(config.salary_group, p=config.salary_group_p)
            owner.append([sin, salary_group])
        else:
            department = random.choice(departments)
            officer.append([sin, department])

    writecsv('owner', ['sin', 'salary_group'], owner)
    writecsv('police_officer', ['sin', 'department'], officer)
    print('roccupation run time:', time.time()-start)

def rvehicle(num):
    start = time.time()
    columns = ['vin','make','price','purchase_method']
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
    p = probability to cover a random extra vehicle"""
    start = time.time()
    columns = ['policy_number','vin','payment_amount']
    insurance = []
    vehicles = pd.read_csv(config.path+'vehicle.csv')[["vin", "price"]].values.tolist()
    vnum = len(vehicles)
    for vehicle in vehicles:
        pnum = fake.unique.ean8()
        payment = round(vehicle[1]*random.rand(), 2)
        insurance.append([pnum,vehicle[0], payment])
        if random.binomial(n=1, p=p) == 1:
            extra = vehicles[random.randint(0, vnum-1)]
            if extra != vehicle:
                payment = round(extra[1]*random.rand(), 2)
                insurance.append([pnum, extra[0], payment])
        
    writecsv('insurance', columns, insurance)
    print('rinsurance run time:', time.time()-start)

def rown():
    start = time.time()
    columns = ['vin','sin']
    own = []
    vins = pd.read_csv(config.path+'vehicle.csv')['vin'].tolist()
    sins = pd.read_csv(config.path+'owner.csv')['sin'].tolist()
    
    vin_filled, sin_filled = False, False
    vin_unused = vins.copy()
    sin_unused = sins.copy()

    while not sin_filled or not vin_filled:
        own.append([vin_unused.pop(0), sin_unused.pop(0)])
        if vin_unused == []:
            vin_filled = True
            vin_unused = vins.copy()
        if sin_unused == []:
            sin_filled = True
            sin_unused = sins.copy()

    writecsv('own', columns, own)
    print('rown run time:', time.time()-start)

def revent(num):
    start = time.time()
    columns = ['event_code','outcome','year','month','day','hour','neighbourhood']
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
    columns = ['event_code','vin']
    stolen = []
    events = pd.read_csv(config.path+'event.csv')['event_code'].tolist()
    vins = pd.read_csv(config.path+'vehicle.csv')['vin'].tolist()
    event_filled, vin_filled = False, False
    event_unused = events.copy()
    vin_unused = vins.copy()

    while not event_filled or not vin_filled:
        stolen.append([event_unused.pop(0), vin_unused.pop(0)])
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
    columns = ['police_sin', 'event_code']
    handled = []
    sins = pd.read_csv(config.path+'police_officer.csv')['sin'].tolist()
    events = pd.read_csv(config.path+'event.csv')['event_code'].tolist()

    for i in events:
        sin = random.choice(sins)
        handled.append([sin, i])

    writecsv('handled', columns, handled)
    print('rhandled run time:', time.time()-start)

if __name__ == "__main__":
    rhuman(10000)
    rdepartment(10)
    roccupation(0.99)
    rvehicle(15000)
    rinsurance(0.5)
    rown()
    revent(10000)
    rstolen()
    rhandled()