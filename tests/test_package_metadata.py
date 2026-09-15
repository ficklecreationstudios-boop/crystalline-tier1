"""Independent checks for package/runtime metadata consistency."""

import importlib.metadata
import os
import subprocess
import sys

import crystalline


def test_runtime_version_matches_published_package_version():
    assert crystalline.__version__ == "5.0.1"
    assert crystalline.get_tier_info()["version"] == crystalline.__version__


def test_distribution_metadata_declares_spdx_license_expression():
    metadata = importlib.metadata.metadata("crystalline-tier1")
    assert metadata["Version"] == crystalline.__version__
    assert metadata["License-Expression"] == "GPL-3.0-only"


def test_import_does_not_mutate_tier_environment():
    env = os.environ.copy()
    env["CRYSTALLINE_TIER"] = "caller-controlled"
    env["CRYSTALLINE_SKIP_LICENSE_VALIDATION"] = "caller-controlled"

    code = (
        "import os, crystalline; "
        "assert os.environ['CRYSTALLINE_TIER'] == 'caller-controlled'; "
        "assert os.environ['CRYSTALLINE_SKIP_LICENSE_VALIDATION'] == 'caller-controlled'"
    )
    result = subprocess.run(
        [sys.executable, "-c", code],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
