"""Smoke tests: the package imports and its version metadata is consistent."""

from importlib.metadata import version
from importlib.resources import files

from packaging.version import Version

import dedpath


def test_import_exposes_version_string() -> None:
    assert isinstance(dedpath.__version__, str)
    assert dedpath.__version__


def test_version_is_pep440() -> None:
    # Raises InvalidVersion if the string is not a valid PEP 440 version.
    Version(dedpath.__version__)


def test_installed_metadata_matches_source_version() -> None:
    # Fails if the package is not installed (e.g. imported from a stray path)
    # or if the build backend read a different version than the source file.
    assert version("dedpath") == dedpath.__version__


def test_package_is_typed() -> None:
    # PEP 561 marker: lets downstream mypy users type-check against dedpath.
    assert files("dedpath").joinpath("py.typed").is_file()


def test_generic_dialect_profile_is_a_package_resource() -> None:
    # The profile must be reachable through importlib.resources (not a path
    # relative to the repo), otherwise it would break once installed from a wheel.
    profile = files("dedpath").joinpath("dialects", "profiles", "sinumerik_generic.yaml")
    assert profile.is_file()
    assert "name: sinumerik_generic" in profile.read_text(encoding="utf-8")
