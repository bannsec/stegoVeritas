# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
import os, sys, ast

here = os.path.abspath(os.path.dirname(__file__))
long_description = "See website for more info."

# Importing during setup causes dependency issues
with open('stegoveritas/version.py') as f:
    exec(f.read())

# TODO: Get 'six' package up to newest version. Right now py010parser is forcing it to 1.10.0, which isn't great.
# NOTE: Removing pfp package for now, until I need it. If I do end up needing it, i will need to have my own versions of both pfp and py010parser
# Specifically, I need to modify py010parser to not be stuck with an old "six" version (which is causing issues), then updated pfp to point to my version of py010parser.
# https://github.com/d0c-s4vage/py010parser/pull/19

setup(
    name='stegoveritas',
    version=version,
    description='General Steganography detection tool.',
    long_description=long_description,
    url='https://github.com/bannsec/stegoVeritas',
    author='Michael Bann',
    author_email='self@bannsecurity.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
        'Environment :: Console'
    ],
    keywords='steg stego steganography stegoveritas',
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'dist']),
    install_requires=['pillow', 'numpy', 'python-magic', 'prettytable', 'exifread', 'python-xmp-toolkit', 'stegoveritas-binwalk', 'pypng', 'apng', 'stegoveritas-pfp', 'distro'],
    extras_require={
        'dev': ['ipython','twine','pytest','python-coveralls','coverage','pytest-cov','pytest-xdist','sphinxcontrib-napoleon', 'sphinx_rtd_theme','sphinx-autodoc-typehints', 'pyOpenSSL'],
    },
    entry_points={
        'console_scripts': [
            'stegoveritas = stegoveritas.stegoveritas:main',
            'stegoveritas_install_deps = stegoveritas_install_deps.install_deps:main',
            'stegoveritas_hide_lsb = stegoveritas.hide_lsb:main',
        ],
    },
)

