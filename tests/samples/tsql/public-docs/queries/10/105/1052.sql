-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-materialized-view-as-select-transact-sql?view=azure-sqldw-latest

CREATE MATERIALIZED VIEW mv_test2  
WITH (distribution = hash(i_category_id), FOR_APPEND)  
AS
SELECT MAX(i.i_rec_start_date) as max_i_rec_start_date, MIN(i.i_rec_end_date) as min_i_rec_end_date, i.i_item_sk, i.i_item_id, i.i_category_id
FROM syntheticworkload.item i  
GROUP BY i.i_item_sk, i.i_item_id, i.i_category_id