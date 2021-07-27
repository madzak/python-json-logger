# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.2] - 2021-07-27
### Added
- Officially supporting 3.9 - @felixonmars.
- You can now add static fields to log objects - @cosimomeli.
### Changed
- Dropped 3.4 support.
- Dropped Travis CI for Github Actions.
- Wheel should build for python 3 instead of just 3.4 now.

## [2.0.1] - 2020-10-12
### Added
- Support Pypi long descripton - @ereli-cb
### Changed
- You can now rename output fields - @schlitzered

## [2.0.0] - 2020-09-26
### Added
- New Changelog
- Added timezone support to timestamps - @lalten
- Refactored log record to function - @georgysavva
- Add python 3.8 support - @tommilligan
### Removed
- Support for Python 2.7
- Debian directory

## [0.1.11] - 2019-03-29
### Added
- Support for Python 3.7
### Changed
- 'stack_info' flag in logging calls is now respected in JsonFormatter by [@ghShu](https://github.com/ghShu)


[2.0.2]: https://github.com/madzak/python-json-logger/compare/v2.0.1...v2.0.2
[2.0.1]: https://github.com/madzak/python-json-logger/compare/v2.0.0...v2.0.1
[2.0.0]: https://github.com/madzak/python-json-logger/compare/v0.1.11...v2.0.0
[0.1.11]: https://github.com/madzak/python-json-logger/compare/v0.1.10...v0.1.11
