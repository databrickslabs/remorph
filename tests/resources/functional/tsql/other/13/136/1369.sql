--Query type: DDL
WITH ClassifierInfo AS (
    SELECT 'classifierB' AS ClassifierName, 'wgReports' AS WorkloadGroup, 'userloginB' AS MemberName, 'MEDIUM' AS Importance, 'productreport' AS WLM_Label
)
SELECT *
FROM ClassifierInfo;
