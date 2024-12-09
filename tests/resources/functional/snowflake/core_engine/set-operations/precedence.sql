--
-- Verify the precedence rules are being correctly handled. Order of evaluation when chaining is:
-- 1. Brackets.
-- 2. INTERSECT
-- 3. UNION and EXCEPT, evaluated left to right.
--

-- snowflake sql:

-- Verifies UNION/EXCEPT/MINUS as left-to-right (1/3), with brackets.
(SELECT 1
 UNION
 SELECT 2
 EXCEPT
 SELECT 3
 MINUS
 (SELECT 4
  UNION
  SELECT 5))

UNION ALL

-- Verifies UNION/EXCEPT/MINUS as left-to-right (2/3) when the order is rotated from the previous.
(SELECT 6
 EXCEPT
 SELECT 7
 MINUS
 SELECT 8
 UNION
 SELECT 9)

UNION ALL

-- Verifies UNION/EXCEPT/MINUS as left-to-right (3/3) when the order is rotated from the previous.
(SELECT 10
 MINUS
 SELECT 11
 UNION
 SELECT 12
 EXCEPT
 SELECT 13)

UNION ALL

-- Verifies that INTERSECT has precedence over UNION/EXCEPT/MINUS.
(SELECT 14
 UNION
 SELECT 15
 EXCEPT
 SELECT 16
 MINUS
 SELECT 17
 INTERSECT
 SELECT 18)

UNION ALL

-- Verifies that INTERSECT is left-to-right, although brackets have precedence.
(SELECT 19
 INTERSECT
 SELECT 20
 INTERSECT
 (SELECT 21
  INTERSECT
  SELECT 22));

-- databricks sql:

    (
        (
            (
                (
                    (
                        ((SELECT 1) UNION (SELECT 2))
                    EXCEPT
                        (SELECT 3)
                    )
                EXCEPT
                    ((SELECT 4) UNION (SELECT 5))
                )
            UNION ALL
                (
                    (
                        ((SELECT 6) EXCEPT (SELECT 7))
                    EXCEPT
                        (SELECT 8)
                    )
                UNION
                    (SELECT 9)
                )
            )
        UNION ALL
            (
                (
                    ((SELECT 10) EXCEPT (SELECT 11))
                UNION
                    (SELECT 12)
                )
            EXCEPT
                (SELECT 13)
            )
        )
    UNION ALL
        (
            (
                ((SELECT 14) UNION (SELECT 15))
            EXCEPT
                (SELECT 16)
            )
        EXCEPT
            ((SELECT 17) INTERSECT (SELECT 18))
        )
    )
UNION ALL
    (
        ((SELECT 19) INTERSECT (SELECT 20))
    INTERSECT
        ((SELECT 21) INTERSECT (SELECT 22))
    );
