--Query type: DCL
CREATE TABLE Users (UserName sysname);
INSERT INTO Users (UserName) VALUES ('MarketingTeam');

CREATE USER MarketingTeam WITHOUT LOGIN;

GRANT EXECUTE ON xp_sendmail TO MarketingTeam;

-- REMORPH CLEANUP: DROP USER MarketingTeam;
-- REMORPH CLEANUP: DROP TABLE Users;