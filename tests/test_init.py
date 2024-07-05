import array
import time

import pytest

from ulid_transform import (
    bytes_to_ulid,
    bytes_to_ulid_or_none,
    bytes_to_uuid_hex_or_none,
    ulid_at_time,
    ulid_hex,
    ulid_now,
    ulid_to_bytes,
    ulid_to_bytes_or_none,
    uuid_hex_to_bytes_or_none,
)


def test_ulid_now():
    ulid_str = ulid_now()
    assert len(ulid_str) == 26
    timestamp = _ulid_timestamp(ulid_str)
    assert timestamp == pytest.approx(int(time.time() * 1000), 1)


def test_ulid_hex():
    ulid_str = ulid_hex()
    assert len(ulid_str) == 32


def test_ulid_to_bytes():
    assert (
        ulid_to_bytes("01GTCKZT7K26YEVVW6AMQ3J0VT")
        == b"\x01\x86\x99?\xe8\xf3\x11\xbc\xed\xef\x86U.9\x03z"
    )


def test_ulid_to_bytes_overflow():
    with pytest.raises(ValueError):
        ulid_to_bytes("01GTCKZT7K26YEVVW6AMQ3J0VT0000")


def test_ulid_to_bytes_under_low():
    with pytest.raises(ValueError):
        ulid_to_bytes("01")


def test_bytes_to_ulid():
    assert (
        bytes_to_ulid(b"\x01\x86\x99?\xe8\xf3\x11\xbc\xed\xef\x86U.9\x03z")
        == "01GTCKZT7K26YEVVW6AMQ3J0VT"
    )


def test_ulid_to_bytes_invalid_length():
    with pytest.raises(ValueError):
        assert ulid_to_bytes("aa")


def test_bytes_to_ulid_invalid_length():
    with pytest.raises(ValueError, match="aa"):
        assert bytes_to_ulid(b"aa")


def test_ulid_to_bytes_2():
    assert (
        ulid_to_bytes("00000000AC00GW0X476W5TVBFE")
        == b"\x00\x00\x00\x00\x01L\x00!\xc0t\x877\x0b\xad\xad\xee"
    )


def test_timestamp_string():
    ulid = ulid_at_time(1677627631.2127638)
    assert ulid[:10] == "01GTD6C9KC"


def test_timestamp():
    now = time.time()
    ulid = ulid_at_time(now)
    # ULIDs store time to 3 decimal places compared to python timestamps
    assert _ulid_timestamp(ulid) == int(now * 1000)


def test_timestamp_fixed():
    now = 1677627631.2127638
    ulid = ulid_at_time(now)
    # ULIDs store time to 3 decimal places compared to python timestamps
    assert _ulid_timestamp(ulid) == int(now * 1000)


def _ulid_timestamp(ulid: str) -> int:
    encoded = ulid[:10].encode("ascii")
    # This unpacks the time from the ulid

    # Copied from
    # https://github.com/ahawker/ulid/blob/06289583e9de4286b4d80b4ad000d137816502ca/ulid/base32.py#L296
    decoding = array.array(
        "B",
        (
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0x00,
            0x01,
            0x02,
            0x03,
            0x04,
            0x05,
            0x06,
            0x07,
            0x08,
            0x09,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0x0A,
            0x0B,
            0x0C,
            0x0D,
            0x0E,
            0x0F,
            0x10,
            0x11,
            0x01,
            0x12,
            0x13,
            0x01,
            0x14,
            0x15,
            0x00,
            0x16,
            0x17,
            0x18,
            0x19,
            0x1A,
            0xFF,
            0x1B,
            0x1C,
            0x1D,
            0x1E,
            0x1F,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0x0A,
            0x0B,
            0x0C,
            0x0D,
            0x0E,
            0x0F,
            0x10,
            0x11,
            0x01,
            0x12,
            0x13,
            0x01,
            0x14,
            0x15,
            0x00,
            0x16,
            0x17,
            0x18,
            0x19,
            0x1A,
            0xFF,
            0x1B,
            0x1C,
            0x1D,
            0x1E,
            0x1F,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
            0xFF,
        ),
    )
    return int.from_bytes(
        bytes(
            (
                ((decoding[encoded[0]] << 5) | decoding[encoded[1]]) & 0xFF,
                ((decoding[encoded[2]] << 3) | (decoding[encoded[3]] >> 2)) & 0xFF,
                (
                    (decoding[encoded[3]] << 6)
                    | (decoding[encoded[4]] << 1)
                    | (decoding[encoded[5]] >> 4)
                )
                & 0xFF,
                ((decoding[encoded[5]] << 4) | (decoding[encoded[6]] >> 1)) & 0xFF,
                (
                    (decoding[encoded[6]] << 7)
                    | (decoding[encoded[7]] << 2)
                    | (decoding[encoded[8]] >> 3)
                )
                & 0xFF,
                ((decoding[encoded[8]] << 5) | (decoding[encoded[9]])) & 0xFF,
            )
        ),
        byteorder="big",
    )


def test_non_uppercase_b32_data():
    assert len(ulid_to_bytes("not_uppercase_b32_data_:::")) == 16


def test_ulid_to_bytes_or_none() -> None:
    """Test ulid_to_bytes_or_none."""

    assert (
        ulid_to_bytes_or_none("01EYQZJXZ5Z1Z1Z1Z1Z1Z1Z1Z1")
        == b"\x01w\xaf\xf9w\xe5\xf8~\x1f\x87\xe1\xf8~\x1f\x87\xe1"
    )
    assert ulid_to_bytes_or_none("invalid") is None
    assert ulid_to_bytes_or_none(None) is None


def test_bytes_to_ulid_or_none() -> None:
    """Test bytes_to_ulid_or_none."""

    assert (
        bytes_to_ulid_or_none(b"\x01w\xaf\xf9w\xe5\xf8~\x1f\x87\xe1\xf8~\x1f\x87\xe1")
        == "01EYQZJXZ5Z1Z1Z1Z1Z1Z1Z1Z1"
    )
    assert bytes_to_ulid_or_none(b"invalid") is None
    assert bytes_to_ulid_or_none(None) is None


def test_uuid_hex_to_bytes_or_none() -> None:
    """Test uuid_hex_to_bytes_or_none."""

    assert (
        uuid_hex_to_bytes_or_none("0123456789abcdef0123456789abcdef")
        == b"\x01#Eg\x89\xab\xcd\xef\x01#Eg\x89\xab\xcd\xef"
    )
    assert uuid_hex_to_bytes_or_none("invalid") is None
    assert uuid_hex_to_bytes_or_none(None) is None


def test_bytes_to_uuid_hex_or_none() -> None:
    """Test bytes_to_uuid_hex_or_none."""

    assert (
        bytes_to_uuid_hex_or_none(b"\x01#Eg\x89\xab\xcd\xef\x01#Eg\x89\xab\xcd\xef")
        == "0123456789abcdef0123456789abcdef"
    )
    assert bytes_to_uuid_hex_or_none(b"invalid") is None
    assert bytes_to_uuid_hex_or_none(None) is None
