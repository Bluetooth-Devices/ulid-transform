"""Table-driven C-vs-Python behavioral parity matrix.

Diff-feeds a fixed grid of valid and invalid inputs to both implementations and
asserts identical observable behavior — same return value, or same exception
type. Known divergences are marked ``xfail(strict=False)`` with the issue or PR
that tracks them; when those land, the corresponding case flips XPASS and the
marker can be removed.

Companion to ``test_impl_sync.py`` (signature/docstring parity). Together they
form the cross-impl contract net referenced in issue #210.
"""

from __future__ import annotations

import pytest

import ulid_transform._py_ulid_impl as py_impl

try:
    import ulid_transform._ulid_impl as c_impl
except ImportError:
    c_impl = None


pytestmark = pytest.mark.skipif(
    c_impl is None, reason="C extension unavailable; parity matrix is C-vs-Py only"
)


_VALID_ULID_STR = "01GTCKZT7K26YEVVW6AMQ3J0VT"
_VALID_ULID_BYTES = b"\x01\x86\x99\x3f\xe8\xf3\x11\xbd\xfb\xd6\x70\x55\x6c\x18\xc0\x6b"
_VALID_ULID_STR_LOWER = "01gtckzt7k26yevvw6amq3j0vt"


# Markers for tracked divergences. ``strict=False`` so an unexpected pass
# becomes a visible XPASS (not a failure) — that's the signal to remove the
# marker once the upstream PR lands.
_xfail_pr_206 = pytest.mark.xfail(
    reason="open PR #206: align *_or_none type tolerance", strict=False
)
_xfail_pr_208 = pytest.mark.xfail(
    reason="open PR #208: align ulid_to_timestamp validation", strict=False
)
_xfail_pr_209 = pytest.mark.xfail(
    reason="open PR #209: C base32 decoder lacks lowercase + Crockford alias support",
    strict=False,
)
_xfail_issue_210_strict_input = pytest.mark.xfail(
    reason="issue #210: Py accepts bytearray/memoryview/bytes where C requires strict type",
    strict=False,
)
_xfail_issue_210_overflow = pytest.mark.xfail(
    reason="issue #210: ulid_at_time overflow semantics undefined; Py raises, C wraps",
    strict=False,
)
_xfail_issue_210_exc_type = pytest.mark.xfail(
    reason="issue #210: exception-type mismatch (AttributeError vs TypeError, etc.)",
    strict=False,
)


def _run(fn, *args):
    try:
        return ("ok", fn(*args))
    except Exception as exc:  # noqa: BLE001
        return ("exc", type(exc).__name__)


def _assert_parity(fn_name: str, *args: object) -> None:
    py_fn = getattr(py_impl, fn_name)
    c_fn = getattr(c_impl, fn_name)
    py_outcome = _run(py_fn, *args)
    c_outcome = _run(c_fn, *args)
    assert py_outcome == c_outcome, (
        f"parity mismatch for {fn_name}({', '.join(repr(a) for a in args)}): "
        f"py={py_outcome!r} c={c_outcome!r}"
    )


# --------------------------------------------------------------------------- #
# bytes_to_ulid
# --------------------------------------------------------------------------- #

_BYTES_TO_ULID_CASES = [
    pytest.param(b"\x00" * 16, id="zero-16-bytes"),
    pytest.param(_VALID_ULID_BYTES, id="valid-bytes"),
    pytest.param(b"", id="empty-bytes"),
    pytest.param(b"short", id="short-bytes"),
    pytest.param(b"\x00" * 17, id="too-long-bytes"),
    pytest.param(123, id="int"),
    pytest.param(None, id="none"),
    pytest.param("a" * 16, id="str-16"),
    pytest.param([0] * 16, marks=_xfail_issue_210_strict_input, id="list"),
    pytest.param(bytearray(16), marks=_xfail_issue_210_strict_input, id="bytearray-16"),
    pytest.param(
        memoryview(b"\x00" * 16),
        marks=_xfail_issue_210_strict_input,
        id="memoryview-16",
    ),
]


@pytest.mark.parametrize("value", _BYTES_TO_ULID_CASES)
def test_bytes_to_ulid_parity(value):
    _assert_parity("bytes_to_ulid", value)


# --------------------------------------------------------------------------- #
# ulid_to_bytes
# --------------------------------------------------------------------------- #

_ULID_TO_BYTES_CASES = [
    pytest.param(_VALID_ULID_STR, id="valid-upper"),
    pytest.param(_VALID_ULID_STR_LOWER, marks=_xfail_pr_209, id="valid-lower"),
    pytest.param("", id="empty-str"),
    pytest.param("short", id="short-str"),
    pytest.param("X" * 27, id="too-long-str"),
    pytest.param(123, id="int"),
    pytest.param(None, id="none"),
    pytest.param([0] * 26, marks=_xfail_issue_210_exc_type, id="list"),
    pytest.param(
        _VALID_ULID_BYTES, marks=_xfail_issue_210_exc_type, id="ulid-as-bytes"
    ),
    pytest.param(
        bytearray(_VALID_ULID_STR.encode()),
        marks=_xfail_issue_210_exc_type,
        id="ulid-as-bytearray",
    ),
]


