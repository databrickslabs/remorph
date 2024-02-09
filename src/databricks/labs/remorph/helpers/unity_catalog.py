from databricks.labs.blueprint.entrypoint import get_logger
from databricks.sdk import WorkspaceClient 

logger = get_logger(__file__)

def create_test_catalog_and_schema(client: WorkspaceClient, catalog_name=None, schema_name=None):  
        if catalog_name in (None, 'transpiler_test') and schema_name in (None, 'convertor_test'): 
            logger.debug("Creating catalog and schema for Remorph")
            try: 
                client.catalogs.create(name='transpiler_test', comment='Catalog created by Remorph for query validation')

            ## TODO there has to be a smarter way to test if a Catalog exists
            ## my thought is if we `list` the catalogs that is a big operation for
            ## large worksapces 
            except: 
                logger.info("Catalog already exists")
            try: 
                client.schema.create(name='convertor_test', catalog_name='transpiler_teste', comment='Schema created by Remorph for query validation')
            except: 
                logger.info("Schema already exists") 