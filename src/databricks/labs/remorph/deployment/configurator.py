import logging
import time

from databricks.sdk.service.catalog import Privilege
from databricks.sdk.service.sql import (
    CreateWarehouseRequestWarehouseType,
    EndpointInfoWarehouseType,
    SpotInstancePolicy,
)


from databricks.labs.remorph.contexts.application import CliContext

logger = logging.getLogger(__name__)


class ResourceConfigurator:
    """
    Handles the setup of common Databricks resources like
    catalogs, schemas, volumes, and warehouses used across remorph modules.
    """

    def __init__(self, context: CliContext):
        self._context = context

    def prompt_for_catalog_setup(
        self,
        required_privileges: tuple[set[Privilege], ...] = (
            {Privilege.ALL_PRIVILEGES},
            {Privilege.USE_CATALOG},
        ),
        max_attempts: int = 3,
    ) -> str:
        for _ in range(1, max_attempts + 1):
            catalog_name = self._context.prompts.question("Enter catalog name", default="remorph")
            catalog = self._context.catalog_operations.get_catalog(catalog_name)
            if catalog:
                logger.info(f"Found existing catalog `{catalog_name}`")
                user_name = self._context.current_user.user_name
                assert user_name is not None
                if self._context.catalog_operations.has_catalog_access(catalog, user_name, required_privileges):
                    return catalog_name
                logger.info(f"User `{user_name}` doesn't have privilege to use catalog `{catalog_name}`")
                if not self._context.prompts.confirm("Do you want to use another catalog?"):
                    raise SystemExit("Aborting the installation.")
            else:
                if self._context.prompts.confirm(f"Catalog `{catalog_name}` doesn't exist. Create it?"):
                    result = self._context.catalog_operations.create_catalog(catalog_name)
                    assert result.name is not None
                    return result.name
                raise SystemExit("Aborting the installation.")
        raise SystemExit(f"Couldn't get answer within {max_attempts} attempts. Aborting the installation.")

    def prompt_for_schema_setup(
        self,
        catalog: str,
        default_schema_name: str,
        required_privileges: tuple[set[Privilege], ...] = (
            {Privilege.ALL_PRIVILEGES},
            {Privilege.USE_SCHEMA},
        ),
        max_attempts: int = 3,
    ) -> str:
        for _ in range(1, max_attempts + 1):
            schema_name = self._context.prompts.question("Enter schema name", default=default_schema_name)
            schema = self._context.catalog_operations.get_schema(catalog, schema_name)
            if schema:
                logger.info(f"Found existing schema `{schema_name}` in catalog `{catalog}`")
                user_name = self._context.current_user.user_name
                assert user_name is not None
                if self._context.catalog_operations.has_schema_access(schema, user_name, required_privileges):
                    return schema_name
                logger.info(
                    f"User `{user_name}` doesn't have privilege to use schema `{schema_name}` in catalog `{catalog}`"
                )
                if not self._context.prompts.confirm("Do you want to use another schema?"):
                    raise SystemExit("Aborting the installation.")
            else:
                if self._context.prompts.confirm(
                    f"Schema `{schema_name}` doesn't exist in catalog `{catalog}`. Create it?"
                ):
                    result = self._context.catalog_operations.create_schema(schema_name, catalog)
                    assert result.name is not None
                    return result.name
                raise SystemExit("Aborting the installation.")
        raise SystemExit(f"Couldn't get answer within {max_attempts} attempts. Aborting the installation.")

    def prompt_for_volume_setup(
        self,
        catalog: str,
        schema: str,
        default_volume_name: str,
        required_privileges: tuple[set[Privilege], ...] = (
            {Privilege.ALL_PRIVILEGES},
            {Privilege.READ_VOLUME, Privilege.WRITE_VOLUME},
        ),
        max_attempts: int = 3,
    ) -> str:
        for _ in range(1, max_attempts + 1):
            volume_name = self._context.prompts.question("Enter volume name", default=default_volume_name)
            volume = self._context.catalog_operations.get_volume(catalog, schema, volume_name)
            if volume:
                logger.info(f"Found existing volume `{volume_name}` in catalog `{catalog}` and schema `{schema}`")
                user_name = self._context.current_user.user_name
                assert user_name is not None
                if self._context.catalog_operations.has_volume_access(volume, user_name, required_privileges):
                    return volume_name
                logger.info(
                    f"User `{user_name}` doesn't have privilege to use volume `{volume_name}` "
                    f"in catalog `{catalog}` and schema `{schema}`"
                )
                if not self._context.prompts.confirm("Do you want to use another volume?"):
                    raise SystemExit("Aborting the installation.")
            else:
                if self._context.prompts.confirm(
                    f"Volume `{volume_name}` doesn't exist in catalog `{catalog}` and schema `{schema}`. Create it?"
                ):
                    result = self._context.catalog_operations.create_volume(catalog, schema, volume_name)
                    assert result.name is not None
                    return result.name
                raise SystemExit("Aborting the installation.")
        raise SystemExit(f"Couldn't get answer within {max_attempts} attempts. Aborting the installation.")

    def prompt_for_warehouse_setup(self, warehouse_name_prefix: str) -> str:
        def warehouse_type(_):
            return _.warehouse_type.value if not _.enable_serverless_compute else "SERVERLESS"

        pro_warehouses = {"[Create new PRO SQL warehouse]": "create_new"} | {
            f"{_.name} ({_.id}, {warehouse_type(_)}, {_.state.value})": _.id
            for _ in self._context.workspace_client.warehouses.list()
            if _.warehouse_type == EndpointInfoWarehouseType.PRO
        }
        warehouse_id = self._context.prompts.choice_from_dict(
            "Select PRO or SERVERLESS SQL warehouse",
            pro_warehouses,
        )
        if warehouse_id == "create_new":
            new_warehouse = self._context.workspace_client.warehouses.create(
                name=f"{warehouse_name_prefix} {time.time_ns()}",
                spot_instance_policy=SpotInstancePolicy.COST_OPTIMIZED,
                warehouse_type=CreateWarehouseRequestWarehouseType.PRO,
                cluster_size="Small",
                max_num_clusters=1,
            )
            warehouse_id = new_warehouse.id
        return warehouse_id
