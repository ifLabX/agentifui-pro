"""
Application version resolution helpers.
"""

import tomllib
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path


def find_pyproject_root(start_path: Path) -> Path | None:
    """
    Search upward from a starting path for a directory containing pyproject.toml.
    """
    current = start_path.resolve()

    for candidate in (current, *current.parents):
        pyproject = candidate / "pyproject.toml"
        if pyproject.is_file():
            return candidate

    return None


def _load_pyproject_version(pyproject_path: Path) -> str:
    """
    Read the version from pyproject.toml to keep development parity with the packaged build.
    """
    if not pyproject_path.is_file():
        return "0.0.0"

    try:
        with pyproject_path.open("rb") as pyproject_file:
            project = tomllib.load(pyproject_file)
    except (tomllib.TOMLDecodeError, OSError):
        return "0.0.0"

    project_version = project.get("project", {}).get("version")
    if isinstance(project_version, str):
        return project_version

    return "0.0.0"


def _resolve_app_version(pyproject_path: Path | None = None) -> str:
    """
    Prefer the installed package metadata, falling back to pyproject.toml when running from source.
    """
    try:
        return version("agentifui-pro-api")
    except PackageNotFoundError:
        if pyproject_path is not None:
            resolved_pyproject = pyproject_path
        else:
            start_path = Path(__file__).resolve().parent
            pyproject_root = find_pyproject_root(start_path)
            if not pyproject_root:
                return "0.0.0"
            resolved_pyproject = pyproject_root / "pyproject.toml"

    return _load_pyproject_version(resolved_pyproject)


__version__ = _resolve_app_version()
