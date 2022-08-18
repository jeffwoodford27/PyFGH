# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))



# This call to setup() does all the work
setup(
    name="PyFGH",
    version="0.3.6",
    description="PyFGH library",
    long_description="This is a library for PyFGH",
    author="Josiah Randleman, Nelson Maxey, Tyler Law, Dr. Jeffrey Woodford",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=['PyFGH', 'PyFGH/util'],
    #package_dir={':outputfiles': 'PyFGH/outputfiles', ":testingfiles": 'PyFGH/testingfiles', ":util": 'PyFGH/util'},
    include_package_data=True,
    # install_requires=["numpy", "scipy", "math", "time", "os", "csv", "scipy"]
)