# Reconcile Config

Consider the below tables that we want to reconcile:

| category | catalog        | schema        | table_name   | schema                                                                                                                                          | primary_key |
|----------|----------------|---------------|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
| source   | source_catalog | source_schema | product_prod | p_id INT,<br>p_name STRING,<br>price NUMBER,<br>discount DECIMAL(5,3),<br>offer DOUBLE,<br>creation_date DATE<br>comment STRING<br>             | p_id        |
| target   | target_catalog | target_schema | product      | product_id INT,<br>product_name STRING,<br>price NUMBER,<br>discount DECIMAL(5,3),<br>offer DOUBLE,<br>creation_date DATE<br>comment STRING<br> | product_id  |

## Run with Drop,Join,Transformation,ColumnThresholds,Filter,JDBC ReaderOptions configs


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
      "column_thresholds": [
        {
          "column_name": "price",
          "upper_bound": "-50",
          "lower_bound": "50",
          "type": "float"
        }
      ],
      "table_thresholds": [
        {
          "lower_bound": "0%",
          "upper_bound": "5%",
          "model": "mismatch"
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

---

## Aggregates Reconcile Config

### Aggregates-Reconcile run with Join, Column Mappings, Transformation, Filter and JDBC ReaderOptions configs

> **Note:** Even though the user provides the `select_columns` and `drop_columns`, those are not considered.


```json
 {
  "source_catalog": "source_catalog",
  "source_schema": "source_schema",
  "target_catalog": "target_catalog",
  "target_schema": "target_schema",
  "tables": [
    {
      "aggregates": [{
        "type": "MIN",
        "agg_columns": ["discount"],
        "group_by_columns": ["p_id"]
      },
        {
          "type": "AVG",
          "agg_columns": ["discount"],
          "group_by_columns": ["p_id"]
        },
        {
          "type": "MAX",
          "agg_columns": ["p_id"],
          "group_by_columns": ["creation_date"]
        },
        {
          "type": "MAX",
          "agg_columns": ["p_name"]
        },
        {
          "type": "SUM",
          "agg_columns": ["p_id"]
        },
        {
          "type": "MAX",
          "agg_columns": ["creation_date"]
        },
        {
          "type": "MAX",
          "agg_columns": ["p_id"],
          "group_by_columns": ["creation_date"]
        }
      ],
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
      "column_thresholds": [
        {
          "column_name": "price",
          "upper_bound": "-50",
          "lower_bound": "50",
          "type": "float"
        }
      ],
      "table_thresholds": [
        {
          "lower_bound": "0%",
          "upper_bound": "5%",
          "model": "mismatch"
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
