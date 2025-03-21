import pytest

import tests.conftest  # noqa

example = "01J3MS6XG9XC7X9FR15J9A82ZP"


@pytest.mark.benchmark(group="ulid_parsing")
def test_ut_decode(benchmark, impl):
    assert isinstance(benchmark(lambda: impl.ulid_to_bytes(example)), bytes)


@pytest.mark.benchmark(group="ulid_parsing")
def test_ulid2_decode(benchmark):
    ulid2 = pytest.importorskip("ulid2")
    assert isinstance(benchmark(lambda: ulid2.decode_ulid_base32(example)), bytes)


@pytest.mark.benchmark(group="ulid_parsing")
def test_ulidpy_decode(benchmark):
    ulid = pytest.importorskip("ulid")
    assert isinstance(benchmark(lambda: ulid.from_str(example).bytes), bytes)
