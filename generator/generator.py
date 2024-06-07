import random, datetime, config, string

def ran(slst):
    return random.choice(slst.split(','))

def rbdate():
    start = datetime.datetime.strptime(config.date_start, "%Y-%m-%d")
    end = datetime.datetime.strptime(config.date_end, "%Y-%m-%d")
    return (start + datetime.timedelta(random.randrange((end - start).days))).strftime("%Y-%m-%d")

def rsin():
    sin = ''
    sum = 0
    for i in range(8):
        num = random.randrange(10)
        sin += str(num)
        if i%2 == 0:
            sum += num
        else:
            sum += 2*num
    sin += str(10 - sum%10)
    return int(sin)

def rphone():
    num = random.choice(config.area_code.split(','))
    for i in range(7):
        num += str(random.randrange(10))
    return num

def remail():
    email = ''
    for i in range(random.randrange(5,20)):
        email += random.choice(string.digits+string.ascii_letters)
    email += '@gmail.com'
    return email

def rhuman(num):
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