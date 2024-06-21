SELECT 
    event.neighborhood, 
    AVG(vehicle.price) AS average_price, 
    COUNT(vehicle.vin) AS total_vehicles, 
    MIN(vehicle.price) AS minimum_price, 
    MAX(vehicle.price) AS maximum_price
FROM 
    event
JOIN 
    got_stolen ON event.event_code = got_stolen.event_code
JOIN 
    vehicle ON got_stolen.vin = vehicle.vin
WHERE 
    vehicle.price IS NOT NULL
GROUP BY 
    event.neighborhood
ORDER BY 
    average_price DESC;