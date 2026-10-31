from setuptools import setup
from Cython.Build import cythonize

class Compiler:
    @staticmethod
    def compile():

        setup(
            name='Hello world app',
            ext_modules=cythonize("hello.pyx"),
        )