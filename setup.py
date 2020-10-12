from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="python-json-logger",
    version="2.0.1",
    url="http://github.com/madzak/python-json-logger",
    license="BSD",
    description="A python library adding a json log formatter",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Zakaria Zajac",
    author_email="zak@madzak.com",
    package_dir={'': 'src'},
    packages=find_packages("src", exclude="tests"),
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    python_requires='>=3.4',
    test_suite="tests.tests",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: System :: Logging',
    ]
)
