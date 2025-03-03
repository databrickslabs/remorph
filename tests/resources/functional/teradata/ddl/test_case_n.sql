-- teradata sql:
CREATE SET TABLE tbl1 ,FALLBACK ,
     NO BEFORE JOURNAL,
     NO AFTER JOURNAL,
     CHECKSUM = DEFAULT,
     DEFAULT MERGEBLOCKRATIO,
     MAP = TD_MAP1
     (
      col1 DECIMAL(14,0) NOT NULL
     )
PRIMARY INDEX col2 ( col3 )
PARTITION BY (
    CASE_N(a =  'IND',b =  'USA',c =  'CAN',NO CASE OR UNKNOWN)

    );
--databricks sql:
CREATE TABLE tbl1 (
                                              col1 DECIMAL(14, 0) NOT NULL
)
