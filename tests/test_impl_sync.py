from inspect import getdoc, signature

import ulid_transform


def get_signature_string(func):
    """Get a comparable signature string from a function."""
    # Doctor the signature to remove quotes - this should be good enough to
    # just get rid of the quoting around deferred annotations.
    try:
        return repr(signature(func)).replace("'", "")
    except ValueError:
        # Functions with @cython.binding(False) don't have introspectable signatures
        return None


def test_impl_exports_required_keys(impl):
    """Test all implementations export the public API exposed by ulid_transform."""
    assert set(ulid_transform.__all__) <= set(dir(impl)), (
        f"{impl} does not match ulid_transform.__all__"
    )


def test_impls_in_sync(impl):
    """Test implementations are in sync with the python implementation (docstrings and signatures)."""
    import ulid_transform._py_ulid_impl as python_impl

    # Check if this is the C implementation (uses @cython.binding(False))
    is_c_impl = impl.__name__ == "ulid_transform._ulid_impl"

    for key in ulid_transform.__all__:
        py_func = getattr(python_impl, key)
        impl_func = getattr(impl, key)
        assert getdoc(py_func) == getdoc(impl_func)
        # Skip signature checks for C implementation with @cython.binding(False)
        # as it doesn't provide reliable introspection
        if not is_c_impl:
            py_sig = get_signature_string(py_func)
            impl_sig = get_signature_string(impl_func)
            if py_sig is not None and impl_sig is not None:
                assert py_sig == impl_sig
