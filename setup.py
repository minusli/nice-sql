import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

# upload pypi
# python setup.py sdist bdist_wheel
# twine upload dist/*

setup(
    name='minusSQL',
    version='0.0.3',
    author='minusli',
    author_email='minusli@foxmail.com',
    url='https://github.com/657143946/minusSQL',
    description='easy sql: decorator with sql',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        "pytest"
    ],
    entry_points={},
    license="Apache License 2.0"
)
