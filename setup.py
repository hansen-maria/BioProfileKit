import sysconfig

from Cython.Build import cythonize
from setuptools import setup, Extension, find_packages


def get_python_include_dir():
    return sysconfig.get_path('include')

extensions = [
    Extension(
        "qc_eda.basic.wrapper_utils",
        ["src/qc_eda/basic/wrapper_utils.pyx"],
    ),
    Extension(
            "qc_eda.biological.taxonomy_validator",
            ["src/qc_eda/biological/taxonomy_validator.pyx"],
    ),
]

setup(
    name="BioProfileKit",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    ext_modules=cythonize(extensions, compiler_directives={'language_level': "3"}),
    zip_safe=False,
)