CREATE TABLE temporary_hll_state_for_manitoba AS
 SELECT HLL_ACCUMULATE(postal_code) as h_a_p_c
  FROM postal_data
  WHERE province = 'Manitoba'
  ;