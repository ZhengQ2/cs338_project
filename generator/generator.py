import random, datetime, config, string

def ran(slst): #random select from string-list
    return random.choice(slst.split(','))

def rbdate(): #random birth date
    start = datetime.datetime.strptime(config.date_start, "%Y-%m-%d")
    end = datetime.datetime.strptime(config.date_end, "%Y-%m-%d")
    return (start + datetime.timedelta(random.randrange((end - start).days))).strftime("%Y-%m-%d")

def rsin(): #random sin
    sin = ran(config.sin_first) #first digit is region code
    sum = int(sin)
    for i in range(7):
        num = random.randrange(10)
        sin += str(num)
        if i%2 == 0:
            sum += 2*num
        else:
            sum += num
    sin += str(10 - sum%10) #odd digit int + 2*even digit int is divisible by 10
    return int(sin)

def rphone(): #random phone
    num = ran(config.area_code) #first 3 digits is area code
    for i in range(7):
        num += str(random.randrange(10))
    return num

def remail(): #random email
    email = ''
    for i in range(random.randrange(5,20)):
        email += random.choice(string.digits+string.ascii_letters)
    email += '@gmail.com'
    return email

def rhuman(num): #random human list
    human = [['Fname','Lname','Sex','SIN','Bdate','Phone','Email']]
    sins = []
    for i in range(num):
        while True:
            sin = rsin()
            if sin not in sins:
                sins.append(sin)
                break
    for i in range(num):
        human.append([ran(config.fname), ran(config.lname), ran(config.sex), sins[i], rbdate(), rphone(), remail()])
    return human

def rcar(num): #random car
    car = [['VIN','Make','Price','PMethod','Dealer']]

    # Generate a random VIN
    wmi_chars = string.ascii_uppercase + string.digits
    vds_chars = string.ascii_uppercase + string.digits
    vis_chars = string.digits
    
    # Generate the WMI (3 characters)
    wmi = ''.join(random.choices(wmi_chars, k=3))
    
    # Generate the VDS (6 characters)
    vds = ''.join(random.choices(vds_chars, k=6))
    
    # The 9th character is a check digit which is often a number or 'X'
    check_digit = random.choice(string.digits + 'X')
    
    # Generate the VIS (8 characters)
    vis = ''.join(random.choices(vis_chars, k=8))
    
    # Concatenate all parts to form the VIN
    vin = wmi + vds + check_digit + vis

    for i in range(num):
        car.append([vin,ran(config.car_make),random.randrange(1000000),None,None])
    return car

print(rcar(1))