import logging
import pytest

from databricks.labs.remorph.__about__ import __version__


logging.getLogger("tests").setLevel("DEBUG")
logging.getLogger("databricks.labs.remorph").setLevel("DEBUG")

logger = logging.getLogger(__name__)


@pytest.fixture
def debug_env_name():
    return "ucws"


@pytest.fixture
def product_info():
    return "remorph", __version__
