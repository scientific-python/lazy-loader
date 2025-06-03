# Release process for `lazy-loader`

## Introduction

Example `version number`

- 1.8.dev0 # development version of 1.8 (release candidate 1)
- 1.8rc1 # 1.8 release candidate 1
- 1.8rc2.dev0 # development version of 1.8 release candidate 2
- 1.8 # 1.8 release
- 1.9.dev0 # development version of 1.9 (release candidate 1)

## Process

- Set release variables:
    ```bash
    export VERSION=<version number>
    export PREVIOUS=<previous version number>
    export ORG="scientific-python"
    export REPO="lazy-loader"
    export LOG="CHANGELOG.md"
    ```
- Autogenerate release notes

  ```bash
  changelist ${ORG}/${REPO} v${PREVIOUS} main --version ${VERSION} --config pyproject.toml --out ${VERSION}.md
  ```

- Put the output of the above command at the top of `CHANGELOG.md`

  ```bash
  cat ${VERSION}.md | cat - ${LOG} > temp && mv temp ${LOG}
  ```

- Update `version` in `lazy_loader/__init__.py`.

- Commit changes:

  ```bash
  git add lazy_loader/__init__.py ${LOG}
  git commit -m "Designate ${VERSION} release"
  ```

- Tag the release in git:

  ```bash
  git tag -s v${VERSION} -m "signed ${VERSION} tag"
  ```

  If you do not have a gpg key, use -u instead; it is important for
  Debian packaging that the tags are annotated

- Push the new meta-data to github:

  ```bash
  git push --tags origin main
  ```

  where `origin` is the name of the `github.com:scientific-python/lazy-loader`
  repository

- Create release from tag

      - go to https://github.com/scientific-python/lazy-loader/releases/new?tag=v${VERSION}
      - add v${VERSION} for the `Release title`
      - paste contents (or upload) of ${VERSION}.md in the `Describe this release section`
      - if pre-release check the box labelled `Set as a pre-release`

- Update https://github.com/scientific-python/lazy-loader/milestones:

  - close old milestone
  - ensure new milestone exists (perhaps setting due date)

- Update `version` in `lazy_loader/__init__.py`.

- Commit changes:

  ```bash
  git add lazy_loader/__init__.py
  git commit -m 'Bump version'
  git push origin main
  ```
