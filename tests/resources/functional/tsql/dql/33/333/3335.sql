-- tsql sql:
WITH reviews AS ( SELECT review_comments, review_id FROM ( VALUES ('This bike has great control.', 1), ('The control of this bike is amazing.', 2) ) AS reviews(review_comments, review_id) ) SELECT review_comments FROM reviews WHERE review_comments LIKE '%bike%control%' OR review_comments LIKE '%control%bike%';
