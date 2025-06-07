from databricks.sdk.core import with_user_agent_extra, with_product
from databricks.labs.blueprint.logger import install_logger
from databricks.labs.remorph.__about__ import __version__

install_logger()

# Add remorph/<version> for projects depending on remorph as a library
with_user_agent_extra("remorph", __version__)

# Add remorph/<version> for re-packaging of remorph, where product name is omitted
with_product("remorph", __version__)
