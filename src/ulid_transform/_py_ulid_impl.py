import array
from random import getrandbits
from time import time

# From https://github.com/ahawker/ulid/blob/06289583e9de4286b4d80b4ad000d137816502ca/ulid/base32.py#L102
#: Array that maps encoded string char byte values to enable O(1) lookups.
_DECODE = array.array(
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


def ulid_hex() -> str:
    """
    Generate a ULID in lowercase hex that will work for a UUID.

    This ulid should not be used for cryptographically secure
    operations.

    This string can be converted with https://github.com/ahawker/ulid

    ulid.from_uuid(uuid.UUID(ulid_hex))
    """
    return f"{int(time() * 1000):012x}{getrandbits(80):020x}"


def ulid_at_time_bytes(timestamp: float) -> bytes:
    """
    Generate an ULID as 16 bytes that will work for a UUID.

    uuid.UUID(bytes=ulid_bytes)
    """
    if not isinstance(timestamp, (int, float)):
        msg = f"must be real number, not {type(timestamp).__name__}"  # type: ignore[unreachable]
        raise TypeError(msg)
    return int(timestamp * 1000).to_bytes(6, byteorder="big") + int(
        getrandbits(80)
    ).to_bytes(10, byteorder="big")


def ulid_now_bytes() -> bytes:
    """Generate an ULID as 16 bytes that will work for a UUID."""
    return ulid_at_time_bytes(time())


def ulid_now() -> str:
    """Generate a ULID."""
    return ulid_at_time(time())


def ulid_at_time(timestamp: float) -> str:
    """
    Generate a ULID.

    This ulid should not be used for cryptographically secure
    operations.

     01AN4Z07BY      79KA1307SR9X4MV3
    |----------|    |----------------|
     Timestamp          Randomness
       48bits             80bits

    This string can be loaded directly with https://github.com/ahawker/ulid

    import ulid_transform as ulid_util
    import ulid
    ulid.parse(ulid_util.ulid())
    """
    return _encode(ulid_at_time_bytes(timestamp))


def _encode(ulid_bytes: bytes) -> str:
    # This is base32 crockford encoding with the loop unrolled for performance
    #
    # This code is adapted from:
    # https://github.com/ahawker/ulid/blob/06289583e9de4286b4d80b4ad000d137816502ca/ulid/base32.py#L102
    #
    enc = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
    return (
        enc[(ulid_bytes[0] & 224) >> 5]
        + enc[ulid_bytes[0] & 31]
        + enc[(ulid_bytes[1] & 248) >> 3]
        + enc[((ulid_bytes[1] & 7) << 2) | ((ulid_bytes[2] & 192) >> 6)]
        + enc[((ulid_bytes[2] & 62) >> 1)]
        + enc[((ulid_bytes[2] & 1) << 4) | ((ulid_bytes[3] & 240) >> 4)]
        + enc[((ulid_bytes[3] & 15) << 1) | ((ulid_bytes[4] & 128) >> 7)]
        + enc[(ulid_bytes[4] & 124) >> 2]
        + enc[((ulid_bytes[4] & 3) << 3) | ((ulid_bytes[5] & 224) >> 5)]
        + enc[ulid_bytes[5] & 31]
        + enc[(ulid_bytes[6] & 248) >> 3]
        + enc[((ulid_bytes[6] & 7) << 2) | ((ulid_bytes[7] & 192) >> 6)]
        + enc[(ulid_bytes[7] & 62) >> 1]
        + enc[((ulid_bytes[7] & 1) << 4) | ((ulid_bytes[8] & 240) >> 4)]
        + enc[((ulid_bytes[8] & 15) << 1) | ((ulid_bytes[9] & 128) >> 7)]
        + enc[(ulid_bytes[9] & 124) >> 2]
        + enc[((ulid_bytes[9] & 3) << 3) | ((ulid_bytes[10] & 224) >> 5)]
        + enc[ulid_bytes[10] & 31]
        + enc[(ulid_bytes[11] & 248) >> 3]
        + enc[((ulid_bytes[11] & 7) << 2) | ((ulid_bytes[12] & 192) >> 6)]
        + enc[(ulid_bytes[12] & 62) >> 1]
        + enc[((ulid_bytes[12] & 1) << 4) | ((ulid_bytes[13] & 240) >> 4)]
        + enc[((ulid_bytes[13] & 15) << 1) | ((ulid_bytes[14] & 128) >> 7)]
        + enc[(ulid_bytes[14] & 124) >> 2]
        + enc[((ulid_bytes[14] & 3) << 3) | ((ulid_bytes[15] & 224) >> 5)]
        + enc[ulid_bytes[15] & 31]
    )


def ulid_to_bytes(value: str) -> bytes:
    """Decode a ulid to bytes."""
    if not isinstance(value, str):
        msg = f"ULID must be a string, not {type(value).__name__}"  # type: ignore[unreachable]
        raise TypeError(msg)
    if len(value) != 26 or not value.isascii():
        # The C extension measures length in UTF-8 bytes via
        # PyUnicode_AsUTF8AndSize, so any non-ASCII codepoint pushes the byte
        # length past 26 and is rejected with ValueError there. Match that: a
        # non-ASCII string is never a valid 26-character ULID, and folding the
        # check here keeps the exception type aligned (C raises ValueError; the
        # bare value.encode("ascii") below would otherwise raise
        # UnicodeEncodeError).
        msg = f"ULID must be a 26 character string: {value}"
        raise ValueError(msg)
    encoded = value.encode("ascii")
    decoding = _DECODE
    return bytes(
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
            ((decoding[encoded[10]] << 3) | (decoding[encoded[11]] >> 2)) & 0xFF,
            (
                (decoding[encoded[11]] << 6)
                | (decoding[encoded[12]] << 1)
                | (decoding[encoded[13]] >> 4)
            )
            & 0xFF,
            ((decoding[encoded[13]] << 4) | (decoding[encoded[14]] >> 1)) & 0xFF,
            (
                (decoding[encoded[14]] << 7)
                | (decoding[encoded[15]] << 2)
                | (decoding[encoded[16]] >> 3)
            )
            & 0xFF,
            ((decoding[encoded[16]] << 5) | (decoding[encoded[17]])) & 0xFF,
            ((decoding[encoded[18]] << 3) | (decoding[encoded[19]] >> 2)) & 0xFF,
            (
                (decoding[encoded[19]] << 6)
                | (decoding[encoded[20]] << 1)
                | (decoding[encoded[21]] >> 4)
            )
            & 0xFF,
            ((decoding[encoded[21]] << 4) | (decoding[encoded[22]] >> 1)) & 0xFF,
            (
                (decoding[encoded[22]] << 7)
                | (decoding[encoded[23]] << 2)
                | (decoding[encoded[24]] >> 3)
            )
            & 0xFF,
            ((decoding[encoded[24]] << 5) | (decoding[encoded[25]])) & 0xFF,
        )
    )


