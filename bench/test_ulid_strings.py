import pytest
import tests.conftest  # noqa


@pytest.mark.benchmark(group="ulid_strings")
def test_ut_ulid_now(benchmark, impl):
    assert isinstance(benchmark(lambda: impl.ulid_now()), str)


@pytest.mark.benchmark(group="ulid_strings")
def test_ut_ulid_at_time(benchmark, impl):
    assert isinstance(benchmark(lambda: impl.ulid_at_time(1)), str)


@pytest.mark.benchmark(group="ulid_strings")
def test_ulid2_ulid_now(benchmark):
    ulid2 = pytest.importorskip("ulid2")
    assert isinstance(benchmark(lambda: ulid2.generate_ulid_as_base32()), str)


@pytest.mark.benchmark(group="ulid_strings")
def test_ulid2_ulid_at_time(benchmark):
    ulid2 = pytest.importorskip("ulid2")
    assert isinstance(
        benchmark(lambda: ulid2.generate_ulid_as_base32(timestamp=1)), str
    )


@pytest.mark.benchmark(group="ulid_strings")
def test_ulidpy_uuid_now(benchmark):
    ulid = pytest.importorskip("ulid")
    assert isinstance(benchmark(lambda: ulid.new().str), str)


@pytest.mark.benchmark(group="ulid_strings")
def test_ulidpy_uuid_at_time(benchmark):
    ulid = pytest.importorskip("ulid")
    assert isinstance(benchmark(lambda: ulid.from_timestamp(timestamp=1).str), str)
