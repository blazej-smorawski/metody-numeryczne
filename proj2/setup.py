from setuptools import setup, Extension

cmatrix = Extension('cmatrix', sources=['cmatrix.pyx'])
csolvers = Extension('csolvers', sources=['csolvers.pyx'])

setup(
    name='proj2',
    author='blazej-smorawski',
    ext_modules=[cmatrix, csolvers]
)
