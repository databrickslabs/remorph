-- single column

ALTER TABLE empl_info modify column empl_id unset masking policy;

-- multiple columns

ALTER TABLE empl_info MODIFY
    COLUMN empl_id UNSET MASKING POLICY
  , COLUMN empl_dob UNSET MASKING POLICY
;