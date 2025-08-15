import sysconfig

from Cython.Build import cythonize
from setuptools import setup, Extension


def get_python_include_dir():
    return sysconfig.get_path('include')

extensions = [
    Extension(
        "qc_eda.basic.wrapper_utils",
        ["qc_eda/basic/wrapper_utils.pyx"],
    ),
]

setup(
    ext_modules=cythonize(extensions, compiler_directives={'language_level': "3"})
)