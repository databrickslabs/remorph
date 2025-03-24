-- Service Tiers

SELECT  db.name as database,
        ds.edition,
        ds.service_objective,
        CURRENT_TIMESTAMP as extract_ts
FROM  SYS.DATABASE_SERVICE_OBJECTIVES AS ds
          JOIN  SYS.DATABASES AS db
                ON ds.database_id = db.database_id
