import re
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

version = re.search(
    r'^__version__\s*=\s*"(.*)"',
    open("py_asciimath/__init__.py").read(),
    re.MULTILINE,
).group(1)

setuptools.setup(
    name="py_asciimath",
    version=version,
    author="Federico Belotti",
    author_email="belo.fede@outlook.com",
    description="A simple converter from ASCIIMath/MathML to LaTeX/MathML",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/belerico/py-asciimath",
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": ["py_asciimath=py_asciimath.py_asciimath:main"]
    },
    test_suite="tests",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=["lark-parser", "docopt", "lxml"],
)
