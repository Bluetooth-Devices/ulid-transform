from inspect import getdoc, signature

import ulid_transform


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
    assert set(ulid_transform.__all__) <= set(dir(impl)), (  # type: ignore[attr-defined]
        f"{impl} does not match ulid_transform.__all__"
    )


def test_impls_in_sync(impl):
    """Test implementations are in sync with the python implementation (docstrings and signatures)."""
    import ulid_transform._py_ulid_impl as python_impl

    for key in ulid_transform.__all__:  # type: ignore[attr-defined]
        py_func = getattr(python_impl, key)
        impl_func = getattr(impl, key)
        assert getdoc(py_func) == getdoc(impl_func)
        assert get_signature_string(py_func) == get_signature_string(impl_func)
