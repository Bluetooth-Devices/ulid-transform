"""Tests for Crockford base32 decoding edge cases (case + aliases)."""

import pytest

_REF_ULID = "01GTCKZT7K26YEVVW6AMQ3J0VT"
_REF_BYTES = b"\x01\x86\x99?\xe8\xf3\x11\xbc\xed\xef\x86U.9\x03z"


def test_lowercase_decodes_same_as_uppercase(impl):
    assert impl.ulid_to_bytes(_REF_ULID.lower()) == _REF_BYTES


@pytest.mark.parametrize(
    "ulid",
    [
        "01gtCKZT7K26YEVVW6AMQ3J0VT",
        "01GtCkZt7k26yEvVw6amq3j0vt",
        "01GTCKZT7K26YEVVW6AMQ3J0vt",
    ],
)
def test_mixed_case_decodes(impl, ulid):
    assert impl.ulid_to_bytes(ulid) == _REF_BYTES


@pytest.mark.parametrize(
    "alias,canon",
    [("I", "1"), ("i", "1"), ("L", "1"), ("l", "1"), ("O", "0"), ("o", "0")],
)
def test_crockford_aliases(impl, alias, canon):
    """I/L (any case) decode as 1, O (any case) decodes as 0."""
    aliased = alias + _REF_ULID[1:]
    canonical = canon + _REF_ULID[1:]
    assert impl.ulid_to_bytes(aliased) == impl.ulid_to_bytes(canonical)


@pytest.mark.parametrize("char", ["U", "u"])
def test_u_remains_excluded(impl, char):
    """Crockford excludes U from the alphabet entirely.

    Both implementations treat U the same (invalid -> 0xFF lookup),
    so decoding does not raise but the result is implementation-defined.
    The contract is that C and Python produce identical output.
    """
    candidate = char + _REF_ULID[1:]
    # No exception, and length is preserved
    assert len(impl.ulid_to_bytes(candidate)) == 16
