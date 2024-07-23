# Reconcile Config

Consider the below tables that we want to reconcile:

| categroy | catalog        | schema        | table_name   | schema                                                                                                                                          | primary_key |
|----------|----------------|---------------|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
| source   | source_catalog | source_schema | product_prod | p_id INT,<br>p_name STRING,<br>price NUMBER,<br>discount DECIMAL(5,3),<br>offer DOUBLE,<br>creation_date DATE<br>comment STRING<br>             | p_id        |
| target   | target_catalog | target_schema | product      | product_id INT,<br>product_name STRING,<br>price NUMBER,<br>discount DECIMAL(5,3),<br>offer DOUBLE,<br>creation_date DATE<br>comment STRING<br> | product_id  |

## Run with Drop,Join,Transformation,Threshold,Filter,JDBC ReaderOptions configs


```json
 {
  "source_catalog": "source_catalog",
  "source_schema": "source_schema",
  "target_catalog": "target_catalog",
  "target_schema": "target_schema",
  "tables": [
    {
      "source_name": "product_prod",
      "target_name": "product",
      "jdbc_reader_options": {
        "number_partitions": 10,
        "partition_column": "p_id",
        "lower_bound": "0",
        "upper_bound": "10000000"
      },
      "join_columns": [
        "p_id"
      ],
      "drop_columns": [
        "comment"
      ],
      "column_mapping": [
        {
          "source_name": "p_id",
          "target_name": "product_id"
        },
        {
          "source_name": "p_name",
          "target_name": "product_name"
        }
      ],
      "transformations": [
        {
          "column_name": "creation_date",
          "source": "creation_date",
          "target": "to_date(creation_date,'yyyy-mm-dd')"
        }
      ],
      "threshold": [
        {
          "column_name": "price",
          "upper_bound": "-50",
          "lower_bound": "50",
          "type": "float"
        }
      ],
      "filters": {
        "source": "p_id > 0",
        "target": "product_id > 0"
      }
    }
  ]
}

```