import time

import pytest


def test_ulid_now(impl):
    ulid_str = impl.ulid_now()
    assert len(ulid_str) == 26
    timestamp = impl.ulid_to_timestamp(ulid_str)
    assert timestamp == pytest.approx(int(time.time() * 1000), 1)


def test_ulid_now_bytes(impl):
    ulid_bytes = impl.ulid_now_bytes()
    assert len(ulid_bytes) == 16
    timestamp = impl.ulid_to_timestamp(ulid_bytes)
    assert timestamp == pytest.approx(int(time.time() * 1000), 1)


def test_ulid_hex(impl):
    ulid_str = impl.ulid_hex()
    assert len(ulid_str) == 32


def test_ulid_to_bytes(impl):
    assert (
        impl.ulid_to_bytes("01GTCKZT7K26YEVVW6AMQ3J0VT")
        == b"\x01\x86\x99?\xe8\xf3\x11\xbc\xed\xef\x86U.9\x03z"
    )


def test_ulid_to_bytes_overflow(impl):
    with pytest.raises(ValueError):
        impl.ulid_to_bytes("01GTCKZT7K26YEVVW6AMQ3J0VT0000")


def test_ulid_to_bytes_under_low(impl):
    with pytest.raises(ValueError):
        impl.ulid_to_bytes("01")


def test_bytes_to_ulid(impl):
    assert (
        impl.bytes_to_ulid(b"\x01\x86\x99?\xe8\xf3\x11\xbc\xed\xef\x86U.9\x03z")
        == "01GTCKZT7K26YEVVW6AMQ3J0VT"
    )


def test_ulid_to_bytes_invalid_length(impl):
    with pytest.raises(ValueError):
        assert impl.ulid_to_bytes("aa")


def test_bytes_to_ulid_invalid_length(impl):
    with pytest.raises(ValueError, match="aa"):
        assert impl.bytes_to_ulid(b"aa")


def test_ulid_to_bytes_2(impl):
    assert (
        impl.ulid_to_bytes("00000000AC00GW0X476W5TVBFE")
        == b"\x00\x00\x00\x00\x01L\x00!\xc0t\x877\x0b\xad\xad\xee"
    )


def test_timestamp_string(impl):
    ulid = impl.ulid_at_time(1677627631.2127638)
    assert ulid[:10] == "01GTD6C9KC"


def test_timestamp_bytes(impl):
    ulid = impl.ulid_at_time_bytes(1677627631.2127638)
    # prefix verified with another ulid implementation (valohai/ulid2)
    assert ulid[:6] == b"\x01\x86\x9af&l"


@pytest.mark.parametrize("gen", ["ulid_at_time", "ulid_at_time_bytes"])
def test_timestamp(impl, gen):
    gen = getattr(impl, gen)
    now = time.time()
    ulid = gen(now)
    # ULIDs store time to 3 decimal places compared to python timestamps
    assert impl.ulid_to_timestamp(ulid) == int(now * 1000)


@pytest.mark.parametrize("gen", ["ulid_at_time", "ulid_at_time_bytes"])
def test_timestamp_fixed(impl, gen):
    gen = getattr(impl, gen)
    now = 1677627631.2127638
    ulid = gen(now)
    # ULIDs store time to 3 decimal places compared to python timestamps
    assert impl.ulid_to_timestamp(ulid) == int(now * 1000)


def test_non_uppercase_b32_data(impl):
    assert len(impl.ulid_to_bytes("not_uppercase_b32_data_:::")) == 16


def test_ulid_to_bytes_or_none(impl):
    """Test ulid_to_bytes_or_none."""
    assert (
        impl.ulid_to_bytes_or_none("01EYQZJXZ5Z1Z1Z1Z1Z1Z1Z1Z1")
        == b"\x01w\xaf\xf9w\xe5\xf8~\x1f\x87\xe1\xf8~\x1f\x87\xe1"
    )
    assert impl.ulid_to_bytes_or_none("invalid") is None
    assert impl.ulid_to_bytes_or_none(None) is None


def test_bytes_to_ulid_or_none(impl):
    """Test bytes_to_ulid_or_none."""
    assert (
        impl.bytes_to_ulid_or_none(
            b"\x01w\xaf\xf9w\xe5\xf8~\x1f\x87\xe1\xf8~\x1f\x87\xe1"
        )
        == "01EYQZJXZ5Z1Z1Z1Z1Z1Z1Z1Z1"
    )
    assert impl.bytes_to_ulid_or_none(b"invalid") is None
    assert impl.bytes_to_ulid_or_none(None) is None
