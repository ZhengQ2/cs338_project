Select * from POLICE_OFFICER 
Left Join HANDLED
On POLICE_OFFICER.SIN = HANDLED.Police_SIN;