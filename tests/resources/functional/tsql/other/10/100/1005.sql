--Query type: DDL
CREATE TABLE #CustomerReviews
(
    ReviewerName nvarchar(255),
    EmailAddress nvarchar(255),
    Comments nvarchar(max)
);

INSERT INTO #CustomerReviews
(
    ReviewerName,
    EmailAddress,
    Comments
)
VALUES
(
    'John Doe',
    'john.doe@example.com',
    'This is a review'
),
(
    'Jane Doe',
    'jane.doe@example.com',
    'This is another review'
);

CREATE FULLTEXT INDEX ON #CustomerReviews
(
    ReviewerName LANGUAGE 1033,
    EmailAddress LANGUAGE 1033,
    Comments LANGUAGE 1033
)
KEY INDEX PK_CustomerReviews_CustomerReviewID;

SELECT *
FROM #CustomerReviews;

-- REMORPH CLEANUP: DROP TABLE #CustomerReviews;