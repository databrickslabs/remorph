CREATE TABLE IF NOT EXISTS metrics (
    recon_table_id BIGINT NOT NULL,
    recon_metrics STRUCT<
                        row_comparison: STRUCT<
                                                missing_in_source: INTEGER,
                                                missing_in_target: INTEGER
                                              >,
                        column_comparison: STRUCT<
                                                   absolute_mismatch: INTEGER,
                                                   threshold_mismatch: INTEGER,
                                                   mismatch_columns: STRING
                                                 >,
                        schema_comparison: BOOLEAN
                    >,
    run_metrics STRUCT<
                        status: BOOLEAN NOT NULL,
                        run_by_user: STRING NOT NULL,
                        exception_message: STRING
                       > NOT NULL,
    inserted_ts TIMESTAMP NOT NULL
);