"""Generative C-vs-Python parity fuzzing.

Complements the enumerated grid in ``test_parity_matrix.py``: instead of a
fixed table of hand-picked cases, this seeds a PRNG and feeds thousands of
random valid and malformed inputs to both implementations, asserting identical
observable behavior — same return value, or same exception type. It locks in
the parity achieved across the #206-#212 / #219 fixes and guards against future
regressions in the base32 codec or the type-checking front doors.

Scope is deliberately the *deterministic* surface: ``ulid_to_bytes``,
``bytes_to_ulid``, ``ulid_to_timestamp``, and their ``*_or_none`` counterparts.
Two regions are intentionally out of scope because they hold C-vs-Py
divergences that are still tracked by open PRs and already enumerated, with
xfail markers, in the matrix:

* the ``ulid_at_time*`` numeric domain (NaN/inf/overflow/str-reject — #218/#219);
* buffer-protocol inputs (``bytearray``/``memoryview``/``list``) to the
  encode/decode front doors, where Python's buffer tolerance diverges from the
  C extension's strict type check (#210).

Seeds are fixed so CI is fully reproducible: a failure always replays from the
``seed`` printed in the assertion message.
"""

from __future__ import annotations

import random
from typing import TYPE_CHECKING

import pytest

import ulid_transform._py_ulid_impl as py_impl

if TYPE_CHECKING:
    from collections.abc import Callable

try:
    import ulid_transform._ulid_impl as c_impl
except ImportError:
    c_impl = None


pytestmark = pytest.mark.skipif(
    c_impl is None, reason="C extension unavailable; parity fuzz is C-vs-Py only"
)

# Crockford base32 alphabet (canonical, uppercase) used to encode ULIDs.
_ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
# Decode-time aliases both impls accept: I/i/L/l -> 1, O/o -> 0.
_DECODE_ALIASES = "ILOilo"
# Arbitrary printable ASCII, including chars that are *invalid* base32 (U, !, ...).
_PRINTABLE = (
    "0123456789"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "!@#$%^&*()_+-=[]{}|;:,.<>?/~` "
)

# Multiple fixed seeds widen coverage while keeping every run reproducible.
_SEEDS = [1, 7, 42, 1234, 98765]
_ITERATIONS = 4000


def _run(fn: Callable[..., object], *args: object) -> tuple[str, object]:
    """Reduce a call to a comparable ``(kind, payload)`` pair.

    ``("ok", value)`` on success, ``("exc", ExceptionTypeName)`` on failure.
    Exception *messages* are intentionally ignored — only the type matters for
    parity here (the matrix already pins message text where it counts).
    """
    try:
        return ("ok", fn(*args))
    except Exception as exc:  # noqa: BLE001 - any divergence in raised type is a finding
        return ("exc", type(exc).__name__)


def _assert_parity(fn_name: str, value: object, seed: int) -> None:
    py_outcome = _run(getattr(py_impl, fn_name), value)
    c_outcome = _run(getattr(c_impl, fn_name), value)
    assert py_outcome == c_outcome, (
        f"parity mismatch (seed={seed}) for {fn_name}({value!r}): "
        f"py={py_outcome!r} c={c_outcome!r}"
    )


def _random_valid_ulid_str(rng: random.Random) -> str:
    """A 26-char string over the canonical alphabet, optionally case-folded."""
    s = "".join(rng.choice(_ALPHABET) for _ in range(26))
    roll = rng.random()
    if roll < 0.3:
        return s.lower()
    if roll < 0.4:
        # Mixed case + decode aliases that both impls fold to 0/1.
        chars = list(s)
        for _ in range(rng.randint(1, 4)):
            chars[rng.randint(0, 25)] = rng.choice(_DECODE_ALIASES)
        return "".join(chars)
    return s


# --------------------------------------------------------------------------- #
# Decode path: valid alphabet -> identical bytes / timestamp.
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("seed", _SEEDS)
def test_decode_valid_alphabet_parity(seed):
    """Random alphabet ULIDs decode to byte-identical output in both impls."""
    rng = random.Random(seed)
    for _ in range(_ITERATIONS):
        s = _random_valid_ulid_str(rng)
        _assert_parity("ulid_to_bytes", s, seed)
        _assert_parity("ulid_to_timestamp", s, seed)
        _assert_parity("ulid_to_bytes_or_none", s, seed)


