SELECT listagg(DISTINCT O_ORDERSTATUS, '|')
    FROM orders WHERE O_TOTALPRICE > 450000;

--------------------------------------+
 LISTAGG(DISTINCT O_ORDERSTATUS, '|') |
--------------------------------------+
 F|O                                  |
--------------------------------------+