#!/usr/bin/env python3
from setuptools import setup


setup(
    name='obsdata',
    version='1.0',
    description=(
        'Package for getting data from Federal Land Manager' +
        ' Environmental Database'
    ),
    author='Bengt Rydberg',
    author_email='bengt.rydberg@molflow.com',
    entry_points={"console_scripts": [
        "get_fed_data = scripts.get_fed_data:cli",
        "get_eanet_data = scripts.get_eanet_data:cli",
    ]},
    packages=['obsdata', 'scripts', 'data', 'tests'],
    package_data={
      '': ['*.csv', '*.txt'],
    },
    include_package_data=True,
)
