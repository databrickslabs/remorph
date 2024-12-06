-- tsql sql:
WITH PredictedScores AS ( SELECT d.id, d.feature1, d.feature2, 1.0 AS Score_new FROM #data d INNER JOIN #scoring_model m ON m.model_id = 1 ) SELECT * FROM PredictedScores;
