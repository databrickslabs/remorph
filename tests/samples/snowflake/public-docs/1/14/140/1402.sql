SELECT column1, ASCII(column1)
  FROM (values('!'), ('A'), ('a'), ('bcd'), (''), (null));