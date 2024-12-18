-- tsql sql:
CREATE VIEW product_catalog AS
    (SELECT p_size, CONCAT('https://example.com/', p_relative_path) AS presigned_url, p_tags
     FROM (VALUES ('large', 'path/to/large.jpg', 'tag1,tag2'), ('small', 'path/to/small.jpg', 'tag3,tag4')) AS products(p_size, p_relative_path, p_tags));
    -- REMORPH CLEANUP: DROP VIEW product_catalog;
