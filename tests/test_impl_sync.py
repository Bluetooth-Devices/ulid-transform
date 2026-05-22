from inspect import getdoc, signature
import os
import random

import pytest

import ulid_transform

try:
    import ulid_transform._ulid_impl as _c_impl
except ImportError:  # pragma: no cover - exercised when C ext is unavailable
    _c_impl = None
import ulid_transform._py_ulid_impl as _py_impl

_BOTH_IMPLS_AVAILABLE = _c_impl is not None


def get_signature_string(func):
    """Get a comparable signature string from a function."""
    sig = signature(func)
    # Strip type annotations and positional-only markers for comparison
    # since C extensions cannot express them via __text_signature__.
    params = [
        p.replace(annotation=p.empty, kind=p.POSITIONAL_OR_KEYWORD)
        for p in sig.parameters.values()
    ]
    sig = sig.replace(parameters=params, return_annotation=sig.empty)
    return repr(sig).replace("'", "")


def test_impl_exports_required_keys(impl):
    """Test all implementations export the public API exposed by ulid_transform."""
    assert set(ulid_transform.__all__) <= set(dir(impl)), (
        f"{impl} does not match ulid_transform.__all__"
    )


def test_impls_in_sync(impl):
    """Test implementations are in sync with the python implementation (docstrings and signatures)."""
    import ulid_transform._py_ulid_impl as python_impl  # noqa: PLC0415

    for key in ulid_transform.__all__:
        py_func = getattr(python_impl, key)
        impl_func = getattr(impl, key)
        assert getdoc(py_func) == getdoc(impl_func)
        assert get_signature_string(py_func) == get_signature_string(impl_func)


# --- Behavioral parity: C and Python must produce byte-identical results ---


pytestmark_parity = pytest.mark.skipif(
    not _BOTH_IMPLS_AVAILABLE,
    reason="C extension not available; cross-impl parity cannot be checked",
)


@pytestmark_parity
def test_parity_bytes_to_ulid_random():
    rng = random.Random(0xC0DE)
    for _ in range(200):
        b = bytes(rng.getrandbits(8) for _ in range(16))
        assert _c_impl.bytes_to_ulid(b) == _py_impl.bytes_to_ulid(b)


@pytestmark_parity
def test_parity_ulid_to_bytes_round_trip():
    """Encoding then decoding through either impl yields the same bytes."""
    for _ in range(200):
        b = os.urandom(16)
        s = _py_impl.bytes_to_ulid(b)
        assert _c_impl.ulid_to_bytes(s) == _py_impl.ulid_to_bytes(s) == b


@pytestmark_parity
def test_parity_ulid_to_bytes_mixed_case():
    """C and Python decode mixed-case ULIDs identically (Crockford is case-insensitive)."""
    rng = random.Random(0xBEEF)
    for _ in range(100):
        b = os.urandom(16)
        s = _py_impl.bytes_to_ulid(b)
        mixed = "".join(ch.lower() if rng.random() < 0.5 else ch for ch in s)
        assert _c_impl.ulid_to_bytes(mixed) == _py_impl.ulid_to_bytes(mixed)


@pytestmark_parity
@pytest.mark.parametrize(
    "alias_char,canonical",
    [
        ("I", "1"),
        ("i", "1"),
        ("L", "1"),
        ("l", "1"),
        ("O", "0"),
        ("o", "0"),
    ],
)
def test_parity_crockford_aliases(alias_char, canonical):
    """I/L (any case) -> 1, O (any case) -> 0; both impls must agree."""
    base = "01GTCKZT7K26YEVVW6AMQ3J0VT"
    aliased = alias_char + base[1:]
    assert _c_impl.ulid_to_bytes(aliased) == _py_impl.ulid_to_bytes(aliased)


@pytestmark_parity
def test_parity_ulid_at_time_timestamp_portion():
    """First 10 chars (timestamp) of ulid_at_time must match across impls."""
    for ts in (0.0, 1.0, 1677627631.2127638, 9999999999.999):
        assert _c_impl.ulid_at_time(ts)[:10] == _py_impl.ulid_at_time(ts)[:10]
        assert _c_impl.ulid_at_time_bytes(ts)[:6] == _py_impl.ulid_at_time_bytes(ts)[:6]


@pytestmark_parity
def test_parity_ulid_hex_format():
    """ulid_hex output format (length, hex chars) matches across impls."""
    for _ in range(10):
        for h in (_c_impl.ulid_hex(), _py_impl.ulid_hex()):
            assert len(h) == 32
            assert all(ch in "0123456789abcdef" for ch in h)


@pytestmark_parity
def test_parity_ulid_to_timestamp_valid_string():
    for s in ("01GTCKZT7K26YEVVW6AMQ3J0VT", "00000000000000000000000000"):
        assert _c_impl.ulid_to_timestamp(s) == _py_impl.ulid_to_timestamp(s)


@pytestmark_parity
def test_parity_or_none_valid_inputs():
    s = "01GTCKZT7K26YEVVW6AMQ3J0VT"
    b = bytes(range(16))
    assert _c_impl.ulid_to_bytes_or_none(s) == _py_impl.ulid_to_bytes_or_none(s)
    assert _c_impl.ulid_to_bytes_or_none(None) == _py_impl.ulid_to_bytes_or_none(None)
    assert _c_impl.bytes_to_ulid_or_none(b) == _py_impl.bytes_to_ulid_or_none(b)
    assert _c_impl.bytes_to_ulid_or_none(None) == _py_impl.bytes_to_ulid_or_none(None)


@pytestmark_parity
def test_parity_or_none_invalid_lengths():
    """_or_none variants return None for length-invalid (but type-correct) input."""
    assert _c_impl.ulid_to_bytes_or_none("short") == _py_impl.ulid_to_bytes_or_none(
        "short"
    )
    assert _c_impl.bytes_to_ulid_or_none(b"short") == _py_impl.bytes_to_ulid_or_none(
        b"short"
    )
