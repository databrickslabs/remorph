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
PRIMARY INDEX COL2 ( COL3 )
PARTITION BY (
    CASE_N(a =  'IND',b =  'USA',c =  'CAN',UNKNOWN)
    );

--databricks sql:
CREATE TABLE TBL1 (
                                              COL1 DECIMAL(14, 0) NOT NULL
);
