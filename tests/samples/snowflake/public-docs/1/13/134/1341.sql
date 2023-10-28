CREATE TABLE strings (s1 VARCHAR COLLATE 'en', s2 VARCHAR COLLATE 'hu');
INSERT INTO strings (s1, s2) VALUES ('dzsa', COLLATE('dzsa', 'hu'));