from pytest_codspeed import BenchmarkFixture
from ulid_transform import ulid_at_time, ulid_at_time_bytes, ulid_now


def test_ulid_now(benchmark: BenchmarkFixture) -> None:
    benchmark(ulid_now)


def test_ulid_at_time(benchmark: BenchmarkFixture) -> None:
    @benchmark
    def _():
        ulid_at_time(1)


def test_ulid_at_time_bytes(benchmark: BenchmarkFixture) -> None:
    @benchmark
    def _():
        ulid_at_time_bytes(1)
