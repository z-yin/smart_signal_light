from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(["adapt_func.pyx",
                          "data_process.pyx"])
)