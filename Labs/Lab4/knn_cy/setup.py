import os
from setuptools import setup

from Cython.Build import cythonize

os.environ["CC"] = "gcc"

setup(
    ext_modules=cythonize(
        ["knn1.pyx", "knn2.pyx", "knn3.pyx"], annotate=True, language_level="3"
    ),
)
