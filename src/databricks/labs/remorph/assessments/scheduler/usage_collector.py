import logging

from databricks.labs.remorph.assessments.pipeline import PipelineClass


class UsageCollector():

    def __init__(self, warehouse_type: str):
        self.collection_type = warehouse_type

    def _validate_time_gap(self):
        """Backfills usage information if a gap in usage history is detected.
        History gaps could be due to system errors like outages or other system errors"""
        pass

    def run(self) -> str:
        status = "COMPLETE"
        pipeline_config = None
        extractor = None
        pipeline = PipelineClass(config=pipeline_config, executor=extractor)
        return status


def main():
    """Executes a PipelineClass that collects usage information from a target data warehouse."""
    try:
        logging.info("Starting usage collection.")
        UsageCollector.run()
        logging.info("Usage collection completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred during usage collection: {e}")


if __name__ == "__main__":
    main()
