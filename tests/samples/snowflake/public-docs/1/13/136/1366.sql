SELECT v, LPAD(v, 10, ' '),             
          LPAD(v, 10, '$')
    FROM demo
    ORDER BY v;