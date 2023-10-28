select *
  from table(my_db.information_schema.tag_references_all_columns('my_table', 'table'));