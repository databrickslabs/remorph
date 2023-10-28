BEGIN WORK;
DELETE FROM leased_bicycles 
    USING (SELECT bicycle_ID AS bicycle_ID FROM returned_bicycles) AS returned
    WHERE leased_bicycles.bicycle_ID = returned.bicycle_ID;
TRUNCATE TABLE returned_bicycles;
COMMIT WORK;