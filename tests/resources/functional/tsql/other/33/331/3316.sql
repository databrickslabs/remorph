-- tsql sql:
INSERT INTO Production.ProductReview (ProductID, ReviewerName, EmailAddress, Rating, Comments)
SELECT Product_ID, Reviewer_Name, Email_Address, Rating, Comments
FROM (
    VALUES
        (1, 'John Doe', 'john@example.com', 4, 'Good product'),
        (2, 'Jane Smith', 'jane@example.com', 5, 'Excellent product'),
        (3, 'Bob Johnson', 'bob@example.com', 3, 'Average product')
) AS Product_Review (Product_ID, Reviewer_Name, Email_Address, Rating, Comments)
