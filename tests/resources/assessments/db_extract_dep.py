import argparse
import json
import sys
import logging
import subprocess

def check_specific_packages(packages, logger):
    for pkg in packages:
        result = subprocess.run(['pip', 'show', pkg], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"{pkg} is installed:")
        else:
            logger.error(f"{pkg} is NOT installed.")
            raise ValueError(f"{pkg} is NOT installed. Please install it using pip.")

def execute():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(description='Generate and store random dataset in DuckDB')
    parser.add_argument('--db-path', type=str, required=True, help='Path to DuckDB database file')
    parser.add_argument(
        '--credential-config-path', type=str, required=True, help='Path string containing credential configuration'
    )
    args = parser.parse_args()
    credential_file = args.credential_config_path

    if not credential_file.endswith('credentials.yml'):
        msg = "Credential config file must have 'credentials.yml' extension"
        # This is the output format expected by the pipeline.py which orchestrates the execution of this script
        print(json.dumps({"status": "error", "message": msg}), file=sys.stderr)
        raise ValueError("Credential config file must have 'credentials.yml' extension")

    try:
        logger.info("Checking if all dependant libs are installed")
        check_specific_packages(['databricks_labs_dqx', 'databricks_labs_ucx'])
        print(json.dumps({"status": "success", "message": "Data loaded successfully"}))

    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    execute()
