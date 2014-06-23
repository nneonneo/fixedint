try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

readme = open('README.rst')
desc = []
for line in readme:
    if line.strip() == '.. __CUT__':
        break
    desc.append(line)
long_description = ''.join(desc)
readme.close()

setup(
    name = 'fixedint',
    version = '0.1.3',
    author = 'Robert Xiao',
    author_email = 'robert.bo.xiao@gmail.com',
    url = 'https://github.com/nneonneo/fixedint',
    license = 'PSF',
    classifiers = [
        "License :: OSI Approved :: Python Software Foundation License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.4",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Utilities",
    ],
    description = "simple fixed-width integers",
    packages = ['fixedint'],
    long_description=long_description,
)
