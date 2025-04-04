import logging

from databricks.labs.remorph.assessments.pipeline import PipelineClass


class UsageCollector:
    """Executes a PipelineClass that collects usage information from a target data warehouse."""

    def __init__(self, warehouse_type: str, pipeline: PipelineClass):
        self.collection_type = warehouse_type
        self.pipeline = pipeline

    def run(self) -> str:
        try:
            logging.info("Executing pipeline.")
            self.pipeline.execute()
            status = "COMPLETE"
        except Exception as e:
            logging.error(f"Usage collection failed: {str(e)}")
            raise RuntimeError(f"Usage collection failed: {str(e)}") from e
        return status
