SELECT ROW_NUMBER() OVER (ORDER BY seq4()) 
    FROM TABLE(generator(rowcount => 10));