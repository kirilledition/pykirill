# 🛠️ Development

## 🔄 Workflow

This is current development workflow to ensure code quality. In future should be automated with make, tox or nox

```bash
pip install ".[development]"
ruff format --check
ruff format
ruff check
mypy source
pytest .
python -m build --wheel
```

## 🗓️ Versioning

`pykirill` uses a custom versioning scheme designed to provide clear and immediate context about the release timeline and the nature of changes included in each release. My versioning scheme follows the format `YYYY.MINOR.PATCH`, where:

- `YYYY` is the current year, indicating the year of the release.
- `MINOR` is the minor version number, incremented for new features and significant changes.
- `PATCH` is the patch version number, incremented for small changes and bug fixes.

### Versioning Rules

**Major Version (`YYYY`):**
The major version corresponds to the current calendar year. This allows users to quickly see when the latest features and improvements were introduced. The major version will change at the beginning of each new year.

**Minor Version:**
The minor version is incremented when:

- New functionality is introduced, enhancing the capabilities of `pykirill`.
- A deprecated option or feature is removed, ensuring the codebase remains clean and up-to-date.

**Patch Version:**
The patch version is incremented for:

- Bug fixes, including behavior changes that resolve issues.
- Small changes that do not introduce new functionality but improve stability or performance.

## 🚀 Releasing

Change version in pyproject.toml
Change version in documentation installation section

```bash
git tag YYYY.MINOR.PATCH
git push origin YYYY.MINOR.PATCH
```