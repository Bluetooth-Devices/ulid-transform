# CHANGELOG


## v1.3.0 (2025-03-05)

### Chores

- Pin prettier to 3.5.1 to fix CI
  ([#83](https://github.com/Bluetooth-Devices/ulid-transform/pull/83),
  [`d9b4fc1`](https://github.com/Bluetooth-Devices/ulid-transform/commit/d9b4fc11a5f23ee00e01778726e54cedf368820c))

- Remove unused labels workflow ([#82](https://github.com/Bluetooth-Devices/ulid-transform/pull/82),
  [`98f2b08`](https://github.com/Bluetooth-Devices/ulid-transform/commit/98f2b08803abf08b69f1e5f5bc25cc8059721504))

- Update wheel build workflow to include armv7l
  ([#89](https://github.com/Bluetooth-Devices/ulid-transform/pull/89),
  [`3132a42`](https://github.com/Bluetooth-Devices/ulid-transform/commit/3132a4213e135f60b1552c90daf18be9fd2adc29))

- **ci**: Bump python-semantic-release/python-semantic-release from 9.20.0 to 9.21.0 in the
  github-actions group ([#85](https://github.com/Bluetooth-Devices/ulid-transform/pull/85),
  [`332ae0d`](https://github.com/Bluetooth-Devices/ulid-transform/commit/332ae0d5b9ed792816fc5d9ebeb8c9c9d8e08535))

- **ci**: Bump the github-actions group with 7 updates
  ([#81](https://github.com/Bluetooth-Devices/ulid-transform/pull/81),
  [`6130f2c`](https://github.com/Bluetooth-Devices/ulid-transform/commit/6130f2ca64dcabec68f5434f0605e47a60695538))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

Co-authored-by: J. Nick Koston <nick@koston.org>

- **deps-dev**: Bump pytest from 8.3.4 to 8.3.5
  ([#88](https://github.com/Bluetooth-Devices/ulid-transform/pull/88),
  [`9cef5f7`](https://github.com/Bluetooth-Devices/ulid-transform/commit/9cef5f7968ade50883e55a3ece159ec73e6c6de7))

Bumps [pytest](https://github.com/pytest-dev/pytest) from 8.3.4 to 8.3.5. - [Release
  notes](https://github.com/pytest-dev/pytest/releases) -
  [Changelog](https://github.com/pytest-dev/pytest/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pytest-dev/pytest/compare/8.3.4...8.3.5)

--- updated-dependencies: - dependency-name: pytest dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump setuptools from 75.8.0 to 75.8.2
  ([#87](https://github.com/Bluetooth-Devices/ulid-transform/pull/87),
  [`1d38ed2`](https://github.com/Bluetooth-Devices/ulid-transform/commit/1d38ed2817291362109c8d963088ecc4eb2b7228))

Bumps [setuptools](https://github.com/pypa/setuptools) from 75.8.0 to 75.8.2. - [Release
  notes](https://github.com/pypa/setuptools/releases) -
  [Changelog](https://github.com/pypa/setuptools/blob/main/NEWS.rst) -
  [Commits](https://github.com/pypa/setuptools/compare/v75.8.0...v75.8.2)

--- updated-dependencies: - dependency-name: setuptools dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#84](https://github.com/Bluetooth-Devices/ulid-transform/pull/84),
  [`6f17818`](https://github.com/Bluetooth-Devices/ulid-transform/commit/6f1781866dcd51d01554f5c6028de5f31bef4386))

- **pre-commit.ci**: Pre-commit autoupdate
  ([#86](https://github.com/Bluetooth-Devices/ulid-transform/pull/86),
  [`24d0d69`](https://github.com/Bluetooth-Devices/ulid-transform/commit/24d0d69e2270639823ae67600ba9e88db40c0d4d))

updates: - [github.com/commitizen-tools/commitizen: v4.2.2 →
  v4.4.1](https://github.com/commitizen-tools/commitizen/compare/v4.2.2...v4.4.1) -
  [github.com/astral-sh/ruff-pre-commit: v0.9.7 →
  v0.9.9](https://github.com/astral-sh/ruff-pre-commit/compare/v0.9.7...v0.9.9)

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

### Features

- Reduce wheel sizes ([#90](https://github.com/Bluetooth-Devices/ulid-transform/pull/90),
  [`f2df716`](https://github.com/Bluetooth-Devices/ulid-transform/commit/f2df71640d8a56f9df96104ad78e8e6678821153))

Add -g0 to compile options to reduce wheel sizes


## v1.2.1 (2025-02-22)

### Bug Fixes

- Update repo links to use bluetooth-devices
  ([#80](https://github.com/Bluetooth-Devices/ulid-transform/pull/80),
  [`3beca28`](https://github.com/Bluetooth-Devices/ulid-transform/commit/3beca289c6f0e728d01461a396ac93de15730d22))

### Chores

- Bump upload/download actions to v4
  ([#73](https://github.com/Bluetooth-Devices/ulid-transform/pull/73),
  [`670b623`](https://github.com/Bluetooth-Devices/ulid-transform/commit/670b623d718d8b6622c5b0840a0dfa175ce7a0af))

- Create dependabot.yml
  ([`b7ad481`](https://github.com/Bluetooth-Devices/ulid-transform/commit/b7ad4816fe3df9e4681c63ce2825658af7a51251))

- Update dependabot.yml to include GHA
  ([`3f9f6d7`](https://github.com/Bluetooth-Devices/ulid-transform/commit/3f9f6d7294d600c50a4f8a003c6da794d1cdb294))

- **deps-dev**: Bump cython from 3.0.11 to 3.0.12
  ([#79](https://github.com/Bluetooth-Devices/ulid-transform/pull/79),
  [`36c741a`](https://github.com/Bluetooth-Devices/ulid-transform/commit/36c741a6da458fd7ed92c613e3bdc4fdb7a1726a))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump pytest from 7.4.4 to 8.3.4
  ([#69](https://github.com/Bluetooth-Devices/ulid-transform/pull/69),
  [`3aad7db`](https://github.com/Bluetooth-Devices/ulid-transform/commit/3aad7db0fb0c75dc7edd8f698565c336f85ba43b))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump pytest-benchmark from 4.0.0 to 5.1.0
  ([#71](https://github.com/Bluetooth-Devices/ulid-transform/pull/71),
  [`b0fffc6`](https://github.com/Bluetooth-Devices/ulid-transform/commit/b0fffc6908b722349ccfcf147a16f328c7ae5d49))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump pytest-codspeed from 3.1.2 to 3.2.0
  ([#76](https://github.com/Bluetooth-Devices/ulid-transform/pull/76),
  [`0781d3c`](https://github.com/Bluetooth-Devices/ulid-transform/commit/0781d3c4aff06e5c51f740fd14eb3cc83f7ffbd2))

- **deps-dev**: Bump pytest-cov from 3.0.0 to 6.0.0
  ([#67](https://github.com/Bluetooth-Devices/ulid-transform/pull/67),
  [`690cc84`](https://github.com/Bluetooth-Devices/ulid-transform/commit/690cc84106c2f489e4575a3094748923e9d23cfc))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump setuptools from 65.7.0 to 75.8.0
  ([#68](https://github.com/Bluetooth-Devices/ulid-transform/pull/68),
  [`1847efa`](https://github.com/Bluetooth-Devices/ulid-transform/commit/1847efaba902ad3d29a840e6c4db6db102189bdc))

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#72](https://github.com/Bluetooth-Devices/ulid-transform/pull/72),
  [`82c8ed5`](https://github.com/Bluetooth-Devices/ulid-transform/commit/82c8ed5a1504be470febf971a7c27b83d33d3422))

- **pre-commit.ci**: Pre-commit autoupdate
  ([#74](https://github.com/Bluetooth-Devices/ulid-transform/pull/74),
  [`ec6b661`](https://github.com/Bluetooth-Devices/ulid-transform/commit/ec6b661e6674a28c8d6bb41e888522340667c62f))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#75](https://github.com/Bluetooth-Devices/ulid-transform/pull/75),
  [`1744f59`](https://github.com/Bluetooth-Devices/ulid-transform/commit/1744f59c264dad9b448a849f965b7bd238fca735))

- **pre-commit.ci**: Pre-commit autoupdate
  ([#77](https://github.com/Bluetooth-Devices/ulid-transform/pull/77),
  [`af69a21`](https://github.com/Bluetooth-Devices/ulid-transform/commit/af69a21b6e3b1b08bd07173f7d1bffb7c8f36bf1))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#78](https://github.com/Bluetooth-Devices/ulid-transform/pull/78),
  [`76a8ad1`](https://github.com/Bluetooth-Devices/ulid-transform/commit/76a8ad18f3c5b0407ea6ab2824a43b23699b3101))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>


## v1.2.0 (2025-01-17)

### Features

- Migrate benchmarks to Python 3.13
  ([#66](https://github.com/Bluetooth-Devices/ulid-transform/pull/66),
  [`d160dd3`](https://github.com/Bluetooth-Devices/ulid-transform/commit/d160dd333020f22e902dab897b0c7839008fce91))


## v1.1.0 (2025-01-17)

### Chores

- Add codspeed benchmarks ([#64](https://github.com/Bluetooth-Devices/ulid-transform/pull/64),
  [`f7c563c`](https://github.com/Bluetooth-Devices/ulid-transform/commit/f7c563c579241adf69d7c676ca0111c35d11e43b))

- Wheel builds should only happen on release
  ([#59](https://github.com/Bluetooth-Devices/ulid-transform/pull/59),
  [`d4cbb09`](https://github.com/Bluetooth-Devices/ulid-transform/commit/d4cbb09b8c547ac9c0b8b9a41971bfadc61e4c7b))

- **pre-commit.ci**: Pre-commit autoupdate
  ([#54](https://github.com/Bluetooth-Devices/ulid-transform/pull/54),
  [`b81af0e`](https://github.com/Bluetooth-Devices/ulid-transform/commit/b81af0e631c949607a871adf2e1abd196237bf5c))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#55](https://github.com/Bluetooth-Devices/ulid-transform/pull/55),
  [`6d5155c`](https://github.com/Bluetooth-Devices/ulid-transform/commit/6d5155c56674b245b3205d6e1491d204e2825a6e))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#56](https://github.com/Bluetooth-Devices/ulid-transform/pull/56),
  [`c691406`](https://github.com/Bluetooth-Devices/ulid-transform/commit/c69140612d0840e8b40ed2b6ab55687f7746ffa6))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#57](https://github.com/Bluetooth-Devices/ulid-transform/pull/57),
  [`c30be1a`](https://github.com/Bluetooth-Devices/ulid-transform/commit/c30be1a622544fb8c645b03e848911b09b3d35a3))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#58](https://github.com/Bluetooth-Devices/ulid-transform/pull/58),
  [`2c2986f`](https://github.com/Bluetooth-Devices/ulid-transform/commit/2c2986f5db4aac03b1416f2cdac50ba0ffdcf418))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#60](https://github.com/Bluetooth-Devices/ulid-transform/pull/60),
  [`56db2e2`](https://github.com/Bluetooth-Devices/ulid-transform/commit/56db2e2ddb59cd5037c434185ad76ced699690ca))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#61](https://github.com/Bluetooth-Devices/ulid-transform/pull/61),
  [`e6ea31c`](https://github.com/Bluetooth-Devices/ulid-transform/commit/e6ea31c16334a1979919a751e4e50daab909d154))

- **pre-commit.ci**: Pre-commit autoupdate
  ([#62](https://github.com/Bluetooth-Devices/ulid-transform/pull/62),
  [`5fb4ab4`](https://github.com/Bluetooth-Devices/ulid-transform/commit/5fb4ab4d5a61fa2dcb2bdca0a967c47ebd4a4144))

- **pre-commit.ci**: Pre-commit autoupdate
  ([#63](https://github.com/Bluetooth-Devices/ulid-transform/pull/63),
  [`86ab538`](https://github.com/Bluetooth-Devices/ulid-transform/commit/86ab538b73bbc534a54c97b36ef31205d2820e5d))

### Features

- Add aarch64 wheels ([#65](https://github.com/Bluetooth-Devices/ulid-transform/pull/65),
  [`950376b`](https://github.com/Bluetooth-Devices/ulid-transform/commit/950376beb4e3d85a9f1e79a6e1408900910099d9))


## v1.0.2 (2024-08-24)

### Bug Fixes

- Switch to github trusted publishing to fix ci
  ([#53](https://github.com/Bluetooth-Devices/ulid-transform/pull/53),
  [`dfaf168`](https://github.com/Bluetooth-Devices/ulid-transform/commit/dfaf1687c32d07ea8e92358a9f1cb8275a6f6b54))


## v1.0.1 (2024-08-24)

### Bug Fixes

- Bump ci to run on python 3.11 ([#52](https://github.com/Bluetooth-Devices/ulid-transform/pull/52),
  [`857e9b8`](https://github.com/Bluetooth-Devices/ulid-transform/commit/857e9b80787e20565d41029dac5f655b1f152672))


## v1.0.0 (2024-08-24)

### Features

- Drop python 3.10 support ([#51](https://github.com/Bluetooth-Devices/ulid-transform/pull/51),
  [`b93b779`](https://github.com/Bluetooth-Devices/ulid-transform/commit/b93b77957945c38f334912d64e7c7aa4137863e3))


## v0.14.0 (2024-08-24)

### Chores

- **pre-commit.ci**: Pre-commit autoupdate
  ([#47](https://github.com/Bluetooth-Devices/ulid-transform/pull/47),
  [`3192c1c`](https://github.com/Bluetooth-Devices/ulid-transform/commit/3192c1cdf5a9c22a3d63193ee21ca133bc95006a))

updates: - [github.com/astral-sh/ruff-pre-commit: v0.5.5 →
  v0.5.6](https://github.com/astral-sh/ruff-pre-commit/compare/v0.5.5...v0.5.6) -
  [github.com/PyCQA/flake8: 7.1.0 → 7.1.1](https://github.com/PyCQA/flake8/compare/7.1.0...7.1.1) -
  [github.com/pre-commit/mirrors-mypy: v1.11.0 →
  v1.11.1](https://github.com/pre-commit/mirrors-mypy/compare/v1.11.0...v1.11.1)

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#48](https://github.com/Bluetooth-Devices/ulid-transform/pull/48),
  [`48fbe45`](https://github.com/Bluetooth-Devices/ulid-transform/commit/48fbe45e65c5a249a7c1eea3b8519b69f4f71020))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#49](https://github.com/Bluetooth-Devices/ulid-transform/pull/49),
  [`3946e2f`](https://github.com/Bluetooth-Devices/ulid-transform/commit/3946e2ff626e3034685cf6b483aa6c204dc8bca6))

updates: - [github.com/astral-sh/ruff-pre-commit: v0.5.7 →
  v0.6.1](https://github.com/astral-sh/ruff-pre-commit/compare/v0.5.7...v0.6.1)

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

### Features

- Python 3.13 support ([#50](https://github.com/Bluetooth-Devices/ulid-transform/pull/50),
  [`c50e08a`](https://github.com/Bluetooth-Devices/ulid-transform/commit/c50e08ac1c019ee8a3313780a7fd180f60e4db3f))


## v0.13.1 (2024-07-30)

### Bug Fixes

- Add pyi stubs for cython implementation
  ([#46](https://github.com/Bluetooth-Devices/ulid-transform/pull/46),
  [`dedaa87`](https://github.com/Bluetooth-Devices/ulid-transform/commit/dedaa87d9e5df4ed037bb0a95c971a6e6e376439))

### Chores

- **pre-commit.ci**: Pre-commit autoupdate
  ([#45](https://github.com/Bluetooth-Devices/ulid-transform/pull/45),
  [`d4b3890`](https://github.com/Bluetooth-Devices/ulid-transform/commit/d4b3890a78a3145c84d0a0f72d80e6face310922))

updates: - [github.com/asottile/pyupgrade: v3.16.0 →
  v3.17.0](https://github.com/asottile/pyupgrade/compare/v3.16.0...v3.17.0) -
  [github.com/astral-sh/ruff-pre-commit: v0.5.4 →
  v0.5.5](https://github.com/astral-sh/ruff-pre-commit/compare/v0.5.4...v0.5.5)

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>


## v0.13.0 (2024-07-29)

### Chores

- Ci fixes (version upgrades, repair extension build in some configs)
  ([#44](https://github.com/Bluetooth-Devices/ulid-transform/pull/44),
  [`de99c22`](https://github.com/Bluetooth-Devices/ulid-transform/commit/de99c22c1a0595fb0068d1abc3ffac157b11f3d4))

### Features

- Improve performance of C implementation
  ([#43](https://github.com/Bluetooth-Devices/ulid-transform/pull/43),
  [`f07d838`](https://github.com/Bluetooth-Devices/ulid-transform/commit/f07d838169743c4e68f344a04b6541a6a8fee239))


## v0.12.0 (2024-07-26)

### Features

- Improve testability, keep implementations in sync
  ([#40](https://github.com/Bluetooth-Devices/ulid-transform/pull/40),
  [`975079d`](https://github.com/Bluetooth-Devices/ulid-transform/commit/975079d682ffb6039454d3c041867e0d14a9f646))

* chore: ignore Cython annotation file

* fix: synchronize c/py implementations

Each implementation now exposes the same public methods, and their docstrings and signatures are
  equivalent.

* chore: remove hand-decoding ULID timestamp from test code

* feat: test C and Python implementations simultaneously

* chore: use new-style annotations in Cython too

They're exported as annotation strings anyway

* chore: add tests to make sure Python and C impls are in sync


## v0.11.1 (2024-07-26)

### Bug Fixes

- Cython build, add a test to verify the Cython module is available
  ([#41](https://github.com/Bluetooth-Devices/ulid-transform/pull/41),
  [`7187b35`](https://github.com/Bluetooth-Devices/ulid-transform/commit/7187b357b395b9c1716c8beaa5fc4db389fece18))

### Chores

- Add benchmarking tests ([#38](https://github.com/Bluetooth-Devices/ulid-transform/pull/38),
  [`456b967`](https://github.com/Bluetooth-Devices/ulid-transform/commit/456b967b457200f3001210fa527242f8a7d229b3))

- Remove IDEA configuration from repository
  ([#39](https://github.com/Bluetooth-Devices/ulid-transform/pull/39),
  [`1d95563`](https://github.com/Bluetooth-Devices/ulid-transform/commit/1d95563461026a7829b4e85a7f93efd71ed55080))


## v0.11.0 (2024-07-25)

### Features

- Add fast ULID bytes functions ([#37](https://github.com/Bluetooth-Devices/ulid-transform/pull/37),
  [`57b58ab`](https://github.com/Bluetooth-Devices/ulid-transform/commit/57b58ab269dcb97dbc905925861c3a25daf7e114))


## v0.10.2 (2024-07-25)

### Bug Fixes

- Fix error message in Cython `bytes_to_ulid`
  ([#36](https://github.com/Bluetooth-Devices/ulid-transform/pull/36),
  [`d8b5462`](https://github.com/Bluetooth-Devices/ulid-transform/commit/d8b54622d1445916f08b61ff3aad34e61bfbb986))

### Chores

- **pre-commit.ci**: Pre-commit autoupdate
  ([#33](https://github.com/Bluetooth-Devices/ulid-transform/pull/33),
  [`4d75f52`](https://github.com/Bluetooth-Devices/ulid-transform/commit/4d75f52e205ec7a4daf3cc1b23769867b9b65996))

updates: - [github.com/astral-sh/ruff-pre-commit: v0.5.0 →
  v0.5.1](https://github.com/astral-sh/ruff-pre-commit/compare/v0.5.0...v0.5.1)

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#34](https://github.com/Bluetooth-Devices/ulid-transform/pull/34),
  [`a27b5b0`](https://github.com/Bluetooth-Devices/ulid-transform/commit/a27b5b0ae2b07f1d5990ea4c04788472e921d415))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#35](https://github.com/Bluetooth-Devices/ulid-transform/pull/35),
  [`bdbb9c5`](https://github.com/Bluetooth-Devices/ulid-transform/commit/bdbb9c58f6d55209416eb7812e31669e14f39171))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>


## v0.10.1 (2024-07-05)

### Bug Fixes

- Wheel builds ([#32](https://github.com/Bluetooth-Devices/ulid-transform/pull/32),
  [`87b511e`](https://github.com/Bluetooth-Devices/ulid-transform/commit/87b511e1b00b8fa07ef7a18a5b5012e8df943441))


## v0.10.0 (2024-07-05)

### Chores

- Add more cover and benchmarks ([#27](https://github.com/Bluetooth-Devices/ulid-transform/pull/27),
  [`822ea8c`](https://github.com/Bluetooth-Devices/ulid-transform/commit/822ea8c5e69b4a9652c19ae0172c16f8236634f5))

- Switch to ruff ([#31](https://github.com/Bluetooth-Devices/ulid-transform/pull/31),
  [`98679ea`](https://github.com/Bluetooth-Devices/ulid-transform/commit/98679ea082591ae710188798b594e57c4f05f444))

- Test on 32bit ([#26](https://github.com/Bluetooth-Devices/ulid-transform/pull/26),
  [`5a62d31`](https://github.com/Bluetooth-Devices/ulid-transform/commit/5a62d31fbb75fd20aa386d44a576e939f665312d))

- **pre-commit.ci**: Pre-commit autoupdate
  ([#28](https://github.com/Bluetooth-Devices/ulid-transform/pull/28),
  [`63cc7f9`](https://github.com/Bluetooth-Devices/ulid-transform/commit/63cc7f9f596df98c59a2564a8749f7b999f1407b))

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

- **pre-commit.ci**: Pre-commit autoupdate
  ([#29](https://github.com/Bluetooth-Devices/ulid-transform/pull/29),
  [`72c43be`](https://github.com/Bluetooth-Devices/ulid-transform/commit/72c43be55a4597066d33d44a92ecb33dd2a5c806))

updates: - [github.com/pre-commit/mirrors-mypy: v1.10.0 →
  v1.10.1](https://github.com/pre-commit/mirrors-mypy/compare/v1.10.0...v1.10.1)

Co-authored-by: pre-commit-ci[bot] <66853113+pre-commit-ci[bot]@users.noreply.github.com>

### Features

- Add new fast or_none functions
  ([#30](https://github.com/Bluetooth-Devices/ulid-transform/pull/30),
  [`4d1d1ee`](https://github.com/Bluetooth-Devices/ulid-transform/commit/4d1d1ee398f791bd35a64941d3eb838cf1ef705e))


## v0.9.0 (2023-10-18)

### Bug Fixes

- Reduce size of wheels by excluding generated .cpp files
  ([#24](https://github.com/Bluetooth-Devices/ulid-transform/pull/24),
  [`29e0ff4`](https://github.com/Bluetooth-Devices/ulid-transform/commit/29e0ff474f729adea32c10a3d0adfc7801b5e892))

### Features

- Build wheel with latest cpython release
  ([#25](https://github.com/Bluetooth-Devices/ulid-transform/pull/25),
  [`8bc67fe`](https://github.com/Bluetooth-Devices/ulid-transform/commit/8bc67fe8f2c56a9aacdede63331afe6c54a1528d))


## v0.8.1 (2023-08-27)

### Bug Fixes

- Rebuild wheels with cython 3.0.2
  ([#22](https://github.com/Bluetooth-Devices/ulid-transform/pull/22),
  [`8d78432`](https://github.com/Bluetooth-Devices/ulid-transform/commit/8d78432cf81b1a2e5230dd434b50c21365686548))

### Chores

- Bump py3.12 to rc1 ([#23](https://github.com/Bluetooth-Devices/ulid-transform/pull/23),
  [`e21accd`](https://github.com/Bluetooth-Devices/ulid-transform/commit/e21accd67406f20aca65e754643e282da39ada26))


## v0.8.0 (2023-07-24)

### Features

- Initial cpython 3.12 support ([#21](https://github.com/Bluetooth-Devices/ulid-transform/pull/21),
  [`7f7e8b9`](https://github.com/Bluetooth-Devices/ulid-transform/commit/7f7e8b90d3a7a529a58d00e66be8494a18476842))


## v0.7.2 (2023-05-01)

### Bug Fixes

- Ensure windows wheel work with older versions
  ([#20](https://github.com/Bluetooth-Devices/ulid-transform/pull/20),
  [`8a440e3`](https://github.com/Bluetooth-Devices/ulid-transform/commit/8a440e3f818b3af8a694544755d55f1c221ada3a))


## v0.7.1 (2023-05-01)

### Bug Fixes

- Missing decode for _bytes_to_ulid
  ([#19](https://github.com/Bluetooth-Devices/ulid-transform/pull/19),
  [`ddf6433`](https://github.com/Bluetooth-Devices/ulid-transform/commit/ddf6433554ca3d4fef6500b84e43adf475a794bb))


## v0.7.0 (2023-04-23)

### Features

- Add a bytes_to_ulid cpp version
  ([#18](https://github.com/Bluetooth-Devices/ulid-transform/pull/18),
  [`fa1c62c`](https://github.com/Bluetooth-Devices/ulid-transform/commit/fa1c62c97be608390a5e42de5712382ee8ec86e9))


## v0.6.3 (2023-04-10)

### Bug Fixes

- Additional 32bit time fixes ([#17](https://github.com/Bluetooth-Devices/ulid-transform/pull/17),
  [`2f5f1be`](https://github.com/Bluetooth-Devices/ulid-transform/commit/2f5f1be3fe63bb63b57e158c32ab5e9d7ab16b9c))


## v0.6.2 (2023-04-09)

### Bug Fixes

- Apply 32bit cast for for random data
  ([#16](https://github.com/Bluetooth-Devices/ulid-transform/pull/16),
  [`1e1d62a`](https://github.com/Bluetooth-Devices/ulid-transform/commit/1e1d62aa961178d6416e4ac82cc0634b06260ad4))


## v0.6.1 (2023-04-09)

### Bug Fixes

- Apply 32bit time fix ([#15](https://github.com/Bluetooth-Devices/ulid-transform/pull/15),
  [`26347f0`](https://github.com/Bluetooth-Devices/ulid-transform/commit/26347f0067be94ba36607ea9b875b5d1354e6002))

### Chores

- Add test_non_uppercase_b32_data
  ([#14](https://github.com/Bluetooth-Devices/ulid-transform/pull/14),
  [`06819d0`](https://github.com/Bluetooth-Devices/ulid-transform/commit/06819d058f2a754a39221027cafb98d0568c5b18))


## v0.6.0 (2023-04-06)

### Features

- Reflect the invalid value when raising ValueError
  ([#13](https://github.com/Bluetooth-Devices/ulid-transform/pull/13),
  [`6a022fb`](https://github.com/Bluetooth-Devices/ulid-transform/commit/6a022fb4084e3a007c469e6e2993ccb3621c4271))


## v0.5.1 (2023-03-22)

### Bug Fixes

- Specify python version to build wheels
  ([#12](https://github.com/Bluetooth-Devices/ulid-transform/pull/12),
  [`9263de0`](https://github.com/Bluetooth-Devices/ulid-transform/commit/9263de0f70a4198cfcb2ba4a8f44440a7841e407))


## v0.5.0 (2023-03-22)

### Features

- Wheels for macOS and Windows ([#11](https://github.com/Bluetooth-Devices/ulid-transform/pull/11),
  [`086852e`](https://github.com/Bluetooth-Devices/ulid-transform/commit/086852e57250994d0f3c9faedabf2df6aeb9e789))

Build wheels for macOS and Windows too


## v0.4.2 (2023-03-13)

### Bug Fixes

- Ulid_now on 32bit ([#10](https://github.com/Bluetooth-Devices/ulid-transform/pull/10),
  [`c8f7dd7`](https://github.com/Bluetooth-Devices/ulid-transform/commit/c8f7dd790f987ca4310dd155a78fff263adf0cfc))


## v0.4.1 (2023-03-13)

### Bug Fixes

- Random as 0 on 32 bit arch ([#9](https://github.com/Bluetooth-Devices/ulid-transform/pull/9),
  [`c9fa4f3`](https://github.com/Bluetooth-Devices/ulid-transform/commit/c9fa4f32c12eabea67da14d0c32d9a5ac65f2842))


## v0.4.0 (2023-03-01)

### Features

- Add bytes_to_ulid ([#8](https://github.com/Bluetooth-Devices/ulid-transform/pull/8),
  [`c9a57ef`](https://github.com/Bluetooth-Devices/ulid-transform/commit/c9a57ef2d68886d37e03dd9d884a51c35a5c1e12))


## v0.3.1 (2023-03-01)

### Bug Fixes

- Encode timestamps correctly in cpp implementation
  ([#7](https://github.com/Bluetooth-Devices/ulid-transform/pull/7),
  [`c7fedc3`](https://github.com/Bluetooth-Devices/ulid-transform/commit/c7fedc350bf9848dc38af362e33819fac4036a9e))

### Chores

- Add timestamp test ([#6](https://github.com/Bluetooth-Devices/ulid-transform/pull/6),
  [`404487d`](https://github.com/Bluetooth-Devices/ulid-transform/commit/404487dd5879f83c6df6ad230ca6670edaacaa40))


## v0.3.0 (2023-02-28)

### Features

- Add examples ([#5](https://github.com/Bluetooth-Devices/ulid-transform/pull/5),
  [`be30a13`](https://github.com/Bluetooth-Devices/ulid-transform/commit/be30a133b3a03b1e6704954cf0c59f4fb64d4b7c))


## v0.2.1 (2023-02-28)

### Bug Fixes

- Drop fast-ulid for cython ([#4](https://github.com/Bluetooth-Devices/ulid-transform/pull/4),
  [`8d72d6b`](https://github.com/Bluetooth-Devices/ulid-transform/commit/8d72d6b58d306d722f096a5b3697d4365eae397d))


## v0.2.0 (2023-02-28)

### Features

- Enable cython builds ([#3](https://github.com/Bluetooth-Devices/ulid-transform/pull/3),
  [`154bf0c`](https://github.com/Bluetooth-Devices/ulid-transform/commit/154bf0c8d02591508b87c2c154ba877da2aa8f97))


## v0.1.0 (2023-02-28)

### Bug Fixes

- Remove html file ([#2](https://github.com/Bluetooth-Devices/ulid-transform/pull/2),
  [`c1a5cf4`](https://github.com/Bluetooth-Devices/ulid-transform/commit/c1a5cf4a4a8c5a2c8ba1663b9132d612fe47570d))

### Chores

- Initial commit
  ([`61fc260`](https://github.com/Bluetooth-Devices/ulid-transform/commit/61fc2606750f879ba7fb69ba3bdd371c5bcac2e8))

### Features

- Init repo ([#1](https://github.com/Bluetooth-Devices/ulid-transform/pull/1),
  [`0ef9511`](https://github.com/Bluetooth-Devices/ulid-transform/commit/0ef95113cd638617de16be44909b228d0df5f092))
