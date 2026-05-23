"""Build optional C extension modules."""

from distutils.command.build_ext import build_ext
import logging
import os
import sys
from pathlib import Path
from typing import Any

try:
    from setuptools import Extension
except ImportError:
    from distutils.core import Extension

_LOGGER = logging.getLogger(__name__)


def getenv_bool(key: str, default: bool = False) -> bool:
    value = os.environ.get(key, str(default)).lower()
    if value in ("1", "true", "yes"):
        return True
    if value in ("0", "false", "no"):
        return False
    msg = f"Invalid value for boolean envvar {key}: {value}"
    raise ValueError(msg)


ulid_module = Extension(
    "ulid_transform._ulid_impl",
    [
        str(Path("src") / "ulid_transform" / "_ulid_impl.cpp"),
    ],
    language="c++",
    extra_compile_args=["-std=c++11", "-O3", "-g0"],
    extra_link_args=["-std=c++11"],
)


class BuildExt(build_ext):
    def build_extensions(self) -> None:
        if self.parallel is None:  # type: ignore[has-type, unused-ignore]
            self.parallel = os.cpu_count() or 1
        try:
            super().build_extensions()
        except Exception:  # nosec
            _LOGGER.exception("Failed to build extensions")
            if getenv_bool("REQUIRE_CYTHON") or getenv_bool("REQUIRE_EXTENSION"):
                raise


def build(setup_kwargs: Any) -> None:
    if getenv_bool("SKIP_CYTHON") or getenv_bool("SKIP_EXTENSION"):
        return
    try:
        setup_kwargs.update(
            {
                "ext_modules": [ulid_module],
                "cmdclass": {"build_ext": BuildExt},
            }
        )
    except Exception:
        _LOGGER.exception("Failed to configure C extension")
        if getenv_bool("REQUIRE_CYTHON") or getenv_bool("REQUIRE_EXTENSION"):
            raise


def _clean_stale_artifacts() -> None:
    """Remove previously-built extension artifacts before packaging.

    The wheel ``include`` globs in ``pyproject.toml`` are unconditional, so a
    stale ``.so``/``.pyd`` left in ``src/ulid_transform/`` by an earlier build
    would otherwise be packaged even when the extension is skipped
    (``SKIP_EXTENSION``) or its build failed and was swallowed, yielding an
    incompatible binary wheel instead of the requested pure-Python fallback.
    Clearing them first means the include globs only ever match a freshly
    built artifact from this run.
    """
    pkg_dir = Path("src") / "ulid_transform"
    for pattern in ("*.so", "*.pyd"):
        for artifact in pkg_dir.glob(pattern):
            artifact.unlink()


def _run_main() -> None:
    """Build the C extension when invoked directly.

    poetry-core calls ``python build_ext.py`` (no args) during the wheel
    build when ``generate-setup-file = false`` is set in
    ``pyproject.toml``.  We synthesise a ``setuptools.setup()`` call with
    an in-place ``build_ext`` so the compiled extension lands next to its
    sources in ``src/ulid_transform/`` where poetry-core's
    ``find_files_to_add`` picks it up.  ``generate-setup-file = false``
    is set so the sdist does not ship a generated ``setup.py`` that does
    ``from build_ext import *``, which fails under
    ``PYTHONSAFEPATH=1`` (see issue #137).
    """
    from setuptools import setup

    _clean_stale_artifacts()
    setup_kwargs: dict[str, Any] = {
        "name": "ulid-transform",
        "packages": ["ulid_transform"],
        "package_dir": {"": "src"},
    }
    build(setup_kwargs)
    if "ext_modules" not in setup_kwargs:
        return
    if len(sys.argv) == 1:
        sys.argv.extend(["build_ext", "--inplace"])
    setup(**setup_kwargs)


if __name__ == "__main__":
    _run_main()
