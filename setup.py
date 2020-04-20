# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

setup(
    name="paulmann",
    version="0.1.0",
    description="lib for accessing Paulmann Lichts BLE enabled lights",
    license="MIT",
    author="mjekovec2",
    author_email="matija@jekovec.net",
    url="https://github.com/mjekovec2/paulmann-lights",
    download_url = "https://github.com/mjekovec2/paulmann-lights/archive/v0.1-alpha.tar.gz", 
    keywords = ['iot', 'bluetooth', 'ble'], 
    packages=find_packages(),
    install_requires=[
        "attrs==19.3.0",
        "pygatt=4.0.5",
        "pexpect=4.8.0"
    ],
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha', 
        'Intended Audience :: Developers', 
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
    ]
)
