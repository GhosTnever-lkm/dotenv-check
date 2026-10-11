# Changelog

All notable changes to this project are documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- `--ignore KEY` (repeatable) to skip template keys that are only needed in CI.

## [0.1.1] - 2026-10-11

### Added

- CI now also runs the test suite on Windows (windows-latest), not only Ubuntu.


## [0.1.0] - 2026-10-11

### Added

- Compare `.env` with `.env.example`: missing, empty, placeholder and extra keys.
- Values are never printed, including in JSON output.
- `--strict` and `--json` modes; exit code 2 for unreadable or malformed files.

[Unreleased]: https://github.com/GhosTnever-lkm/dotenv-check/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/GhosTnever-lkm/dotenv-check/releases/tag/v0.1.0