def bytes_to_ulid(value: bytes) -> str:
    """Encode bytes to a ulid."""
    if not isinstance(value, bytes):
        msg = f"ULID bytes must be bytes, not {type(value).__name__}"  # type: ignore[unreachable]
        raise TypeError(msg)
    if len(value) != 16:
        msg = f"ULID bytes must be 16 bytes: {value!r}"
        raise ValueError(msg)
    return _encode(value)


def ulid_to_bytes_or_none(ulid: str | None) -> bytes | None:
    """Convert an ulid to bytes."""
    if not isinstance(ulid, str) or len(ulid) != 26:
        return None
    try:
        return ulid_to_bytes(ulid)
    except (ValueError, UnicodeEncodeError):
        return None


def bytes_to_ulid_or_none(ulid_bytes: bytes | None) -> str | None:
    """Convert bytes to a ulid."""
    if not isinstance(ulid_bytes, bytes) or len(ulid_bytes) != 16:
        return None
    return bytes_to_ulid(ulid_bytes)


def ulid_to_timestamp(ulid: str | bytes) -> int:
    """
    Get the timestamp from a ULID.
    The returned value is in milliseconds since the UNIX epoch.
    """
    if isinstance(ulid, bytes):
        if len(ulid) != 16:
            msg = f"ULID bytes must be 16 bytes: {ulid!r}"
            raise ValueError(msg)
        ulid_bytes = ulid
    elif isinstance(ulid, str):
        ulid_bytes = ulid_to_bytes(ulid)
    else:
        msg = f"ULID must be a string or bytes, not {type(ulid).__name__}"  # type: ignore[unreachable]
        raise TypeError(msg)
    return int.from_bytes(b"\x00\x00" + ulid_bytes[:6], "big")
