SELECT v, hex_encoded_string, TO_VARCHAR(b, 'UTF-8')
  FROM strings
  ORDER BY v
  ;