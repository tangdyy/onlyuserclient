from setuptools import setup, find_packages 

with open("readme.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setup(
    name = 'onlyuserclient',
    version = '1.0.8',
    description = 'onlyuser client',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tangdyy/onlyuserclient",
    author = 'Tang dayong', 
    author_email="tangdyy@126.com",
    requires=['django', 'djangorestframework'],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6' 
)