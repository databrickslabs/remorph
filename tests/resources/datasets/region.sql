--------------------------------------------------------------------------------

DROP TABLE if EXISTS region;
CREATE TABLE if NOT EXISTS region (
  r_regionkey BIGINT,
  r_name STRING,
  r_comment STRING
);
--------------------------------------------------------------------------------

INSERT INTO region (r_regionkey, r_name, r_comment) VALUES
 (0, 'AFRICA', 'lar deposits. blithely final packages cajole. regular waters are final requests. regular accounts are according to '),
 (1, 'AMERICA', 'hs use ironic, even requests. s'),
 (2, 'ASIA', 'ges. thinly even pinto beans ca'),
 (3, 'EUROPE', 'ly final courts cajole furiously final excuse'),
 (4, 'MIDDLE EAST', 'uickly special accounts cajole carefully blithely close requests. carefully final asymptotes haggle furiousl');