-- see https://docs.snowflake.com/en/sql-reference/sql/alter-view

-- single column

ALTER VIEW user_info_v modify column ssn_number unset masking policy;

-- multiple columns

ALTER VIEW user_info_v modify
    column ssn_number unset masking policy
  , column dob unset masking policy
;