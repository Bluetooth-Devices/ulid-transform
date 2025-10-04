from inspect import getdoc, signature

import pytest

import ulid_transform


def get_signature_string(func):
    """Get a comparable signature string from a function."""
    # Doctor the signature to remove quotes - this should be good enough to
    # just get rid of the quoting around deferred annotations.
    return repr(signature(func)).replace("'", "")


def test_impl_exports_required_keys(impl):
    """Test all implementations export the public API exposed by ulid_transform."""
    assert set(ulid_transform.__all__) <= set(dir(impl)), (
        f"{impl} does not match ulid_transform.__all__"
    )


def test_impls_docstrings_in_sync(impl):
    """Test implementations have matching docstrings with the python implementation."""
    import ulid_transform._py_ulid_impl as python_impl

    for key in ulid_transform.__all__:
        py_func = getattr(python_impl, key)
        impl_func = getattr(impl, key)
        assert getdoc(py_func) == getdoc(impl_func)


@pytest.mark.skipif(
    "impl.__name__ == 'ulid_transform._ulid_impl'",
    reason="C implementation uses @cython.binding(False) which breaks introspection",
)
def test_impls_signatures_in_sync(impl):
    """Test implementations have matching signatures with the python implementation."""
    import ulid_transform._py_ulid_impl as python_impl

    for key in ulid_transform.__all__:
        py_func = getattr(python_impl, key)
        impl_func = getattr(impl, key)
        assert get_signature_string(py_func) == get_signature_string(impl_func)
