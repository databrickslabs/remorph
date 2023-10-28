SELECT * FROM invoices
    WHERE amount < (
                   SELECT AVG(amount)
                       FROM invoices
                   )
    ;