Select Neighbourhood, count(*) as num_events 
From EVENT
Group by Neighbourhood
having count(*) >= {0};
