select * from target;


Select * from src;


-- Following statement joins all three rows in src against the single row in target
UPDATE target
  SET v = src.v
  FROM src
  WHERE target.k = src.k;
