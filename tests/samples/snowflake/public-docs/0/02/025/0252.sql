SELECT * FROM (SELECT seq2(0), seq1(1) FROM table(generator(rowCount => 132))) ORDER BY seq2(0) LIMIT 7 OFFSET 125;
