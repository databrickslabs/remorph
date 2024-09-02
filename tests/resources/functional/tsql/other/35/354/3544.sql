--Query type: DCL
CREATE TABLE Users
(
    UserName VARCHAR(50),
    Role VARCHAR(50)
);

INSERT INTO Users (UserName, Role)
VALUES ('JohnDoe', 'Manager');

DENY VIEW DEFINITION ON Users TO JohnDoeLogin;

SELECT * FROM Users;
-- REMORPH CLEANUP: DROP TABLE Users;