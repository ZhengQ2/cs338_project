Select 
OWN.VIN as VIN, 
HUMAN.SIN as OWNER_SIN, 
HUMAN.FName as OWNER_FirstName, 
HUMAN.LName as OWNER_LastName, 
HUMAN.Phone as OWNER_Phone, 
HUMAN.Email as OWNER_Email
From OWN
Left join HUMAN
On OWN.SIN = HUMAN.SIN
Where OWN.VIN = "{0}";
