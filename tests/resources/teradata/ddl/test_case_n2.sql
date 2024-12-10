/***************************************************************************************************
* SUB-VERSION                                                                                      *
* ================================================================================================ *
* SVN Infostamp             (DO NOT EDIT THE NEXT 8 LINES!)                                        *
* ================================================================================================ *
* $Id: SPH_CNTRY_CRDNTR.ddl 158373 2024-10-02 16:01:21Z UDEPLOY $
* $LastChangedBy: UDEPLOY $
* $LastChangedDate: 2024-10-02 18:01:21 +0200 (śr., 02 paź 2024) $
* $LastChangedRevision: 158373 $
* ================================================================================================ *
* SVN Info END                                                                                     *
***************************************************************************************************/
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
    CASE_N(a =  'FRA',b =  'ZRH',c =  'MUC',UNKNOWN)

    )
--,NO CASE OR UNKNOWN