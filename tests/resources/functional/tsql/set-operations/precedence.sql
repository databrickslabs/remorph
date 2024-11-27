--
-- Verify the precedence rules are being correctly handled. Order of evaluation when chaining is:
-- 1. Brackets.
-- 2. INTERSECT
-- 3. UNION and EXCEPT, evaluated left to right.
--

-- tsql sql:

-- Verifies UNION/EXCEPT as left-to-right, with brackets.
SELECT 1
UNION
SELECT 2
EXCEPT
(SELECT 3
 UNION ALL
 SELECT 4)

INTERSECT

-- Verifies UNION/EXCEPT as left-to-right when the order is reversed.
SELECT 5
EXCEPT
SELECT 6
UNION
SELECT 7

INTERSECT

-- Verifies brackets have precedence over INTERSECT.
(SELECT 8
 INTERSECT
 SELECT 9)

INTERSECT

-- Not needed: just confirms helps us confirm that INTERSECT is also left-to-right.
SELECT 10;


-- databricks sql:
    (
        (
            (
                ((SELECT 1) UNION (SELECT 2))
            EXCEPT
                ((SELECT 3) UNION ALL (SELECT 4))
            )
        INTERSECT
            (
                ((SELECT 5) EXCEPT (SELECT 6))
            UNION
                (SELECT 7)
            )
        )
    INTERSECT
        ((SELECT 8) INTERSECT (SELECT 9))
    )
INTERSECT
    (SELECT 10);
