"""Build optional C extension modules."""

import logging
import os
from distutils.command.build_ext import build_ext
from os.path import join
from typing import Any

try:
    from setuptools import Extension
except ImportError:
    from distutils.core import Extension


def getenv_bool(key: str, default: bool = False) -> bool:
    value = os.environ.get(key, str(default)).lower()
    if value in ("1", "true", "yes"):
        return True
    if value in ("0", "false", "no"):
        return False
    raise ValueError(f"Invalid value for boolean envvar {key}: {value}")


ulid_module = Extension(
    "ulid_transform._ulid_impl",
    [
        join("src", "ulid_transform", "_ulid_impl.cpp"),
    ],
    language="c++",
    extra_compile_args=["-std=c++11", "-O3", "-g0"],
    extra_link_args=["-std=c++11"],
)


class BuildExt(build_ext):
    def build_extensions(self) -> None:
        try:
            super().build_extensions()
        except Exception:  # nosec
            logging.exception("Failed to build extensions")
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
        logging.exception("Failed to configure C extension")
        if getenv_bool("REQUIRE_CYTHON") or getenv_bool("REQUIRE_EXTENSION"):
            raise
