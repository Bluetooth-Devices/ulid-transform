import os

import pytest


def test_require_cython():
    """Fail if REQUIRE_CYTHON is set and the Cython module is not available."""
    if os.environ.get("REQUIRE_CYTHON", "").lower() not in ("1", "true", "yes"):
        pytest.skip("REQUIRE_CYTHON is not truthy")
    import ulid_transform._ulid_impl as c_impl

    assert repr(c_impl.ulid_now).startswith("<cyfunction")
