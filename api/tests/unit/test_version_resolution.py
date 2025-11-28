"""
Tests for resolving the application version.
"""

from importlib.metadata import PackageNotFoundError
from pathlib import Path

import pytest
from src.core import config


def test_resolve_app_version_reads_pyproject_when_package_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('[project]\nversion = "1.2.3"\n', encoding="utf-8")

    def _raise_package_not_found(_: str) -> str:
        raise PackageNotFoundError("package not installed")

    monkeypatch.setattr(config, "version", _raise_package_not_found)

    assert config._resolve_app_version(pyproject_path=pyproject) == "1.2.3"


def test_resolve_app_version_handles_missing_pyproject(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def _raise_package_not_found(_: str) -> str:
        raise PackageNotFoundError("package not installed")

    monkeypatch.setattr(config, "version", _raise_package_not_found)

    assert config._resolve_app_version(pyproject_path=tmp_path / "pyproject.toml") == "0.0.0"


@pytest.mark.parametrize(
    ("file_content", "expected_version"),
    [
        ('[project]\nversion = "1.2.3"', "1.2.3"),
        ('[project]\nname = "test-project"', "0.0.0"),
        ('version = "1.2.3"', "0.0.0"),
        ('[project]\nversion = 123', "0.0.0"),
        ("this is not valid toml", "0.0.0"),
        ("", "0.0.0"),
    ],
)
def test_load_pyproject_version_edge_cases(tmp_path: Path, file_content: str, expected_version: str) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(file_content, encoding="utf-8")

    assert config._load_pyproject_version(pyproject) == expected_version
