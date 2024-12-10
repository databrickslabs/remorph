-- tsql sql:
CREATE DATABASE test_geo_redundancy
WITH BACKUP_STORAGE_REDUNDANCY = 'GEO';
-- REMORPH CLEANUP: DROP DATABASE test_geo_redundancy;
