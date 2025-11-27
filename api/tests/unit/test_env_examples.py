from pathlib import Path

API_ENV_PATH = Path(__file__).resolve().parents[2] / ".env.example"
WEB_ENV_PATH = Path(__file__).resolve().parents[3] / "web" / ".env.example"

API_REQUIRED_KEYS = {"DATABASE_URL", "REDIS_URL"}
WEB_REQUIRED_KEYS = {"NEXT_PUBLIC_API_URL"}


def parse_env_file(path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    for index, raw_line in enumerate(path.read_text().splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        assert "=" in line, f"{path}: line {index} must contain '='"
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        assert key, f"{path}: line {index} has empty key"
        assert key not in env, f"{path}: duplicate key '{key}'"
        env[key] = value
    return env


def test_api_env_example_has_required_keys() -> None:
    env = parse_env_file(API_ENV_PATH)

    missing = API_REQUIRED_KEYS - set(env)
    assert not missing, f"api/.env.example is missing required keys: {sorted(missing)}"

    empty_required = [key for key in API_REQUIRED_KEYS if not env.get(key)]
    assert not empty_required, f"api/.env.example required keys need placeholder values: {sorted(empty_required)}"


def test_web_env_example_has_required_keys() -> None:
    env = parse_env_file(WEB_ENV_PATH)

    missing = WEB_REQUIRED_KEYS - set(env)
    assert not missing, f"web/.env.example is missing required keys: {sorted(missing)}"

    empty_required = [key for key in WEB_REQUIRED_KEYS if not env.get(key)]
    assert not empty_required, f"web/.env.example required keys need placeholder values: {sorted(empty_required)}"
