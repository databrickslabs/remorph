MERGE INTO members m
  USING (
  SELECT id, date
  FROM signup
  WHERE DATEDIFF(day, CURRENT_DATE(), signup.date::DATE) < -30) s ON m.id = s.id
  WHEN MATCHED THEN UPDATE SET m.fee = 40;