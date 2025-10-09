"""Contract tests for mypy static type checking integration.

These tests verify that mypy is properly configured and functioning.
All tests follow TDD principles - they define the contract before implementation.
"""

import re
import subprocess
import tomllib
from pathlib import Path


def test_mypy_installed() -> None:
    """Contract: mypy is installed and accessible via uv."""
    result = subprocess.run(
        ["uv", "run", "mypy", "--version"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )

    assert result.returncode == 0, f"mypy not accessible: {result.stderr}"
    assert "mypy" in result.stdout.lower(), f"Unexpected output: {result.stdout}"

    # Extract version and verify >= 1.8.0
    # Output format: "mypy 1.18.2 (compiled: yes)"
    version_match = re.search(r"mypy (\d+\.\d+\.\d+)", result.stdout)
    assert version_match, f"Could not extract version from: {result.stdout}"

    version_str = version_match.group(1)
    major, minor = map(int, version_str.split(".")[:2])
    assert (major, minor) >= (1, 8), f"mypy version {version_str} < 1.8.0"


def test_mypy_config_exists() -> None:
    """Contract: mypy configuration section exists in pyproject.toml."""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"

    with open(pyproject_path, "rb") as f:
        config = tomllib.load(f)

    assert "tool" in config, "No [tool] section in pyproject.toml"
    assert "mypy" in config["tool"], "No [tool.mypy] section in pyproject.toml"

    mypy_config = config["tool"]["mypy"]

    # Verify required fields
    required_fields = ["strict", "plugins", "python_version", "mypy_path", "files"]
    for field in required_fields:
        assert field in mypy_config, f"Missing required field: {field}"


def test_strict_mode_enabled() -> None:
    """Contract: mypy strict mode is enabled."""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"

    with open(pyproject_path, "rb") as f:
        config = tomllib.load(f)

    mypy_config = config["tool"]["mypy"]
    assert mypy_config.get("strict") is True, "strict mode not enabled"


def test_pydantic_plugin_configured() -> None:
    """Contract: Pydantic mypy plugin is configured."""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"

    with open(pyproject_path, "rb") as f:
        config = tomllib.load(f)

    mypy_config = config["tool"]["mypy"]
    plugins = mypy_config.get("plugins", [])

    assert isinstance(plugins, list), "plugins must be a list"
    assert "pydantic.mypy" in plugins, "pydantic.mypy plugin not configured"


def test_migrations_excluded() -> None:
    """Contract: migrations directory is excluded from type checking."""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"

    with open(pyproject_path, "rb") as f:
        config = tomllib.load(f)

    # Check for overrides section
    assert "tool" in config
    assert "mypy" in config["tool"]

    # mypy.overrides is a list of override sections
    overrides = config["tool"]["mypy"].get("overrides", [])

    # Find migrations override
    migrations_override = None
    for override in overrides:
        if override.get("module") == "migrations.*":
            migrations_override = override
            break

    assert migrations_override is not None, "No override for migrations.* module"
    assert migrations_override.get("ignore_errors") is True, "migrations errors not ignored"


def test_mypy_runs_successfully() -> None:
    """Contract: mypy executes without configuration errors.

    Exit codes:
    - 0: Success, no errors
    - 1: Type errors found (expected initially)
    - 2: Configuration error (NOT acceptable)
    """
    result = subprocess.run(
        ["uv", "run", "mypy", "."],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )

    # Exit code 0 or 1 is acceptable (0 = no errors, 1 = type errors)
    # Exit code 2 means configuration error - NOT acceptable
    assert result.returncode in [0, 1], f"mypy configuration error (exit {result.returncode}): {result.stderr}"


def test_mypy_cache_created() -> None:
    """Contract: mypy creates cache directory on execution."""
    cache_dir = Path(__file__).parent.parent / ".mypy_cache"

    # Clean cache if exists
    if cache_dir.exists():
        import shutil

        shutil.rmtree(cache_dir)

    # Run mypy
    subprocess.run(
        ["uv", "run", "mypy", "."],
        capture_output=True,
        cwd=Path(__file__).parent.parent,
    )

    # Verify cache created
    assert cache_dir.exists(), ".mypy_cache directory not created"
    assert cache_dir.is_dir(), ".mypy_cache is not a directory"

    # Verify Python version subdirectory exists
    python_subdir = cache_dir / "3.12"
    assert python_subdir.exists(), "Python 3.12 cache subdirectory not created"


def test_type_error_detection() -> None:
    """Contract: mypy correctly detects type errors."""
    # Create temporary file with intentional type error
    temp_file = Path(__file__).parent.parent / "src" / "_test_temp_type_error.py"

    try:
        temp_file.write_text('def test_function() -> int:\n    return "this is a string, not an int"  # Type error\n')

        # Run mypy on the temp file
        result = subprocess.run(
            ["uv", "run", "mypy", "src/_test_temp_type_error.py"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )

        # Should exit with error code 1 (type errors found)
        assert result.returncode == 1, "mypy should detect type error"

        # Should contain return-value error code
        assert "return-value" in result.stdout, f"Expected 'return-value' error code in output: {result.stdout}"

    finally:
        # Clean up temp file
        if temp_file.exists():
            temp_file.unlink()
