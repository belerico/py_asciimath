import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_asciimath",  # Replace with your own username
    version="0.0.3",
    author="Federico Belotti",
    author_email="belo.fede@outlook.com",
    description="A simple converter from ASCIIMath to LaTeX",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/belerico/py-asciimath",
    packages=["py_asciimath", "tests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=["lark-parser"],
    python_requires=">=3.6",
)
