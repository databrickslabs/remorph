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
      RANGE_N(a  BETWEEN -110  AND 52  EACH 1 ,NO RANGE | UNKNOWN ),
    RANGE_N(SNAP_WEEK_IX  BETWEEN -110  AND 52  EACH 1 ,NO RANGE OR UNKNOWN),
    RANGE_N(a  BETWEEN -110  AND 52  EACH 1 ,NO RANGE ),
    RANGE_N(a  BETWEEN -110  AND 52  EACH 1 ,UNKNOWN ),
    RANGE_N(a  BETWEEN -110  AND 52  EACH 1 ,NO RANGE , UNKNOWN )
    )

-- RANGE_N(c  BETWEEN -110  AND 52  EACH 1 ,UNKNOWN )
--( RANGE_N(SNAP_WEEK_IX  BETWEEN -110  AND 52  EACH 1 ,
--NO RANGE OR UNKNOWN),( RANGE_N(b  BETWEEN -110  AND 52  EACH 1 ,
--NO RANGE )))