# --------------------------------------------------------------------------- #
# Decode path: arbitrary ASCII (mostly invalid base32) -> same outcome.
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("seed", _SEEDS)
def test_decode_arbitrary_ascii_parity(seed):
    """26-char strings of arbitrary ASCII: same value, or same exception type."""
    rng = random.Random(seed + 1)
    for _ in range(_ITERATIONS):
        s = "".join(rng.choice(_PRINTABLE) for _ in range(26))
        _assert_parity("ulid_to_bytes", s, seed)
        _assert_parity("ulid_to_bytes_or_none", s, seed)
        _assert_parity("ulid_to_timestamp", s, seed)


@pytest.mark.parametrize("seed", _SEEDS)
def test_decode_arbitrary_length_parity(seed):
    """Wrong-length strings (incl. empty and >26) must diverge identically."""
    rng = random.Random(seed + 2)
    for _ in range(_ITERATIONS):
        length = rng.choice([0, 1, 13, 25, 26, 27, 32])
        s = "".join(rng.choice(_PRINTABLE) for _ in range(length))
        _assert_parity("ulid_to_bytes", s, seed)
        _assert_parity("ulid_to_bytes_or_none", s, seed)
        _assert_parity("ulid_to_timestamp", s, seed)


@pytest.mark.parametrize("seed", _SEEDS)
def test_decode_non_ascii_parity(seed):
    """26-char strings with non-ASCII codepoints: same outcome in both impls."""
    rng = random.Random(seed + 3)
    pool = "éàÿĀ中µ\U0001f600"
    for _ in range(_ITERATIONS):
        s = "".join(rng.choice(_ALPHABET + pool) for _ in range(26))
        _assert_parity("ulid_to_bytes", s, seed)
        _assert_parity("ulid_to_bytes_or_none", s, seed)


# --------------------------------------------------------------------------- #
# Encode path: random bytes -> same string / timestamp / outcome.
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("seed", _SEEDS)
def test_encode_random_bytes_parity(seed):
    """Random byte strings of assorted lengths: same value or same exception."""
    rng = random.Random(seed + 4)
    for _ in range(_ITERATIONS):
        length = rng.choice([0, 1, 8, 15, 16, 16, 16, 17, 32])
        b = bytes(rng.getrandbits(8) for _ in range(length))
        _assert_parity("bytes_to_ulid", b, seed)
        _assert_parity("bytes_to_ulid_or_none", b, seed)
        _assert_parity("ulid_to_timestamp", b, seed)


# --------------------------------------------------------------------------- #
# Round trip: random 16 bytes -> ulid -> bytes, identical across impls.
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("seed", _SEEDS)
def test_round_trip_random_bytes(seed):
    """16 random bytes survive encode->decode, identically in C and Python."""
    rng = random.Random(seed + 5)
    for _ in range(_ITERATIONS):
        raw = bytes(rng.getrandbits(8) for _ in range(16))
        c_str = c_impl.bytes_to_ulid(raw)
        py_str = py_impl.bytes_to_ulid(raw)
        assert c_str == py_str, (
            f"encode mismatch (seed={seed}) for {raw!r}: c={c_str!r} py={py_str!r}"
        )
        # Round-trips back to the original bytes in both impls.
        assert c_impl.ulid_to_bytes(c_str) == raw
        assert py_impl.ulid_to_bytes(py_str) == raw


# --------------------------------------------------------------------------- #
# Type front door: random non-str/bytes scalars -> same exception type / None.
# Buffer-protocol types (bytearray/memoryview/list) are excluded here — their
# C-vs-Py divergence is a tracked #210 corner enumerated in the matrix.
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("seed", _SEEDS)
def test_wrong_type_parity(seed):
    """Non-str/bytes scalars must hit the same type-check verdict in both impls."""
    rng = random.Random(seed + 6)
    candidates = [None, 123, 12.5, {"x": 1}, object(), True, frozenset()]
    for _ in range(_ITERATIONS):
        value = rng.choice(candidates)
        for fn in (
            "ulid_to_bytes",
            "bytes_to_ulid",
            "ulid_to_timestamp",
            "ulid_to_bytes_or_none",
            "bytes_to_ulid_or_none",
        ):
            _assert_parity(fn, value, seed)
