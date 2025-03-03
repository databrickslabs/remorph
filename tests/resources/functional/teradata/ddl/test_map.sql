-- teradata sql:
CREATE MULTISET TABLE NEW_TABLE_NAME ,FALLBACK ,
     NO BEFORE JOURNAL,
     NO AFTER JOURNAL,
     CHECKSUM = DEFAULT,
     DEFAULT MERGEBLOCKRATIO,
     MAP = TD_MAP1
     (
      COL1 DECIMAL(9,2) COMPRESS (0.00 ,105.00 ,18.00  ),
      COL2 DECIMAL(9,2) COMPRESS (0.00 ,105.00),
      COL3 DECIMAL(18,4),
      COL4 DECIMAL(18,4),
      COL5 DECIMAL(18,4),
      COL6 DECIMAL(18,4),
      COL7 TIMESTAMP(0))
PRIMARY INDEX ( COL1 ,COL2 ,COL3 )
PARTITION BY ( RANGE_N(COL1 BETWEEN -110 AND 52 EACH 1,
 NO RANGE OR UNKNOWN),RANGE_N(COL2 BETWEEN 202302 AND 203012 EACH 1,
 NO RANGE OR UNKNOWN),CASE_N(
COL3 = 'IND',
 NO CASE OR UNKNOWN) );

--databricks sql:
CREATE TABLE NEW_TABLE_NAME (
                                COL1 DECIMAL(9, 2),
                                COL2 DECIMAL(9, 2),
                                COL3 DECIMAL(18, 4),
                                COL4 DECIMAL(18, 4),
                                COL5 DECIMAL(18, 4),
                                COL6 DECIMAL(18, 4),
                                COL7 TIMESTAMP
)

