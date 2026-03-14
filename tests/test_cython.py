import os

import pytest


def _require_extension() -> bool:
    """Check if REQUIRE_EXTENSION or REQUIRE_CYTHON is truthy."""
    for key in ("REQUIRE_EXTENSION", "REQUIRE_CYTHON"):
        if os.environ.get(key, "").lower() in ("1", "true", "yes"):
            return True
    return False


def test_require_c_extension():
    """Fail if REQUIRE_EXTENSION is set and the C extension module is not available."""
    if not _require_extension():
        pytest.skip("REQUIRE_EXTENSION is not truthy")
    import ulid_transform._ulid_impl as c_impl

    assert repr(c_impl.ulid_now).startswith("<built-in function")
