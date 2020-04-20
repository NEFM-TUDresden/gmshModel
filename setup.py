import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gmshModel",
    version="1.0.0",
    author="PhilippMetsch",
    author_email="philipp.metsch@tu-dresden.de",
    description="A mesh modeling interface to the Gmsh-Python-API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering",
    ],
    python_requires='>=3.5',
)
