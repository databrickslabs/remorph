--Snow sql
CREATE SET TABLE db_ods_plus.SPH_CNTRY_CRDNTR ,FALLBACK ,
     NO BEFORE JOURNAL,
     NO AFTER JOURNAL,
     CHECKSUM = DEFAULT,
     DEFAULT MERGEBLOCKRATIO,
     MAP = TD_MAP1
     (
      SPH_CNTRY_CRDNTR_ID DECIMAL(14,0) NOT NULL
     )
PRIMARY INDEX XUPI_SPH_CNTRY_CRDNTR ( SPH_CNTRY_CRDNTR_ID )
PARTITION BY (
    CASE_N(a =  'FRA',b =  'ZRH',c =  'MUC')
    );

--dbsql
CREATE TABLE db_ods_plus.SPH_CNTRY_CRDNTR (
                                              SPH_CNTRY_CRDNTR_ID DECIMAL(14, 0) NOT NULL
)
