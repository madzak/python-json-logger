# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.7] - 2023-02-21
### Changed
- Fix inclusion of py.typed in pip packages - @sth
- Added pytest support with test file rename. Migrated to assertEqual

## [2.0.6] - 2023-02-14
### Changed
- Parameter `rename_fields` in merge_record_extra is now optional - @afallou

## [2.0.5] - 2023-02-12
### Added
- Allow reserved attrs to be renamed - @henkhogan
- Support added for Python 3.11
- Now verifying builds in Pypy 3.9 as well
- Type annotations are now in the package - @louis-jaris
### Changed
- Fix rename_fields for exc_info - @guilhermeferrari
- Cleaned up test file for PEP8 - @lopagela
- Cleaned up old Python 2 artifacts - @louis-jaris
- Dropped Python 3.5 support - @idomozes
- Moved type check via tox into 3.11 run only
- Added test run in Python3.6 (will keep for a little while longer, but it's EOL so upgrade)

## [2.0.4] - 2022-07-11
### Changed
- Fix too strict regex for percentage style logging - @aberres
- 

## [2.0.3] - 2022-07-08
### Added
- Add PEP 561 marker/basic mypy configuration. - @bringhurst
- Workaround logging.LogRecord.msg type of string. - @bringhurst
### Changed
- Changed a link archive of the reference page in case it's down. - @ahonnecke
- Removed unnecessary try-except around OrderedDict usage - @sozofaan
- Update documentation link to json module + use https - @deronnax
- Dropped 3.5 support. - @bringhurst

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


[2.0.7]: https://github.com/madzak/python-json-logger/compare/v2.0.6...v2.0.7
[2.0.6]: https://github.com/madzak/python-json-logger/compare/v2.0.5...v2.0.6
[2.0.5]: https://github.com/madzak/python-json-logger/compare/v2.0.4...v2.0.5
[2.0.4]: https://github.com/madzak/python-json-logger/compare/v2.0.3...v2.0.4
[2.0.3]: https://github.com/madzak/python-json-logger/compare/v2.0.2...v2.0.3
[2.0.2]: https://github.com/madzak/python-json-logger/compare/v2.0.1...v2.0.2
[2.0.1]: https://github.com/madzak/python-json-logger/compare/v2.0.0...v2.0.1
[2.0.0]: https://github.com/madzak/python-json-logger/compare/v0.1.11...v2.0.0
[0.1.11]: https://github.com/madzak/python-json-logger/compare/v0.1.10...v0.1.11
