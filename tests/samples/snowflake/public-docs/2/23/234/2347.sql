select listagg(x, ', ') within group (ORDER BY last_name collate 'sp')
    from table1
    ORDER BY last_name;