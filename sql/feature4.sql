Case 
when {0} is numerical 
then select * from Vehicle where VIN in 
    (select VIN from INSURANCE where INSURANCE.payment_amt <= {0})
when {0} is string
then (Case when {0} not in Make then NA
           Else (select * from Vehicle where Vehicle.Make = {0}));
