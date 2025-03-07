import pytest
import tests.conftest  # noqa

example = "01J3YPYJJW00GW0X476W5TVBFE"
example_timestamp = 1722238847580


@pytest.mark.benchmark(group="timestamp")
def test_ut_timestamp(benchmark, impl):
    assert benchmark(lambda: impl.ulid_to_timestamp(example)) == example_timestamp


@pytest.mark.benchmark(group="timestamp")
def test_ulid2_timestamp(benchmark):
    ulid2 = pytest.importorskip("ulid2")
    assert (
        benchmark(lambda: ulid2.get_ulid_timestamp(example))
        == example_timestamp / 1000.0
    )


@pytest.mark.benchmark(group="timestamp")
def test_ulidpy_uuid(benchmark):
    ulid = pytest.importorskip("ulid")
    assert (
        benchmark(lambda: ulid.from_str(example).timestamp().timestamp)
        == example_timestamp / 1000.0
    )
