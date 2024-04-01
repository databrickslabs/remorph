from pathlib import Path


def source_and_databricks_sql(*file_names):
    sql_tuples = []
    for file in file_names:
        abs_path = Path(__file__).parent.parent / file
        with open(abs_path, 'r') as file_content:
            content = file_content.read()

        parts = content.split('-- source:')
        for part in parts[1:]:
            source_sql, databricks_sql = part.split('-- databricks_sql:')
            source_sql = source_sql.strip().rstrip(';')
            # print(source_sql)
            databricks_sql = databricks_sql.strip().rstrip(';').replace('\\', '')
            # print(databricks_sql)
            sql_tuples.append((databricks_sql.replace('\\', ''), source_sql.replace('\\', '')))
            # print(sql_tuples)

    return sql_tuples
