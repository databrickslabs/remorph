-- see https://docs.snowflake.com/en/sql-reference/constructs/connect-by

-- The components of a car.
CREATE TABLE components (
    description VARCHAR,
    quantity INTEGER,
    component_ID INTEGER,
    parent_component_ID INTEGER
    );

INSERT INTO components (description, quantity, component_ID, parent_component_ID) VALUES
    ('car', 1, 1, 0),
       ('wheel', 4, 11, 1),
          ('tire', 1, 111, 11),
          ('#112 bolt', 5, 112, 11),
          ('brake', 1, 113, 11),
             ('brake pad', 1, 1131, 113),
       ('engine', 1, 12, 1),
          ('piston', 4, 121, 12),
          ('cylinder block', 1, 122, 12),
          ('#112 bolt', 16, 112, 12)   -- Can use same type of bolt in multiple places
    ;