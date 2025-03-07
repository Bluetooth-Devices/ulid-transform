from __future__ import annotations

import logging

import pytest

log = logging.getLogger(__name__)


def _get_available_implementations():
    import ulid_transform._py_ulid_impl as ulid_transform_py

    yield ("python", ulid_transform_py)

    try:
        import ulid_transform._ulid_impl as ulid_transform_c

        yield ("c", ulid_transform_c)
    except ImportError:
        log.warning("Failed to import C extension", exc_info=True)
        pass


_impls = dict(_get_available_implementations())
impl_names, impl_modules = zip(*_impls.items(), strict=False)


@pytest.fixture(params=impl_modules, ids=impl_names)
def impl(request):
    """Fixture that cycles through all available implementations of the ulid_transform module."""
    return request.param
