# lazy_loader 0.4

We're happy to announce the release of lazy_loader 0.4!

## Enhancements

- ENH: Add require argument to load() to accept version specifiers ([#48](https://github.com/scientific-python/lazy_loader/pull/48)).
- Add version as __version__ ([#97](https://github.com/scientific-python/lazy_loader/pull/97)).

## Bug Fixes

- Avoid exception when __frame_data["code_context"] is None ([#83](https://github.com/scientific-python/lazy_loader/pull/83)).
- Make `lazy_load.load` partially thread-safe ([#90](https://github.com/scientific-python/lazy_loader/pull/90)).

## Documentation

- Add security contact ([#91](https://github.com/scientific-python/lazy_loader/pull/91)).
- Recommend newer Python versions to avoid race ([#102](https://github.com/scientific-python/lazy_loader/pull/102)).

## Maintenance

- Use label-check and attach-next-milestone-action ([#64](https://github.com/scientific-python/lazy_loader/pull/64)).
- Use setuptools ([#65](https://github.com/scientific-python/lazy_loader/pull/65)).
- Specify what goes in sdist ([#66](https://github.com/scientific-python/lazy_loader/pull/66)).
- Use changelist ([#67](https://github.com/scientific-python/lazy_loader/pull/67)).
- Used dependabot ([#68](https://github.com/scientific-python/lazy_loader/pull/68)).
- Bump pre-commit from 3.3 to 3.3.3 ([#69](https://github.com/scientific-python/lazy_loader/pull/69)).
- Bump scientific-python/attach-next-milestone-action from f94a5235518d4d34911c41e19d780b8e79d42238 to a4889cfde7d2578c1bc7400480d93910d2dd34f6 ([#72](https://github.com/scientific-python/lazy_loader/pull/72)).
- Bump scientific-python/attach-next-milestone-action from a4889cfde7d2578c1bc7400480d93910d2dd34f6 to bc07be829f693829263e57d5e8489f4e57d3d420 ([#74](https://github.com/scientific-python/lazy_loader/pull/74)).
- Bump actions/checkout from 3 to 4 ([#75](https://github.com/scientific-python/lazy_loader/pull/75)).
- Bump changelist from 0.1 to 0.3 ([#77](https://github.com/scientific-python/lazy_loader/pull/77)).
- Bump pre-commit from 3.3.3 to 3.4.0 ([#76](https://github.com/scientific-python/lazy_loader/pull/76)).
- Use trusted publisher ([#78](https://github.com/scientific-python/lazy_loader/pull/78)).
- Bump pre-commit from 3.4.0 to 3.5.0 ([#80](https://github.com/scientific-python/lazy_loader/pull/80)).
- Bump changelist from 0.3 to 0.4 ([#81](https://github.com/scientific-python/lazy_loader/pull/81)).
- Bump actions/checkout from 3 to 4 ([#82](https://github.com/scientific-python/lazy_loader/pull/82)).
- Bump actions/setup-python from 4 to 5 ([#85](https://github.com/scientific-python/lazy_loader/pull/85)).
- Bump pre-commit from 3.5.0 to 3.6.0 ([#84](https://github.com/scientific-python/lazy_loader/pull/84)).
- Update pre-commit ([#87](https://github.com/scientific-python/lazy_loader/pull/87)).
- Use setup-python pip cache ([#95](https://github.com/scientific-python/lazy_loader/pull/95)).
- Bump codecov/codecov-action from 3 to 4 ([#93](https://github.com/scientific-python/lazy_loader/pull/93)).
- Bump pre-commit from 3.6.0 to 3.6.2 ([#100](https://github.com/scientific-python/lazy_loader/pull/100)).
- Bump changelist from 0.4 to 0.5 ([#99](https://github.com/scientific-python/lazy_loader/pull/99)).
- Refuse star imports in stub loader ([#101](https://github.com/scientific-python/lazy_loader/pull/101)).
- Bump pre-commit from 3.6.2 to 3.7.0 ([#103](https://github.com/scientific-python/lazy_loader/pull/103)).
- Update pre-commit repos ([#104](https://github.com/scientific-python/lazy_loader/pull/104)).

## Contributors

4 authors added to this release (alphabetically):

- Chris Markiewicz ([@effigies](https://github.com/effigies))
- Dan Schult ([@dschult](https://github.com/dschult))
- Jarrod Millman ([@jarrodmillman](https://github.com/jarrodmillman))
- Stefan van der Walt ([@stefanv](https://github.com/stefanv))

5 reviewers added to this release (alphabetically):

- Brigitta Sipőcz ([@bsipocz](https://github.com/bsipocz))
- Chris Markiewicz ([@effigies](https://github.com/effigies))
- Dan Schult ([@dschult](https://github.com/dschult))
- Jarrod Millman ([@jarrodmillman](https://github.com/jarrodmillman))
- Stefan van der Walt ([@stefanv](https://github.com/stefanv))

_These lists are automatically generated, and may not be complete or may contain
duplicates._

# Changelog

## [v0.3](https://github.com/scientific-python/lazy_loader/tree/v0.3) (2023-06-30)

[Full Changelog](https://github.com/scientific-python/lazy_loader/compare/v0.2...v0.3)

**Merged pull requests:**

- Announce Python 3.12 support [\#63](https://github.com/scientific-python/lazy_loader/pull/63) ([jarrodmillman](https://github.com/jarrodmillman))
- Ignore B028 [\#62](https://github.com/scientific-python/lazy_loader/pull/62) ([jarrodmillman](https://github.com/jarrodmillman))
- Use dependabot to update requirements [\#61](https://github.com/scientific-python/lazy_loader/pull/61) ([jarrodmillman](https://github.com/jarrodmillman))
- Use dependabot to update GH actions [\#60](https://github.com/scientific-python/lazy_loader/pull/60) ([jarrodmillman](https://github.com/jarrodmillman))
- Use ruff [\#59](https://github.com/scientific-python/lazy_loader/pull/59) ([jarrodmillman](https://github.com/jarrodmillman))
- Update requirements [\#58](https://github.com/scientific-python/lazy_loader/pull/58) ([jarrodmillman](https://github.com/jarrodmillman))
- Warn and discourage lazy.load of subpackages [\#57](https://github.com/scientific-python/lazy_loader/pull/57) ([dschult](https://github.com/dschult))
- Test on Python 3.12.0-beta.2 [\#53](https://github.com/scientific-python/lazy_loader/pull/53) ([jarrodmillman](https://github.com/jarrodmillman))

## [v0.2](https://github.com/scientific-python/lazy_loader/tree/v0.2)

[Full Changelog](https://github.com/scientific-python/lazy_loader/compare/v0.1...v0.2)

There were no changes since the release candidate, so
see release notes for v0.2rc0 below for details.

## [v0.2rc0](https://github.com/scientific-python/lazy_loader/tree/v0.2rc0)

[Full Changelog](https://github.com/scientific-python/lazy_loader/compare/v0.1...v0.2rc0)

**Closed issues:**

- Allow to not fail on stub attach in frozen apps [\#38](https://github.com/scientific-python/lazy_loader/issues/38)
- Stub files with absolute imports [\#36](https://github.com/scientific-python/lazy_loader/issues/36)
- Help to packaging Debian package [\#35](https://github.com/scientific-python/lazy_loader/issues/35)
- conda upload [\#33](https://github.com/scientific-python/lazy_loader/issues/33)
- Possible issues with partial lazy loading [\#32](https://github.com/scientific-python/lazy_loader/issues/32)
- Type hints/Mypy best practices? [\#28](https://github.com/scientific-python/lazy_loader/issues/28)
- Re-export non descendant attribute? [\#27](https://github.com/scientific-python/lazy_loader/issues/27)
- This is awesome [\#6](https://github.com/scientific-python/lazy_loader/issues/6)

**Merged pull requests:**

- Add information that `pyi` files are used in runtime when use `attach\_stub` [\#47](https://github.com/scientific-python/lazy_loader/pull/47) ([Czaki](https://github.com/Czaki))
- Update tests to improve coverage [\#45](https://github.com/scientific-python/lazy_loader/pull/45) ([jarrodmillman](https://github.com/jarrodmillman))
- Use codecov GH action [\#44](https://github.com/scientific-python/lazy_loader/pull/44) ([jarrodmillman](https://github.com/jarrodmillman))
- Update year [\#43](https://github.com/scientific-python/lazy_loader/pull/43) ([jarrodmillman](https://github.com/jarrodmillman))
- Update GH actions [\#42](https://github.com/scientific-python/lazy_loader/pull/42) ([jarrodmillman](https://github.com/jarrodmillman))
- Update pre-commit [\#41](https://github.com/scientific-python/lazy_loader/pull/41) ([jarrodmillman](https://github.com/jarrodmillman))
- Update optional depedencies [\#40](https://github.com/scientific-python/lazy_loader/pull/40) ([jarrodmillman](https://github.com/jarrodmillman))
- Fix extension substitution to work with `\*.pyc` files [\#39](https://github.com/scientific-python/lazy_loader/pull/39) ([Czaki](https://github.com/Czaki))
- Sort returned \_\_all\_\_ [\#34](https://github.com/scientific-python/lazy_loader/pull/34) ([stefanv](https://github.com/stefanv))

## [v0.1](https://github.com/scientific-python/lazy_loader/tree/v0.1) (2022-09-21)

[Full Changelog](https://github.com/scientific-python/lazy_loader/compare/v0.1rc3...v0.1)

**Merged pull requests:**

- Update classifiers [\#31](https://github.com/scientific-python/lazy_loader/pull/31) ([jarrodmillman](https://github.com/jarrodmillman))
- Update precommit hooks [\#30](https://github.com/scientific-python/lazy_loader/pull/30) ([jarrodmillman](https://github.com/jarrodmillman))
- Refer to SPEC for stub usage [\#29](https://github.com/scientific-python/lazy_loader/pull/29) ([stefanv](https://github.com/stefanv))

## [v0.1rc3](https://github.com/scientific-python/lazy_loader/tree/v0.1rc3) (2022-08-29)

[Full Changelog](https://github.com/scientific-python/lazy_loader/compare/v0.1rc2...v0.1rc3)

**Merged pull requests:**

- Add test and coverage badges [\#26](https://github.com/scientific-python/lazy_loader/pull/26) ([jarrodmillman](https://github.com/jarrodmillman))
- Fix typos [\#25](https://github.com/scientific-python/lazy_loader/pull/25) ([jarrodmillman](https://github.com/jarrodmillman))
- Measure test coverage [\#23](https://github.com/scientific-python/lazy_loader/pull/23) ([jarrodmillman](https://github.com/jarrodmillman))
- Document release process [\#22](https://github.com/scientific-python/lazy_loader/pull/22) ([jarrodmillman](https://github.com/jarrodmillman))
- Add classifiers [\#21](https://github.com/scientific-python/lazy_loader/pull/21) ([jarrodmillman](https://github.com/jarrodmillman))
- Lint toml files [\#20](https://github.com/scientific-python/lazy_loader/pull/20) ([jarrodmillman](https://github.com/jarrodmillman))
- Test on more versions and platforms [\#19](https://github.com/scientific-python/lazy_loader/pull/19) ([jarrodmillman](https://github.com/jarrodmillman))
- Update GH actions [\#18](https://github.com/scientific-python/lazy_loader/pull/18) ([jarrodmillman](https://github.com/jarrodmillman))
- Split out linting CI from testing [\#17](https://github.com/scientific-python/lazy_loader/pull/17) ([jarrodmillman](https://github.com/jarrodmillman))
- Update precommit hooks [\#16](https://github.com/scientific-python/lazy_loader/pull/16) ([jarrodmillman](https://github.com/jarrodmillman))
- Specify lower bounds on dependencies [\#15](https://github.com/scientific-python/lazy_loader/pull/15) ([jarrodmillman](https://github.com/jarrodmillman))
- Lower min required Python version to 3.7 [\#14](https://github.com/scientific-python/lazy_loader/pull/14) ([donatasm](https://github.com/donatasm))
- feat: add attach_stub function to load imports from type stubs [\#10](https://github.com/scientific-python/lazy_loader/pull/10) ([tlambert03](https://github.com/tlambert03))
- Avoid conflicts when function is implemented in same-named submodule [\#9](https://github.com/scientific-python/lazy_loader/pull/9) ([stefanv](https://github.com/stefanv))
- DOC fix missing comma in usage example in README.md [\#7](https://github.com/scientific-python/lazy_loader/pull/7) ([adrinjalali](https://github.com/adrinjalali))

## [v0.1rc2](https://github.com/scientific-python/lazy_loader/tree/v0.1rc2) (2022-03-10)

[Full Changelog](https://github.com/scientific-python/lazy_loader/compare/v0.1rc1...v0.1rc2)

**Merged pull requests:**

- Add contributor README [\#5](https://github.com/scientific-python/lazy_loader/pull/5) ([stefanv](https://github.com/stefanv))
- Simplify delayed exception handling and improve reporting [\#4](https://github.com/scientific-python/lazy_loader/pull/4) ([stefanv](https://github.com/stefanv))

## [v0.1rc1](https://github.com/scientific-python/lazy_loader/tree/v0.1rc1) (2022-03-01)

[Full Changelog](https://github.com/scientific-python/lazy_loader/compare/v0.0...v0.1rc1)

**Closed issues:**

- Create package on pypi [\#1](https://github.com/scientific-python/lazy_loader/issues/1)

**Merged pull requests:**

- Run pre-commit hooks [\#3](https://github.com/scientific-python/lazy_loader/pull/3) ([tupui](https://github.com/tupui))
- Add the packaging infrastructure [\#2](https://github.com/scientific-python/lazy_loader/pull/2) ([tupui](https://github.com/tupui))

\* _This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)_
