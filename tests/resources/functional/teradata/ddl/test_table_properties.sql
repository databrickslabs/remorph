-- teradata sql:
CREATE SET TABLE DB_FLIGHT_STATS.FSTATS_INFO_LOADED_DATA_HIST ,NO FALLBACK ,
     NO BEFORE JOURNAL,
     NO AFTER JOURNAL,
     CHECKSUM = DEFAULT,
     DEFAULT MERGEBLOCKRATIO
     (
      loaded_timestamp string default 's',
      co_upd_tms TIMESTAMP(0))
PRIMARY INDEX ( loaded_timestamp );


--databricks sql:
CREATE TABLE DB_FLIGHT_STATS.FSTATS_INFO_LOADED_DATA_HIST (
                                                              loaded_timestamp STRING DEFAULT 's',
                                                              co_upd_tms TIMESTAMP
) TBLPROPERTIES ('delta.feature.allowColumnDefaults' = 'supported')
