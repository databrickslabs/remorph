-- single column

ALTER TABLE empl_info MODIFY COLUMN empl_id SET MASKING POLICY mask_empl_id;

-- multiple columns

ALTER TABLE empl_info MODIFY
    COLUMN empl_id SET MASKING POLICY mask_empl_id
  , COLUMN empl_dob SET MASKING POLICY mask_empl_dob
;