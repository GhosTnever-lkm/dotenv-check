# Changelog

All notable changes to this project are documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [0.1.2] - 2026-10-13

### Added

- Ignore keys consistently in both the template and local environment.
- Add safe parsing for inline comments and explicit errors for malformed quoted values and invalid UTF-8 input.
- Make JSON `failed` agree with the exit code when `--strict` promotes warnings.
- Add CLI version regression coverage, install guidance, badges, and tagged wheel/sdist releases with SHA-256 checksums.

### Fixed

- Correctly report strict-mode placeholder warnings as failures in machine-readable output.
- Prevent ignored local-only keys from being reported as extras.

## [0.1.1] - 2026-10-11

### Added

- CI now also runs the test suite on Windows (windows-latest), not only Ubuntu.
- `--ignore KEY` (repeatable) to skip template keys that are only needed in CI.

## [0.1.0] - 2026-10-11

### Added

- Compare `.env` with `.env.example`: missing, empty, placeholder and extra keys.
- Values are never printed, including in JSON output.
- `--strict` and `--json` modes; exit code 2 for unreadable or malformed files.

[Unreleased]: https://github.com/GhosTnever-lkm/dotenv-check/compare/v0.1.2...HEAD
[0.1.2]: https://github.com/GhosTnever-lkm/dotenv-check/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/GhosTnever-lkm/dotenv-check/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/GhosTnever-lkm/dotenv-check/releases/tag/v0.1.0
