SELECT oldt.* ,newt.*
  FROM my_table BEFORE(STATEMENT => '8e5d0ca9-005e-44e6-b858-a8f5b37c5726') AS oldt
    FULL OUTER JOIN my_table AT(STATEMENT => '8e5d0ca9-005e-44e6-b858-a8f5b37c5726') AS newt
    ON oldt.id = newt.id
WHERE oldt.id IS NULL OR newt.id IS NULL;