try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name = 'fixedint',
    version = '0.1.0',
    author = 'Robert Xiao',
    author_email = 'robert.bo.xiao@gmail.com',
    url = 'https://github.com/nneonneo/fixedint',
    license = 'PSF',
    classifiers = [
        "License :: OSI Approved :: Python Software Foundation License",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Utilities",
    ],
    description = "simple fixed-width integers",
    packages = ['fixedint'],
    long_description=open('README.rst').read(),
)
