from uuid import UUID

import pytest
import tests.conftest  # noqa


@pytest.mark.benchmark(group="ulid_as_uuid")
def test_ut_ulid_now_bytes(benchmark, impl):
    assert isinstance(
        benchmark(lambda: UUID(bytes=impl.ulid_now_bytes())),
        UUID,
    )


@pytest.mark.benchmark(group="ulid_as_uuid")
def test_ut_ulid_hex(benchmark, impl):
    assert isinstance(benchmark(lambda: UUID(hex=impl.ulid_hex())), UUID)


@pytest.mark.benchmark(group="ulid_as_uuid")
def test_ulid2_uuid(benchmark):
    ulid2 = pytest.importorskip("ulid2")
    assert isinstance(benchmark(lambda: ulid2.generate_ulid_as_uuid()), UUID)


@pytest.mark.benchmark(group="ulid_as_uuid")
def test_ulidpy_uuid(benchmark):
    ulid = pytest.importorskip("ulid")
    assert isinstance(benchmark(lambda: ulid.new().uuid), UUID)
