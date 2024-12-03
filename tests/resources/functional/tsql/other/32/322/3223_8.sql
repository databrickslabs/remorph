--Query type: DDL
CREATE TABLE region_nation (
    region_id TINYINT,
    region_name VARCHAR(10),
    nation_name VARCHAR(10)
);

INSERT INTO region_nation
SELECT *
FROM (
    VALUES
        (1, 'asia', 'china'),
        (2, 'america', 'usa'),
        (3, 'europe', 'germany')
) AS region_nation (region_id, region_name, nation_name)
WHERE region_id = 1;
