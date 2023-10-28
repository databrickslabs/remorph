SELECT O_ORDERSTATUS, listagg(O_CLERK, ', ') WITHIN GROUP (ORDER BY O_TOTALPRICE DESC)
    FROM orders WHERE O_TOTALPRICE > 450000 GROUP BY O_ORDERSTATUS;

---------------+--------------------------------------------------------------------+
 O_ORDERSTATUS |  LISTAGG(O_CLERK, ', ') WITHIN GROUP (ORDER BY O_TOTALPRICE DESC)  |
---------------+--------------------------------------------------------------------+
 O             | Clerk#000000220, Clerk#000000411, Clerk#000000114                  |
 F             | Clerk#000000508, Clerk#000000136, Clerk#000000521, Clerk#000000386 |
---------------+--------------------------------------------------------------------+