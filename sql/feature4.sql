Case 
when user_input is numerical 
then select * from Vehicle where VIN in 
    (select VIN from INSURANCE where INSURANCE.payment_amt <= user_input)
when user_input is string
then (Case when user_input not in Make then NA
           Else (select * from Vehicle where Vehicle.Make = user_input))