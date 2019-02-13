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
    install_requires=['pillow', 'numpy', 'pfp', 'python-magic', 'prettytable'],
    extras_require={
        'dev': ['six==1.10.0','ipython','twine','pytest','python-coveralls','coverage','pytest-cov','pytest-xdist','sphinxcontrib-napoleon', 'sphinx_rtd_theme','sphinx-autodoc-typehints', 'pyOpenSSL'],
    },
    entry_points={
        'console_scripts': [
            'stegoveritas = stegoveritas.stegoveritas:main',
        ],
    },
)

