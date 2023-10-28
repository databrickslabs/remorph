SELECT state, bushels,
        RANK() OVER (ORDER BY bushels DESC),
        DENSE_RANK() OVER (ORDER BY bushels DESC)
    FROM corn_production;