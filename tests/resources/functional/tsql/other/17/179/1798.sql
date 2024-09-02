--Query type: DML
DECLARE @h HIERARCHYID = HIERARCHYID::GetRoot();
DECLARE @c HIERARCHYID = @h.GetDescendant(NULL, NULL);
SELECT @c.ToString() AS cToString;
DECLARE @c2 HIERARCHYID = @h.GetDescendant(@c, NULL);
SELECT @c2.ToString() AS c2ToString;
SET @c2 = @h.GetDescendant(@c, @c2);
SELECT @c2.ToString() AS c2ToStringUpdated;
SET @c = @h.GetDescendant(@c, @c2);
SELECT @c.ToString() AS cToStringUpdated;
SET @c2 = @h.GetDescendant(@c, @c2);
SELECT @c2.ToString() AS c2ToStringUpdatedAgain;
-- REMORPH CLEANUP: DROP VARIABLE @h;
-- REMORPH CLEANUP: DROP VARIABLE @c;
-- REMORPH CLEANUP: DROP VARIABLE @c2;