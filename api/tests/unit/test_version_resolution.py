"""
Tests for resolving the application version.
"""

from importlib.metadata import PackageNotFoundError
from pathlib import Path

import pytest
from src.core import version as version_module


def test_resolve_app_version_reads_pyproject_when_package_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('[project]\nversion = "1.2.3"\n', encoding="utf-8")

    def _raise_package_not_found(_: str) -> str:
        raise PackageNotFoundError("package not installed")

    monkeypatch.setattr(version_module, "version", _raise_package_not_found)

    assert version_module._resolve_app_version(pyproject_path=pyproject) == "1.2.3"


def test_resolve_app_version_handles_missing_pyproject(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def _raise_package_not_found(_: str) -> str:
        raise PackageNotFoundError("package not installed")

    monkeypatch.setattr(version_module, "version", _raise_package_not_found)

    assert version_module._resolve_app_version(pyproject_path=tmp_path / "pyproject.toml") == "0.0.0"


def test_resolve_app_version_discovers_pyproject(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    project_root = tmp_path / "project"
    src_dir = project_root / "src" / "core"
    src_dir.mkdir(parents=True)
    (project_root / "pyproject.toml").write_text('[project]\nversion = "4.5.6"\n', encoding="utf-8")

    def _raise_package_not_found(_: str) -> str:
        raise PackageNotFoundError("package not installed")

    monkeypatch.setattr(version_module, "version", _raise_package_not_found)
    monkeypatch.setattr(version_module, "__file__", str(src_dir / "version.py"))

    assert version_module._resolve_app_version() == "4.5.6"


@pytest.mark.parametrize(
    ("file_content", "expected_version"),
    [
        ('[project]\nversion = "1.2.3"', "1.2.3"),
        ('[project]\nname = "test-project"', "0.0.0"),
        ('version = "1.2.3"', "0.0.0"),
        ("[project]\nversion = 123", "0.0.0"),
        ("this is not valid toml", "0.0.0"),
        ("", "0.0.0"),
    ],
)
def test_load_pyproject_version_edge_cases(tmp_path: Path, file_content: str, expected_version: str) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(file_content, encoding="utf-8")

    assert version_module._load_pyproject_version(pyproject) == expected_version


def test_find_pyproject_root_returns_closest_parent(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    nested_dir = project_root / "src" / "core"
    nested_dir.mkdir(parents=True)
    (project_root / "pyproject.toml").write_text("", encoding="utf-8")

    assert version_module.find_pyproject_root(nested_dir) == project_root


def test_find_pyproject_root_handles_missing_marker(tmp_path: Path) -> None:
    search_root = tmp_path / "no-project"
    search_root.mkdir()

    assert version_module.find_pyproject_root(search_root) is None
