-- teradata sql:
CREATE SET TABLE TBL1 ,FALLBACK ,
     NO BEFORE JOURNAL,
     NO AFTER JOURNAL,
     CHECKSUM = DEFAULT,
     DEFAULT MERGEBLOCKRATIO,
     MAP = TD_MAP1
     (
      COL1 DECIMAL(14,0) NOT NULL
     )
PRIMARY INDEX COL1 ( COL2 )
PARTITION BY (
    RANGE_N(COL1  BETWEEN DATE '2001-01-01' AND DATE '2030-12-31' EACH INTERVAL '1' DAY ),
    RANGE_N(COL1  BETWEEN 200501  AND 200512  EACH 1 ,
    200601  AND 200612  EACH 1 ,
    200701  AND 200712  EACH 1 ),
    RANGE_N(totalorders BETWEEN * AND *),
    RANGE_N(totalorders BETWEEN *, 100, 1000 AND *),
    RANGE_N(a  BETWEEN -110  AND 52  EACH 1 ,NO RANGE | UNKNOWN ),
    RANGE_N(COL2  BETWEEN -110  AND 52  EACH 1 ,NO RANGE OR UNKNOWN),
    RANGE_N(a  BETWEEN -110  AND 52  EACH 1 ,NO RANGE ),
    RANGE_N(a  BETWEEN -110  AND 52  EACH 1 ,UNKNOWN ),
    RANGE_N(a  BETWEEN -110  AND 52  EACH 1 ,NO RANGE , UNKNOWN ),

    );

--databricks sql:
CREATE TABLE TBL1 (
                                              COL1 DECIMAL(14, 0) NOT NULL
)
