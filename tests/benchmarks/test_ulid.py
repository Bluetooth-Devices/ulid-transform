from pytest_codspeed import BenchmarkFixture

from ulid_transform import ulid_at_time, ulid_at_time_bytes, ulid_now

ITERATIONS = 10000


def test_ulid_now(benchmark: BenchmarkFixture) -> None:
    _ulid_now = ulid_now

    @benchmark
    def _():
        for _ in range(ITERATIONS):
            _ulid_now()


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
