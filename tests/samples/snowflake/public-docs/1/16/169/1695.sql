SELECT RLIKE('800-456-7891', $$[2-9]\d{2}-\d{3}-\d{4}$$) AS matches_phone_number;


SELECT RLIKE('jsmith@email.com',$$\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$$) AS matches_email_address;
