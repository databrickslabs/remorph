from pathlib import Path
from unittest.mock import patch

import pytest

from databricks.labs.remorph.assessments.profiler import Profiler


def test_supported_source_technologies():
    """Test that supported source technologies are correctly returned"""
    profiler = Profiler()
    supported_platforms = profiler.supported_source_technologies()
    assert isinstance(supported_platforms, list)
    assert "Synapse" in supported_platforms


def test_profile_unsupported_platform():
    """Test that profiling an unsupported platform raises ValueError"""
    profiler = Profiler()
    with pytest.raises(ValueError, match="Unsupported platform: InvalidPlatform"):
        profiler.profile("InvalidPlatform")


@patch(
    'databricks.labs.remorph.assessments.profiler._PLATFORM_TO_SOURCE_TECHNOLOGY',
    {"Synapse": "tests/resources/assessments/pipeline_config_main.yml"},
)
@patch('databricks.labs.remorph.assessments.profiler.PRODUCT_PATH_PREFIX', Path(__file__).parent / "../../../")
def test_profile_execution():
    """Test successful profiling execution using actual pipeline configuration"""
    profiler = Profiler()
    profiler.profile("Synapse")
    assert Path("/tmp/profiler_main/profiler_extract.db").exists(), "Profiler extract database should be created"


@patch(
    'databricks.labs.remorph.assessments.profiler._PLATFORM_TO_SOURCE_TECHNOLOGY',
    {"Synapse": "tests/resources/assessments/synapse/pipeline_config_main.yml"},
)
def test_profile_execution_with_invalid_config():
    """Test profiling execution with invalid configuration"""
    with patch('pathlib.Path.exists', return_value=False):
        profiler = Profiler()
        with pytest.raises(FileNotFoundError):
            profiler.profile("Synapse")
