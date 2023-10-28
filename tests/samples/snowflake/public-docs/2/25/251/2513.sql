CREATE TABLE demo (radius DOUBLE, v_radius VARIANT);
INSERT INTO demo (radius) VALUES (2.0);
UPDATE demo SET v_radius = TO_VARIANT(radius);