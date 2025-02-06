from databricks.labs.blueprint.entrypoint import get_logger, is_in_debug

if __name__ == "__main__":
    logger = get_logger(__file__)
    logger.setLevel("INFO")
    if is_in_debug():
        logger.getLogger("databricks").setLevel(logger.setLevel("DEBUG"))

    logger.info("Successfully Setup Remorph Components Locally")
