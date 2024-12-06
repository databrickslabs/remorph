-- tsql sql:
WITH customer_info AS ( SELECT c_name, c_password FROM ( VALUES ('customer1', 'password1'), ('customer2', 'password2') ) AS customers (c_name, c_password) ) SELECT c_name FROM customer_info WHERE PWDCOMPARE('password1', c_password) = 1 ;