@pytest.mark.parametrize("value", _ULID_TO_BYTES_CASES)
def test_ulid_to_bytes_parity(value):
    _assert_parity("ulid_to_bytes", value)


# --------------------------------------------------------------------------- #
# ulid_to_timestamp
# --------------------------------------------------------------------------- #

_ULID_TO_TIMESTAMP_CASES = [
    pytest.param(_VALID_ULID_STR, id="valid-str"),
    pytest.param(_VALID_ULID_BYTES, id="valid-bytes"),
    pytest.param(b"\x00" * 16, id="zero-bytes"),
    pytest.param("short", id="short-str"),
    pytest.param(123, id="int"),
    pytest.param(None, id="none"),
    pytest.param(b"short", marks=_xfail_pr_208, id="short-bytes"),
    pytest.param(b"\x00" * 17, marks=_xfail_pr_208, id="too-long-bytes"),
    pytest.param(bytearray(16), marks=_xfail_pr_208, id="bytearray-16"),
    pytest.param(memoryview(b"\x00" * 16), marks=_xfail_pr_208, id="memoryview-16"),
]


@pytest.mark.parametrize("value", _ULID_TO_TIMESTAMP_CASES)
def test_ulid_to_timestamp_parity(value):
    _assert_parity("ulid_to_timestamp", value)


# --------------------------------------------------------------------------- #
# ulid_to_bytes_or_none
# --------------------------------------------------------------------------- #

_ULID_TO_BYTES_OR_NONE_CASES = [
    pytest.param(None, id="none"),
    pytest.param(_VALID_ULID_STR, id="valid-str"),
    pytest.param(_VALID_ULID_STR_LOWER, marks=_xfail_pr_209, id="valid-lower"),
    pytest.param("", id="empty"),
    pytest.param("short", id="short"),
    pytest.param("é" * 26, id="non-ascii-26"),
    pytest.param(123, marks=_xfail_pr_206, id="int"),
    pytest.param(b"x" * 26, marks=_xfail_pr_206, id="bytes-26"),
    pytest.param([0] * 26, marks=_xfail_pr_206, id="list-26"),
    pytest.param(object(), marks=_xfail_pr_206, id="object"),
]


@pytest.mark.parametrize("value", _ULID_TO_BYTES_OR_NONE_CASES)
def test_ulid_to_bytes_or_none_parity(value):
    _assert_parity("ulid_to_bytes_or_none", value)


# --------------------------------------------------------------------------- #
# bytes_to_ulid_or_none
# --------------------------------------------------------------------------- #

_BYTES_TO_ULID_OR_NONE_CASES = [
    pytest.param(None, id="none"),
    pytest.param(_VALID_ULID_BYTES, id="valid-bytes"),
    pytest.param(b"\x00" * 16, id="zero-bytes"),
    pytest.param(b"short", id="short"),
    pytest.param(b"", id="empty"),
    pytest.param(b"\x00" * 17, id="too-long"),
    pytest.param(123, marks=_xfail_pr_206, id="int"),
    pytest.param("x" * 16, marks=_xfail_pr_206, id="str-16"),
    pytest.param(bytearray(16), marks=_xfail_pr_206, id="bytearray-16"),
    pytest.param([0] * 16, marks=_xfail_pr_206, id="list-16"),
    pytest.param(object(), marks=_xfail_pr_206, id="object"),
]


@pytest.mark.parametrize("value", _BYTES_TO_ULID_OR_NONE_CASES)
def test_bytes_to_ulid_or_none_parity(value):
    _assert_parity("bytes_to_ulid_or_none", value)


# --------------------------------------------------------------------------- #
# ulid_at_time / ulid_at_time_bytes — non-deterministic; only shape + error
# parity is asserted.
# --------------------------------------------------------------------------- #

_AT_TIME_VALID = [0.0, 1.0, 1_700_000_000.0]
_AT_TIME_INVALID = [
    pytest.param(None, id="none"),
    pytest.param([0], id="list"),
    pytest.param({}, id="dict"),
    pytest.param("not-a-float", marks=_xfail_issue_210_exc_type, id="str"),
    pytest.param(-1.0, marks=_xfail_issue_210_overflow, id="negative"),
    pytest.param(1e18, marks=_xfail_issue_210_overflow, id="huge"),
    # NaN / inf: Py raises on float->int conversion, C casts the NaN/inf
    # double to int64_t which is undefined behavior in C++ (typically yields
    # 0 or INT64_MIN), then silently produces a "ULID" with that timestamp.
    pytest.param(float("nan"), marks=_xfail_issue_210_overflow, id="nan"),
    pytest.param(float("inf"), marks=_xfail_issue_210_overflow, id="inf"),
    pytest.param(float("-inf"), marks=_xfail_issue_210_overflow, id="neg-inf"),
]


@pytest.mark.parametrize("timestamp", _AT_TIME_VALID)
def test_ulid_at_time_valid_shape(timestamp):
    """Valid timestamps: both impls return a 26-char str (content is random)."""
    py_val = py_impl.ulid_at_time(timestamp)
    c_val = c_impl.ulid_at_time(timestamp)
    assert isinstance(py_val, str) and len(py_val) == 26
    assert isinstance(c_val, str) and len(c_val) == 26


