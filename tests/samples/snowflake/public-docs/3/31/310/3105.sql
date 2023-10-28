-- single column

ALTER VIEW user_info_v MODIFY COLUMN ssn_number SET MASKING POLICY ssn_mask_v;

-- multiple columns

ALTER VIEW user_info_v MODIFY
    COLUMN ssn_number SET MASKING POLICY ssn_mask_v
  , COLUMN dob SET MASKING POLICY dob_mask_v
;