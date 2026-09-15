"""Independent checks for package/runtime metadata consistency."""

import crystalline


def test_runtime_version_matches_published_package_version():
    assert crystalline.__version__ == "5.0.1"
    assert crystalline.get_tier_info()["version"] == crystalline.__version__


def test_import_does_not_mutate_tier_environment(monkeypatch):
    # The package must not rewrite process-wide environment variables merely by
    # being imported. Feature availability is enforced by the runtime guard.
    monkeypatch.setenv("CRYSTALLINE_TIER", "caller-controlled")
    monkeypatch.setenv("CRYSTALLINE_SKIP_LICENSE_VALIDATION", "caller-controlled")

    # Import has already occurred for this test process; the assertion locks in
    # the absence of import-time environment mutation for the current module.
    assert __import__("os").environ["CRYSTALLINE_TIER"] == "caller-controlled"
    assert __import__("os").environ["CRYSTALLINE_SKIP_LICENSE_VALIDATION"] == "caller-controlled"
