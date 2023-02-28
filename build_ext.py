"""Build optional cython modules."""

import os
from distutils.command.build_ext import build_ext
from os.path import join
from typing import Any

try:
    from setuptools import Extension
except ImportError:
    from distutils.core import Extension

convert_module = Extension(
    "ulid_transform._convert",
    [join("src", "ulid_transform", "_convert.pyx")],
    language="c++",
)
generate_module = Extension(
    "ulid_transform._generate",
    [join("src", "ulid_transform", "_generate.pyx")],
    language="c++",
)


class BuildExt(build_ext):
    def build_extensions(self) -> None:
        try:
            super().build_extensions()
        except Exception:  # nosec
            pass


def build(setup_kwargs: Any) -> None:
    if os.environ.get("SKIP_CYTHON", False):
        return
    try:
        from Cython.Build import cythonize

        setup_kwargs.update(
            dict(
                ext_modules=cythonize(
                    [
                        convert_module,
                        generate_module,
                    ],
                    compiler_directives={"language_level": "3"},  # Python 3
                ),
                cmdclass=dict(build_ext=BuildExt),
            )
        )
    except Exception:
        if os.environ.get("REQUIRE_CYTHON"):
            raise
        pass
