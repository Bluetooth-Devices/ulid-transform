"""Generative C-vs-Python parity fuzzing.

Complements the enumerated grid in ``test_parity_matrix.py``: instead of a
fixed table of hand-picked cases, this seeds a PRNG and feeds thousands of
random valid and malformed inputs to both implementations, asserting identical
observable behavior — same return value, or same exception *type and message*.
It locks in the parity achieved across the #206-#212 / #219 / #221 / #226 /
#227 fixes and guards against future regressions in the base32 codec or the
type-checking front doors.

Message text is part of the comparison (see ``_run``). Once #227 aligned the
last divergent message (the Python string decoder's wrong-length ``ValueError``
now ``repr``-quotes the value like the C ``%R`` does), every malformed input
the fuzz generates raises a byte-identical message in both impls — so the
thousands of generated cases double as a regression guard for the message-text
divergence class that a type-only assertion cannot see.

Scope is deliberately the *deterministic* surface: ``ulid_to_bytes``,
``bytes_to_ulid``, ``ulid_to_timestamp``, and their ``*_or_none`` counterparts.
The ``ulid_at_time*`` family stays out of scope: its random 80-bit tail makes
full-output comparison non-deterministic, and its numeric-domain corners
(NaN/inf/overflow/str-reject — #218/#219) are pinned in the matrix instead.

Buffer-protocol inputs (``bytearray``/``memoryview``/``list``) to the
encode/decode front doors were once excluded under #210, when Python's buffer
tolerance diverged from the C extension's strict type check. That divergence is
resolved (#210 closed) — both impls now reject them identically at the strict
``str``/``bytes`` gate — so they are fuzzed here in ``test_wrong_type_parity``.

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


def _run(fn: Callable[..., object], *args: object) -> tuple[object, ...]:
    """Reduce a call to a comparable ``(kind, *payload)`` tuple.

    ``("ok", value)`` on success, ``("exc", ExceptionTypeName, message)`` on
    failure. The exception *message* is part of the comparison: every entry
    point fuzzed here now raises byte-identical messages in both impls — the C
    extension and the Python fallback agree on the wrong-type ``not <type>``
    suffix, the wrong-length ``repr``-quoted value (#227), and the non-ASCII
    rejection (#221/#226). Comparing only the exception *type* would silently
    miss message drift, the divergence class that earlier slipped past both
    this fuzz and the type-only matrix. ``ulid_at_time*`` stays out of scope
    (random tail); every other entry point on this surface is message-aligned.
    """
    try:
        return ("ok", fn(*args))
    except Exception as exc:  # noqa: BLE001 - any divergence in type or message is a finding
        return ("exc", type(exc).__name__, str(exc))


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
# Type front door: random non-str/bytes inputs -> same exception type / None.
# Includes buffer-protocol types (bytearray/memoryview/list): #210 is closed and
# both impls now reject them identically at the strict str/bytes type gate.
# --------------------------------------------------------------------------- #


def _random_buffer_value(rng: random.Random) -> object:
    """A buffer-protocol value of assorted length and random content.

    ``bytearray``/``memoryview``/``list`` all expose a buffer but are neither
    ``str`` nor ``bytes``; both impls must reject them at the type gate
    regardless of length or content.
    """
    length = rng.choice([0, 1, 15, 16, 17, 26, 32])
    raw = bytes(rng.getrandbits(8) for _ in range(length))
    kind = rng.choice(("bytearray", "memoryview", "list"))
    if kind == "bytearray":
        return bytearray(raw)
    if kind == "memoryview":
        return memoryview(raw)
    return list(raw)


@pytest.mark.parametrize("seed", _SEEDS)
def test_wrong_type_parity(seed):
    """Non-str/bytes inputs must hit the same type-check verdict in both impls.

    Covers plain scalars and buffer-protocol types (``bytearray``/
    ``memoryview``/``list``) of assorted lengths and contents — see #210.
    """
    rng = random.Random(seed + 6)
    scalars = [None, 123, 12.5, {"x": 1}, object(), True, frozenset()]
    for _ in range(_ITERATIONS):
        value = _random_buffer_value(rng) if rng.random() < 0.5 else rng.choice(scalars)
        for fn in (
            "ulid_to_bytes",
            "bytes_to_ulid",
            "ulid_to_timestamp",
            "ulid_to_bytes_or_none",
            "bytes_to_ulid_or_none",
        ):
            _assert_parity(fn, value, seed)
