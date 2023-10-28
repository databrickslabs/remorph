CREATE TABLE double_demo (variant1 VARIANT);
INSERT INTO double_demo (variant1)
    SELECT TO_VARIANT(3.14);