@pytest.mark.parametrize("timestamp", _AT_TIME_VALID)
def test_ulid_at_time_bytes_valid_shape(timestamp):
    py_val = py_impl.ulid_at_time_bytes(timestamp)
    c_val = c_impl.ulid_at_time_bytes(timestamp)
    assert isinstance(py_val, bytes) and len(py_val) == 16
    assert isinstance(c_val, bytes) and len(c_val) == 16


@pytest.mark.parametrize("timestamp", _AT_TIME_INVALID)
def test_ulid_at_time_invalid_parity(timestamp):
    """Both impls raise the same exception type on invalid input."""
    py_outcome = _run(py_impl.ulid_at_time, timestamp)
    c_outcome = _run(c_impl.ulid_at_time, timestamp)
    # Both must have errored — if either returned successfully, the case
    # doesn't belong in the invalid grid. Filtered separately so the failure
    # message is clearer than `_assert_parity` would give.
    assert py_outcome[0] == "exc" and c_outcome[0] == "exc", (
        f"expected both impls to raise; got py={py_outcome!r} c={c_outcome!r}"
    )
    assert py_outcome == c_outcome, (
        f"exception type mismatch: py={py_outcome!r} c={c_outcome!r}"
    )


@pytest.mark.parametrize("timestamp", _AT_TIME_INVALID)
def test_ulid_at_time_bytes_invalid_parity(timestamp):
    py_outcome = _run(py_impl.ulid_at_time_bytes, timestamp)
    c_outcome = _run(c_impl.ulid_at_time_bytes, timestamp)
    assert py_outcome[0] == "exc" and c_outcome[0] == "exc", (
        f"expected both impls to raise; got py={py_outcome!r} c={c_outcome!r}"
    )
    assert py_outcome == c_outcome, (
        f"exception type mismatch: py={py_outcome!r} c={c_outcome!r}"
    )


# --------------------------------------------------------------------------- #
# Generators — shape-only (output is random/time-dependent).
# --------------------------------------------------------------------------- #


def test_ulid_now_shape():
    py_val = py_impl.ulid_now()
    c_val = c_impl.ulid_now()
    assert isinstance(py_val, str) and len(py_val) == 26
    assert isinstance(c_val, str) and len(c_val) == 26


def test_ulid_now_bytes_shape():
    py_val = py_impl.ulid_now_bytes()
    c_val = c_impl.ulid_now_bytes()
    assert isinstance(py_val, bytes) and len(py_val) == 16
    assert isinstance(c_val, bytes) and len(c_val) == 16


def test_ulid_hex_shape():
    py_val = py_impl.ulid_hex()
    c_val = c_impl.ulid_hex()
    assert isinstance(py_val, str) and len(py_val) == 32
    assert isinstance(c_val, str) and len(c_val) == 32
    # Must parse as hex
    int(py_val, 16)
    int(c_val, 16)


# --------------------------------------------------------------------------- #
# Cross-impl round-trip parity for ulid_to_bytes ↔ bytes_to_ulid.
# --------------------------------------------------------------------------- #

# Sample of ULID strings spanning the alphabet — mixed-case where allowed.
# Lowercase / mixed-case cases depend on PR #209 (C base32 alias support); on
# main the C decoder silently produces wrong bytes for non-uppercase input,
# so they're xfailed until that PR lands.
_ROUND_TRIP_DECODE_SAMPLES = [
    pytest.param("00000000000000000000000000", id="all-zero"),
    pytest.param("7ZZZZZZZZZZZZZZZZZZZZZZZZZ", id="all-z-upper"),
    pytest.param(_VALID_ULID_STR, id="valid-upper"),
    pytest.param(_VALID_ULID_STR_LOWER, marks=_xfail_pr_209, id="valid-lower"),
    pytest.param("01GTCKZT7K26yevvw6amq3j0vt", marks=_xfail_pr_209, id="valid-mixed"),
]


@pytest.mark.parametrize("ulid_str", _ROUND_TRIP_DECODE_SAMPLES)
def test_ulid_to_bytes_byte_equal(ulid_str):
    """C and Py decode to identical bytes — no silent divergence."""
    assert py_impl.ulid_to_bytes(ulid_str) == c_impl.ulid_to_bytes(ulid_str)


# Encode path takes canonical uppercase bytes only — no PR #209 dependency.
_ROUND_TRIP_ENCODE_SAMPLES = [
    "00000000000000000000000000",
    "7ZZZZZZZZZZZZZZZZZZZZZZZZZ",
    _VALID_ULID_STR,
]


@pytest.mark.parametrize("ulid_str", _ROUND_TRIP_ENCODE_SAMPLES)
def test_bytes_to_ulid_byte_equal(ulid_str):
    """Encode the canonical-uppercase bytes; both impls produce the same string."""
    raw = py_impl.ulid_to_bytes(ulid_str)
    assert py_impl.bytes_to_ulid(raw) == c_impl.bytes_to_ulid(raw)
