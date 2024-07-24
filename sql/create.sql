DROP SCHEMA IF EXISTS Auto_Theft;
CREATE SCHEMA Auto_Theft;

USE Auto_Theft;

CREATE TABLE ACCOUNT
    (SIN VARCHAR(11) NOT NULL, 
     Username VARCHAR(50) NOT NULL,
     Password VARCHAR(50) NOT NULL,
     PRIMARY KEY (Username),
     UNIQUE(SIN));

CREATE TABLE VEHICLE
    (VIN VARCHAR(17) NOT NULL,
     Make VARCHAR(50) NOT NULL,
     PRICE DECIMAL(10,2) NOT NULL,
     Purchase_Method VARCHAR(50) NOT NULL,
     PRIMARY KEY (VIN));

CREATE TABLE INSURANCE
    (Policy_Number VARCHAR(10) NOT NULL,
     VIN VARCHAR(17) NOT NULL,
     Payment_Amount DECIMAL(10,2) NOT NULL,
     PRIMARY KEY(Policy_Number, VIN),
     FOREIGN KEY(VIN) REFERENCES VEHICLE(VIN)
        ON DELETE CASCADE
        ON UPDATE CASCADE);

CREATE TABLE EVENT 
    (Event_Code INT NOT NULL, 
     Outcome VARCHAR(50) NOT NULL, 
     Year INT NOT NULL CHECK(Year >= 1950), 
     Month INT NOT NULL CHECK(Month <= 12 AND Month >= 1), 
     Day INT NOT NULL CHECK(Day <= 31 AND Day >= 1),
     Hour INT, 
     Neighbourhood VARCHAR(50) NOT NULL,
     PRIMARY KEY(Event_Code));

CREATE TABLE GOT_STOLEN 
    (Event_Code INT NOT NULL, 
     VIN VARCHAR(17) NOT NULL, 
     PRIMARY KEY (Event_Code, VIN),
     FOREIGN KEY (Event_Code) REFERENCES EVENT(Event_Code)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
     FOREIGN KEY (VIN) REFERENCES VEHICLE(VIN)
        ON DELETE CASCADE
        ON UPDATE CASCADE);

CREATE TABLE HUMAN
    (SIN VARCHAR(11) NOT NULL, 
     Birth_date DATE NOT NULL, 
     FName VARCHAR(50) NOT NULL,
     LName VARCHAR(50) NOT NULL,
     Phone VARCHAR(50) NOT NULL,
     Email VARCHAR(50),
     PRIMARY KEY (SIN));

CREATE TABLE OWNER
    (SIN VARCHAR(11) NOT NULL, 
     Salary_group VARCHAR(10) NOT NULL, 
     PRIMARY KEY (SIN),
     FOREIGN KEY (SIN) REFERENCES HUMAN(SIN)
        ON DELETE CASCADE
        ON UPDATE CASCADE);

CREATE TABLE OWN 
    (SIN VARCHAR(11) NOT NULL, 
     VIN VARCHAR(17) NOT NULL, 
     PRIMARY KEY (SIN, VIN),
     FOREIGN KEY (SIN) REFERENCES OWNER(SIN)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
     FOREIGN KEY (VIN) REFERENCES VEHICLE(VIN)
        ON DELETE CASCADE
        ON UPDATE CASCADE);

CREATE TABLE DEPARTMENT
    (Dept_ID INT NOT NULL, 
     Dname VARCHAR(50) NOT NULL, 
     PRIMARY KEY (Dept_ID));

CREATE TABLE POLICE_OFFICER
    (SIN VARCHAR(11) NOT NULL, 
     Department INT NOT NULL, 
     PRIMARY KEY (SIN),
     FOREIGN KEY (Department) REFERENCES DEPARTMENT(Dept_ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
     FOREIGN KEY (SIN) REFERENCES HUMAN(SIN)
        ON DELETE CASCADE
        ON UPDATE CASCADE);

CREATE TABLE HANDLED
    (Police_SIN VARCHAR(11) NOT NULL, 
     Event_Code INT NOT NULL, 
     PRIMARY KEY (Police_SIN, Event_Code),
     FOREIGN KEY (Police_SIN) REFERENCES POLICE_OFFICER(SIN)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
     FOREIGN KEY (Event_Code) REFERENCES EVENT(Event_Code)
        ON DELETE CASCADE
        ON UPDATE CASCADE);
