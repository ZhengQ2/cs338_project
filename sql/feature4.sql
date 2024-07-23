SELECT *
FROM EVENT
ORDER BY
    Year DESC,
    Day DESC,
    CASE
        WHEN Hour IS NULL OR Hour NOT BETWEEN 0 AND 24 THEN NULL
        ELSE Hour
    END DESC
Limit %s;

