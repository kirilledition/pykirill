from pathlib import Path


def read_version():
    try:
        import tomllib
    except ImportError:
        return "0.0.0"
    pyproject_path = Path(__file__).resolve().parents[1] / "pyproject.toml"
    with pyproject_path.open("rb") as file:
        pyproject_data = tomllib.load(file)
    return pyproject_data["project"]["version"]


VERSION = read_version()
