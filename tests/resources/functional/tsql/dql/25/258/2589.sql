--Query type: DQL
WITH temp_result AS (SELECT EXP(LOG(20)) AS exp_log, LOG(EXP(20)) AS log_exp)
SELECT exp_log, log_exp
FROM temp_result
