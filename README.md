# Fast ULID transformations

<p align="center">
  <a href="https://github.com/bluetooth-devices/ulid-transform/actions/workflows/ci.yml?query=branch%3Amain">
    <img src="https://img.shields.io/github/actions/workflow/status/bluetooth-devices/ulid-transform/ci.yml?branch=main&label=CI&logo=github&style=flat-square" alt="CI Status" >
  </a>
  <a href="https://codecov.io/gh/bluetooth-devices/ulid-transform">
    <img src="https://img.shields.io/codecov/c/github/bluetooth-devices/ulid-transform.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Test coverage percentage">
  </a>
</p>
<p align="center">
  <a href="https://python-poetry.org/">
    <img src="https://img.shields.io/badge/packaging-poetry-299bd7?style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAASCAYAAABrXO8xAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAJJSURBVHgBfZLPa1NBEMe/s7tNXoxW1KJQKaUHkXhQvHgW6UHQQ09CBS/6V3hKc/AP8CqCrUcpmop3Cx48eDB4yEECjVQrlZb80CRN8t6OM/teagVxYZi38+Yz853dJbzoMV3MM8cJUcLMSUKIE8AzQ2PieZzFxEJOHMOgMQQ+dUgSAckNXhapU/NMhDSWLs1B24A8sO1xrN4NECkcAC9ASkiIJc6k5TRiUDPhnyMMdhKc+Zx19l6SgyeW76BEONY9exVQMzKExGKwwPsCzza7KGSSWRWEQhyEaDXp6ZHEr416ygbiKYOd7TEWvvcQIeusHYMJGhTwF9y7sGnSwaWyFAiyoxzqW0PM/RjghPxF2pWReAowTEXnDh0xgcLs8l2YQmOrj3N7ByiqEoH0cARs4u78WgAVkoEDIDoOi3AkcLOHU60RIg5wC4ZuTC7FaHKQm8Hq1fQuSOBvX/sodmNJSB5geaF5CPIkUeecdMxieoRO5jz9bheL6/tXjrwCyX/UYBUcjCaWHljx1xiX6z9xEjkYAzbGVnB8pvLmyXm9ep+W8CmsSHQQY77Zx1zboxAV0w7ybMhQmfqdmmw3nEp1I0Z+FGO6M8LZdoyZnuzzBdjISicKRnpxzI9fPb+0oYXsNdyi+d3h9bm9MWYHFtPeIZfLwzmFDKy1ai3p+PDls1Llz4yyFpferxjnyjJDSEy9CaCx5m2cJPerq6Xm34eTrZt3PqxYO1XOwDYZrFlH1fWnpU38Y9HRze3lj0vOujZcXKuuXm3jP+s3KbZVra7y2EAAAAAASUVORK5CYII=" alt="Poetry">
  </a>
  <a href="https://github.com/ambv/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square" alt="black">
  </a>
  <a href="https://github.com/pre-commit/pre-commit">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">
  </a>
  <a href="https://codspeed.io/Bluetooth-Devices/ulid-transform"><img src="https://img.shields.io/endpoint?url=https://codspeed.io/badge.json" alt="CodSpeed Badge"/></a>
</p>
<p align="center">
  <a href="https://pypi.org/project/ulid-transform/">
    <img src="https://img.shields.io/pypi/v/ulid-transform.svg?logo=python&logoColor=fff&style=flat-square" alt="PyPI Version">
  </a>
  <img src="https://img.shields.io/pypi/pyversions/ulid-transform.svg?style=flat-square&logo=python&amp;logoColor=fff" alt="Supported Python versions">
  <img src="https://img.shields.io/pypi/l/ulid-transform.svg?style=flat-square" alt="License">
</p>

Create and transform ULIDs

This library will use the CPP implementation from https://github.com/suyash/ulid if cython is available, and will fallback to pure python if it is not.

## Example

```python
>>> import ulid_transform
>>> ulid_transform.ulid_hex()
'01869a2ea5fb0b43aa056293e47c0a35'
>>> ulid_transform.ulid_now()
'0001HZX0NW00GW0X476W5TVBFE'
>>> ulid_transform.ulid_at_time(1234)
'000000016JC62D620DGYNG2R8H'
>>> ulid_transform.ulid_to_bytes('0001HZX0NW00GW0X476W5TVBFE')
b'\x00\x00c\xfe\x82\xbc\x00!\xc0t\x877\x0b\xad\xad\xee'
>> ulid_transform.bytes_to_ulid(b"\x01\x86\x99?\xe8\xf3\x11\xbc\xed\xef\x86U.9\x03z")
'01GTCKZT7K26YEVVW6AMQ3J0VT'
>>> ulid_transform.ulid_to_bytes_or_none('0001HZX0NW00GW0X476W5TVBFE')
b'\x00\x00c\xfe\x82\xbc\x00!\xc0t\x877\x0b\xad\xad\xee'
>>> ulid_transform.ulid_to_bytes_or_none(None)
>>> ulid_transform.bytes_to_ulid_or_none(b'\x00\x00c\xfe\x82\xbc\x00!\xc0t\x877\x0b\xad\xad\xee')
'0001HZX0NW00GW0X476W5TVBFE'
>>> ulid_transform.bytes_to_ulid_or_none(None)
```

## Installation

Install this via pip (or your favourite package manager):

`pip install ulid-transform`

## Contributors ✨

Thanks to https://github.com/suyash/ulid which provides the cython implementation guts.

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- prettier-ignore-start -->
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- markdownlint-disable -->
<!-- markdownlint-enable -->
<!-- ALL-CONTRIBUTORS-LIST:END -->
<!-- prettier-ignore-end -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## Credits

This package was created with
[Copier](https://copier.readthedocs.io/) and the
[browniebroke/pypackage-template](https://github.com/browniebroke/pypackage-template)
project template.
