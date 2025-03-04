import pandas as pd
import duckdb
import argparse
import json
import sys
import yaml
import numpy as np
from datetime import datetime, timedelta


def generate_random_dataset(size=10):
    # Generate dates for the last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    dates = pd.date_range(start=start_date, end=end_date, periods=size)

    data = {
        'id': range(1, size + 1),
        'date': dates,
        'category': np.random.choice(['Low', 'Medium', 'High'], size),
        'department': np.random.choice(['Sales', 'Marketing', 'Engineering', 'Support'], size),
        'is_active': np.random.choice([True, False], size, p=[0.8, 0.2]),
        'score': np.random.uniform(0, 100, size).round(2),
    }

    return pd.DataFrame(data)


def main():

    parser = argparse.ArgumentParser(description='Generate and store random dataset in DuckDB')
    parser.add_argument('--db-path', type=str, required=True, help='Path to DuckDB database file')
    parser.add_argument(
        '--credential-config-path', type=str, required=True, help='Path string containing credential configuration'
    )
    args = parser.parse_args()

    try:
        with open(args.credential_config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
            assert config
    except (yaml.YAMLError, FileNotFoundError) as e:
        print(json.dumps({"status": "error", "message": f"Error reading config: {e}"}), file=sys.stderr)
        sys.exit(1)

    try:
        df = generate_random_dataset()
        print(df.columns, file=sys.stderr)
        # Connect to DuckDB
        conn = duckdb.connect(args.db_path)

        # Create table with appropriate schema
        conn.execute(
            """
            CREATE OR REPLACE TABLE random_data (
                id INTEGER,
                date TIMESTAMP,
                category VARCHAR,
                department VARCHAR,
                is_active BOOLEAN,
                score DOUBLE
            )
        """
        )

        conn.execute("INSERT INTO random_data SELECT * FROM df")
        conn.close()

        print(json.dumps({"status": "success", "message": "Data loaded successfully"}))

    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
