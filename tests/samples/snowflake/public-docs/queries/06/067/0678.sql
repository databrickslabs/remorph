-- see https://docs.snowflake.com/en/sql-reference/constructs/group-by-grouping-sets

INSERT INTO nurses
    (ID, full_name, medical_license, radio_license)
  VALUES
    (101, 'Lily Vine', 'LVN', NULL),
    (102, 'Larry Vancouver', 'LVN', NULL),
    (172, 'Rhonda Nova', 'RN', NULL)
    ;