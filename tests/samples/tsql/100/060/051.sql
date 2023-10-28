SELECT ColumnA, ColumnB FROM T GROUP BY ColumnA, ColumnB;  
SELECT ColumnA + ColumnB FROM T GROUP BY ColumnA, ColumnB;  
SELECT ColumnA + ColumnB FROM T GROUP BY ColumnA + ColumnB;  
SELECT ColumnA + ColumnB + constant FROM T GROUP BY ColumnA, ColumnB;