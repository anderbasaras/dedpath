# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Project scaffolding: `src/` layout built with hatchling, managed with uv.
- Tooling: ruff (lint + format), mypy (strict), pytest + Hypothesis + pytest-cov,
  pre-commit hooks (including a local confidential-terms guard).
- GitHub Actions CI on Ubuntu and Windows with Python 3.12 and 3.13, plus a
  build job that checks the wheel contents.
- Placeholder generic SINUMERIK 840D dialect profile shipped inside the package.
- Project documentation: v1 scope (`docs/scope.md`), references and dev-log template.
