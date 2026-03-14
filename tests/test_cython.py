import os

import pytest


def test_require_c_extension():
    """Fail if REQUIRE_EXTENSION is set and the C extension module is not available."""
    if os.environ.get("REQUIRE_EXTENSION", "").lower() not in ("1", "true", "yes"):
        pytest.skip("REQUIRE_EXTENSION is not truthy")
    import ulid_transform._ulid_impl as c_impl

    assert repr(c_impl.ulid_now).startswith("<built-in function")
