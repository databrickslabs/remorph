ALTER TABLE <table_name>
    { ALTER | MODIFY } { CONSTRAINT <name> | PRIMARY KEY | { UNIQUE | FOREIGN KEY } (<column_name>, [ ... ] ) }
    { [ [ NOT ] ENFORCED ] [ VALIDATE | NOVALIDATE ] [ RELY | NORELY ] };