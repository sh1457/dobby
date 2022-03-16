import setuptools
from pathlib import Path

MAJOR, MINOR, PATCH = 0, 1, 0
VERSION = f"{MAJOR}.{MINOR}.{PATCH}"

DESCRIPTION = ("A collection of python scripts to scrape data from the web,"
               " generate data parametrically, animate images/charts primarily"
               " for easy web publishing")

path = Path(__file__).with_name("README.md")


LONG_DESCRIPTION = None
try:
    with open(path, "r") as fp:
        LONG_DESCRIPTION = fp.read()
except Exception as exc:
    print("Failed to open/read the README.md file to get the long description")
    print("The long description will default to value of description")
    LONG_DESCRIPTION = DESCRIPTION

setuptools.setup(
    name='dobby',
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Sujith Sudarshan',
    author_email='sh1457@gmail.com',
    python_requires='>=3.10.2',
    url='https://github.com/sh1457/dobby',
    package_dir={'src': ''},
    packages=setuptools.find_packages(where='src'),
    entry_points={
        'console_scripts': ["run=dobby:main"],
    },
    install_requires=[
        "click",
        "requests",
        "numpy",
        "matplotlib",
        "pandas",
        "lxml",
        "html5lib",
        "beautifulsoup4",
    ],
    extras_require={},
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.10.2',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
