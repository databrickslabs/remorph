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
    RANGE_N(REAL_SELLING_DT  BETWEEN DATE '2001-01-01' AND DATE '2030-12-31' EACH INTERVAL '1' DAY ),
    RANGE_N(REFERENCE_MON_ID  BETWEEN 200501  AND 200512  EACH 1 ,
    200601  AND 200612  EACH 1 ,
    200701  AND 200712  EACH 1 ),
    RANGE_N(totalorders BETWEEN * AND *),
    RANGE_N(totalorders BETWEEN *, 100, 1000 AND *),
    RANGE_N(a  BETWEEN -110  AND 52  EACH 1 ,NO RANGE | UNKNOWN ),
    RANGE_N(SNAP_WEEK_IX  BETWEEN -110  AND 52  EACH 1 ,NO RANGE OR UNKNOWN),
    RANGE_N(a  BETWEEN -110  AND 52  EACH 1 ,NO RANGE ),
    RANGE_N(a  BETWEEN -110  AND 52  EACH 1 ,UNKNOWN ),
    RANGE_N(a  BETWEEN -110  AND 52  EACH 1 ,NO RANGE , UNKNOWN ),

    )
