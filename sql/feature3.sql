SELECT 
    EVENT.Neighbourhood, 
    AVG(VEHICLE.price) AS average_price, 
    COUNT(VEHICLE.VIN) AS total_vehicles, 
    MIN(VEHICLE.price) AS minimum_price, 
    MAX(VEHICLE.price) AS maximum_price
FROM 
    EVENT
JOIN 
    GOT_STOLEN ON EVENT.Event_Code = GOT_STOLEN.Event_Code
JOIN 
    VEHICLE ON GOT_STOLEN.VIN = VEHICLE.VIN
WHERE 
    VEHICLE.Price IS NOT NULL
GROUP BY 
    EVENT.Neighbourhood
ORDER BY 
    average_price DESC;
