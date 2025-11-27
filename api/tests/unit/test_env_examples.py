from pathlib import Path
from typing import Dict, Set

import pytest


def find_repo_root() -> Path:
    """Locate repository root using common markers to avoid fragile relative paths."""
    current = Path(__file__).resolve()
    for candidate in [current] + list(current.parents):
        if (candidate / ".git").exists() or (candidate / "AGENTS.md").exists():
            return candidate
    raise RuntimeError("Repository root not found")


REPO_ROOT = find_repo_root()
API_ENV_PATH = REPO_ROOT / "api" / ".env.example"
WEB_ENV_PATH = REPO_ROOT / "web" / ".env.example"

API_REQUIRED_KEYS: Set[str] = {"DATABASE_URL", "REDIS_URL"}
WEB_REQUIRED_KEYS: Set[str] = {"NEXT_PUBLIC_API_URL"}


def parse_env_file(path: Path) -> Dict[str, str]:
    env: Dict[str, str] = {}
    for index, raw_line in enumerate(path.read_text().splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(f"{path}: line {index} must contain '='")
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise ValueError(f"{path}: line {index} has empty key")
        if key in env:
            raise ValueError(f"{path}: duplicate key '{key}'")
        env[key] = value
    return env


@pytest.mark.parametrize(
    ("env_path", "required_keys", "name"),
    [
        (API_ENV_PATH, API_REQUIRED_KEYS, "api"),
        (WEB_ENV_PATH, WEB_REQUIRED_KEYS, "web"),
    ],
)
def test_env_example_has_required_keys(env_path: Path, required_keys: Set[str], name: str) -> None:
    env = parse_env_file(env_path)

    missing = required_keys - set(env)
    assert not missing, f"{name}/.env.example is missing required keys: {sorted(missing)}"

    empty_required = [key for key in required_keys if not env.get(key)]
    assert not empty_required, f"{name}/.env.example required keys need placeholder values: {sorted(empty_required)}"
