from os import path
from setuptools import setup, find_packages

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="python-json-logger",
    version="2.0.6",
    url="http://github.com/madzak/python-json-logger",
    license="BSD",
    include_package_data=True,
    description="A python library adding a json log formatter",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Zakaria Zajac",
    author_email="zak@madzak.com",
    package_dir={'': 'src'},
    package_data={"src/pythonjsonlogger": ["py.typed"]},
    packages=find_packages("src", exclude="tests"),
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    python_requires=">=3.6",
    test_suite="tests.tests",
    classifiers=[
        'Development Status :: 6 - Mature',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: System :: Logging',
    ]
)
