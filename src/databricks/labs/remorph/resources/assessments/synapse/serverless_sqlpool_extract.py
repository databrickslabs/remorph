import json
import sys
import logging
from .common.functions import arguments_loader


def execute():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    arguments_loader(description="Synapse Synapse Serverless SQL Pool Extract Script")


    try:


        # This is the output format expected by the pipeline.py which orchestrates the execution of this script
        print(json.dumps({"status": "success", "message": "Data loaded successfully"}))

    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}), file=sys.stderr)
        sys.exit(1)





if __name__ == '__main__':
    execute()
