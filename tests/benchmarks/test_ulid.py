from pytest_codspeed import BenchmarkFixture

from ulid_transform import (
    bytes_to_ulid,
    bytes_to_ulid_or_none,
    ulid_at_time,
    ulid_at_time_bytes,
    ulid_hex,
    ulid_now,
    ulid_now_bytes,
    ulid_to_bytes,
    ulid_to_bytes_or_none,
    ulid_to_timestamp,
)

ITERATIONS = 10000

_SAMPLE_ULID_STR = "01GTCKZT7K26YEVVW6AMQ3J0VT"
_SAMPLE_ULID_BYTES = b"\x01\x86\x99?\xe8\xf3\x11\xbc\xed\xef\x86U.9\x03z"


def test_ulid_now(benchmark: BenchmarkFixture) -> None:
    _ulid_now = ulid_now

    @benchmark
    def _():
        for _ in range(ITERATIONS):
            _ulid_now()


def test_ulid_now_bytes(benchmark: BenchmarkFixture) -> None:
    _ulid_now_bytes = ulid_now_bytes

    @benchmark
    def _():
        for _ in range(ITERATIONS):
            _ulid_now_bytes()


def test_ulid_hex(benchmark: BenchmarkFixture) -> None:
    _ulid_hex = ulid_hex

    @benchmark
    def _():
        for _ in range(ITERATIONS):
            _ulid_hex()


def test_ulid_at_time(benchmark: BenchmarkFixture) -> None:
    _ulid_at_time = ulid_at_time

    @benchmark
    def _():
        for _ in range(ITERATIONS):
            _ulid_at_time(1)


def test_ulid_at_time_bytes(benchmark: BenchmarkFixture) -> None:
    _ulid_at_time_bytes = ulid_at_time_bytes

    @benchmark
    def _():
        for _ in range(ITERATIONS):
            _ulid_at_time_bytes(1)


def test_ulid_to_bytes(benchmark: BenchmarkFixture) -> None:
    _ulid_to_bytes = ulid_to_bytes
    sample = _SAMPLE_ULID_STR

    @benchmark
    def _():
        for _ in range(ITERATIONS):
            _ulid_to_bytes(sample)


def test_ulid_to_bytes_or_none_valid(benchmark: BenchmarkFixture) -> None:
    _ulid_to_bytes_or_none = ulid_to_bytes_or_none
    sample = _SAMPLE_ULID_STR

    @benchmark
    def _():
        for _ in range(ITERATIONS):
            _ulid_to_bytes_or_none(sample)


def test_ulid_to_bytes_or_none_invalid(benchmark: BenchmarkFixture) -> None:
    _ulid_to_bytes_or_none = ulid_to_bytes_or_none
    sample = "not a valid ulid"

    @benchmark
    def _():
        for _ in range(ITERATIONS):
            _ulid_to_bytes_or_none(sample)


def test_bytes_to_ulid(benchmark: BenchmarkFixture) -> None:
    _bytes_to_ulid = bytes_to_ulid
    sample = _SAMPLE_ULID_BYTES

    @benchmark
    def _():
        for _ in range(ITERATIONS):
            _bytes_to_ulid(sample)


def test_bytes_to_ulid_or_none_valid(benchmark: BenchmarkFixture) -> None:
    _bytes_to_ulid_or_none = bytes_to_ulid_or_none
    sample = _SAMPLE_ULID_BYTES

    @benchmark
    def _():
        for _ in range(ITERATIONS):
            _bytes_to_ulid_or_none(sample)


def test_bytes_to_ulid_or_none_invalid(benchmark: BenchmarkFixture) -> None:
    _bytes_to_ulid_or_none = bytes_to_ulid_or_none
    sample = b"too short"

    @benchmark
    def _():
        for _ in range(ITERATIONS):
            _bytes_to_ulid_or_none(sample)


def test_ulid_to_timestamp_str(benchmark: BenchmarkFixture) -> None:
    _ulid_to_timestamp = ulid_to_timestamp
    sample = _SAMPLE_ULID_STR

    @benchmark
    def _():
        for _ in range(ITERATIONS):
            _ulid_to_timestamp(sample)


def test_ulid_to_timestamp_bytes(benchmark: BenchmarkFixture) -> None:
    _ulid_to_timestamp = ulid_to_timestamp
    sample = _SAMPLE_ULID_BYTES

    @benchmark
    def _():
        for _ in range(ITERATIONS):
            _ulid_to_timestamp(sample)
