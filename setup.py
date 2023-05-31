import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

# upload pypi
# python setup.py sdist bdist_wheel
# twine upload dist/*

setup(
    name='nice-sql',
    version='2.0.1',
    author='minusli',
    author_email='minusli@foxmail.com',
    url='https://github.com/minusli/nicesql',
    description='easy nice sql: decorator with sql',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=["tests"]),
    python_requires='>=3',
    install_requires=[
        "pytest",
        "pymysql",
        "DBUtils",
        "nice-datapath==0.0.1",
    ],
    entry_points={},
    license="Apache License 2.0"
)
