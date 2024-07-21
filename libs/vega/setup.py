from setuptools import find_packages, setup

setup(
    name='vega',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Django>=4.0',  # specify your Django version
    ],
)