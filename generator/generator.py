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

for i in rhuman(10):
    print(i)