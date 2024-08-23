# 🛠️ Development

## 🔄 Workflow

This is current development workflow to ensure code quality. In future should be automated with make, tox or nox

```bash
pip install -e ".[documentation,development]"
ruff format --check
ruff format
ruff check
mypy source
pytest .
python -m build --wheel
```

Certainly! Here’s the updated version of your documentation, incorporating the feature versioning part:

---

## 🗓️ Versioning

`pykirill` uses a custom versioning scheme designed to provide clear and immediate context about the release timeline and the nature of changes included in each release. The versioning scheme follows the format `YYYY.MINOR.PATCH`, where:

- **`YYYY`**: The current year, indicating the year of the release.
- **`MINOR`**: The minor version number, incremented for new features and significant changes.
- **`PATCH`**: The patch version number, incremented for small changes and bug fixes.

### Feature Branch Versioning

When developing new features, a separate feature branch is created. The version of the Python package in this feature branch is based on the current master version, with an additional feature identifier appended. The version format in a feature branch is `YYYY.MINOR.PATCH+FEATURE`.

For example, if the current version on the master branch is `2024.1.0` and you are working on a feature for Principal Component Analysis (PCA), the version in the feature branch would be `2024.1.0+pca`.

This versioning approach allows you to distinguish between different package versions during development and testing, ensuring clarity and traceability as features are developed and integrated.


## 🚀 Releasing

Change version in pyproject.toml
Change version in documentation installation section

```bash
git tag YYYY.MINOR.PATCH
git push origin YYYY.MINOR.PATCH
```