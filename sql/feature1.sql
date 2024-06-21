Select Neighbourhood, count(*) as num_events from EVENT
Group by Neighbourhood
having count(*) >= {0};
