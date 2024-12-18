-- tsql sql:
CREATE TABLE orders (order_ID INTEGER, total_cost REAL, quantity INTEGER, city VARCHAR, state VARCHAR);
INSERT INTO orders (order_ID, total_cost, quantity, city, state)
VALUES (1, 10.00, 2, 'NY', 'NY'),
       (2, 20.00, 4, 'LA', 'CA'),
       (3, 30.00, 6, 'CHI', 'IL'),
       (4, 40.00, 8, 'HOU', 'TX');
