-- Returns error
  INSERT ALL
    INTO t1 VALUES (src1.key, a)
  SELECT src1.a AS a
  FROM src1, src2 WHERE src1.key = src2.key;

-- Completes successfully
  INSERT ALL
    INTO t1 VALUES (key, a)
  SELECT src1.key AS key, src1.a AS a
  FROM src1, src2 WHERE src1.key = src2.key;