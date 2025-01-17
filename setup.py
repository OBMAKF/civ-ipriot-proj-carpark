# Student:          Nathan Bransby
# Student Number:   V141198

from setuptools import find_packages, setup

setup(
    name="smartpark",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "paho-mqtt",
        "sense-hat",
        "tkinter",
        "tomli",
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "smartpark = smartpark.main:main",
        ],
    },
    python_requires=">=3.10",
)
