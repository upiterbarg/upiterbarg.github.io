# encoding: utf-8
from setuptools import setup, find_packages
import os
import sys
import platform

used = sys.version_info
required = (3, 6)

# if version of pip that doesn't understand the python_requires classifier, must be pip >= 9.0.0
# must be built using at least version 24.2.0 of setuptools
# in order for the python_requires argument to be recognized and the appropriate metadata generated
# python -m pip install --upgrade pip setuptools
if used[:2] < required:
    sys.stderr.write(
        "Unsupported Python version: %s.%s. "
        "Python 3.6 or later is required."
        % (sys.version_info.major, sys.version_info.minor)
    )
    sys.exit(1)

short_desc = "A simple utility for telescope time planning, for astronomy hobbyists."


def read_readme(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name)) as f:
        return f.read()


setup(
    name="telescope-planner",
    version=__import__("telescope_planner").__version__,
    description=short_desc,
    author="Victor Domingos",
    packages=find_packages(),
    include_package_data=False,
    long_description=read_readme("README.md"),  # for PyPI
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://no-title.victordomingos.com/projects/telescope-planner/",
    project_urls={
        "Documentation": "https://github.com/victordomingos/telescope-planner/blob/master/README.md",
        "Source": "https://github.com/victordomingos/telescope-planner",
        "Bug Reports": "https://github.com/victordomingos/telescope-planner/issues",
    },
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Operating System :: iOS",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Operating System :: POSIX :: Linux ",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Astronomy",
    ],
    keywords="python3 astronomy telescope planner planning space sky "
    "observation night deepspace solar system stars nebulas planets "
    "galaxies astropy astroplan skyfield NGC Messier Caldwell pyoNGC",
    install_requires=[
        "geocoder==1.38.1",
        "skyfield==1.10",
        "PyOngc==0.3.0",
        "pytz==2018.9",
        "astroplan==0.4",
    ],
    entry_points={
        "console_scripts": ["telescope-planner = telescope_planner.__main__:main"]
    },
)
