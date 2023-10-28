select *
  from table(my_db.information_schema.tag_references('my_table', 'table'));