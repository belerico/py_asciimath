import setuptools

from py_asciimath import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_asciimath",
    version=__version__,
    author="Federico Belotti",
    author_email="belo.fede@outlook.com",
    description="A simple converter from ASCIIMath to LaTeX",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/belerico/py-asciimath",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": ["py_asciimath = py_asciimath.__main__:main"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=["lark-parser", "docopt"],
    python_requires=">=3.6",
)
