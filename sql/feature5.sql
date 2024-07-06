SELECT 
    VEHICLE.Make, 
    AVG(INSURANCE.Payment_Amount) OVER (PARTITION BY VEHICLE.Make) AS avg_insurance_payment_by_make,
    SUM(INSURANCE.Payment_Amount) OVER (PARTITION BY VEHICLE.Make) AS sum_insurance_payment_by_make
FROM 
    INSURANCE
JOIN 
    VEHICLE ON INSURANCE.VIN = VEHICLE.VIN;
