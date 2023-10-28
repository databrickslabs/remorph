SELECT v, b, 
    -- Convert binary -> hex-encoded-string -> string.
    TRY_HEX_DECODE_STRING(TO_VARCHAR(b)) 
  FROM hex;