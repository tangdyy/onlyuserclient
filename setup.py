from setuptools import setup, find_packages 

setup(
    name = 'onlyuserclient',
    version = '1.0.1',
    description = 'onlyuser client',
    author = 'Tang dayong',    
    requires=['django', 'djangorestframework'],
    package_dir={'': 'src'},
    packages=['onlyuserclient']
)