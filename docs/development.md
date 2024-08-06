# 🛠️ Development

## 🔄 Workflow

This is current development workflow to ensure code quality. In future should be automated with make, tox or nox

```bash
pip install .
ruff format --check
ruff format
ruff check
mypy src
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

### Versioning Scheme in Practice

For example, a version `2024.1.0` indicates:
- `2024`: The release was made in the year 2024.
- `1`: This is the first minor update of the year, introducing new features or removing deprecated features.
- `0`: There have been no patch updates for this minor version yet.

A subsequent bug fix would update the version to `2024.1.1`, indicating the first patch for the first minor release of 2024.


## 🚀 Releasing

Change version in pyproject.toml
Change version in documentation installation section

```bash
git tag YYYY.MINOR.PATCH
git push origin YYYY.MINOR.PATCH
```