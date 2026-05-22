"""Build optional C extension modules."""

from distutils.command.build_ext import build_ext
import logging
import os
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
