SELECT v, LENGTH(v),
       TO_VARCHAR(b_hex, 'HEX')       AS b_hex,    LENGTH(b_hex),  
       TO_VARCHAR(b_base64, 'BASE64') AS b_base64, LENGTH(b_base64),
       TO_VARCHAR(b_utf8, 'UTF-8')    AS b_utf8,   LENGTH(b_utf8)
  FROM binary_table;