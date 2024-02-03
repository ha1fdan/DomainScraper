# Export MySQL data to csv

```sql
SELECT domain
INTO OUTFILE '/home/name/domains_export.csv'
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
FROM scraped_domains
WHERE LENGTH(domain) = 6;
```

You can change `WHERE LENGTH(domain) = 6;` to the length of the domain including the TLD.