
from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Stockolio',
    version='0.0.8',
    description='A Python stock portfolio, with transaction managers for several Dutch brokers',
    long_description=readme,
    author='Aris Wallet',
    author_email='aris.wallet@gmail.com',
    url='https://github.com/promwarm/Stockolio',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)