--Query type: DQL
SELECT DIFFERENCE('Similarity', 'Likeness') AS SimilarityScore FROM (VALUES ('Similarity', 'Likeness')) AS TempTable(String1, String2);
