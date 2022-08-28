# Release process for `lazy_loader`

## Introduction

Example `version`

- 1.8.dev0 \# development version of 1.8 (release candidate 1)
- 1.8rc1 \# 1.8 release candidate 1
- 1.8rc2.dev0 \# development version of 1.8 (release candidate 2)
- 1.8 \# 1.8 release
- 1.9.dev0 \# development version of 1.9 (release candidate 1)

## Process

- Update and review `CHANGELOG.md`:

      gem install github_changelog_generator
      github_changelog_generator -u scientific-python -p lazy_loader --since-tag=<last tag>

- Update `version` in `pyproject.toml`.

- Commit changes:

      git add pyproject.toml CHANGELOG.md
      git commit -m 'Designate <version> release'

- Add the version number (e.g., [v1.2.0]{.title-ref}) as a tag in git:

      git tag -s [-u <key-id>] v<version> -m 'signed <version> tag'

  If you do not have a gpg key, use -u instead; it is important for
  Debian packaging that the tags are annotated

- Push the new meta-data to github:

      git push --tags origin main

  where `origin` is the name of the `github.com:scientific-python/lazy_loader`
  repository

- Review the github release page:

      https://github.com/scientific-python/lazy_loader/releases

- Publish on PyPi:

      git clean -fxd
      pip install flit
      flit build
      flit publish

- Update `version` in `pyproject.toml`.

- Commit changes:

      git add pyproject.toml
      git commit -m 'Bump version'
      git push origin main
