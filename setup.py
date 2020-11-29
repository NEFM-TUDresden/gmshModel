import setuptools
import os

# get required information from package
packageName="gmshModel"                                                         # name of the package
filePath=os.path.dirname(__file__)                                              # path of this file

# get version
versionFile=os.path.join(filePath,packageName,"_version.py")                    # version file
with open(versionFile,"r") as fileHandle:                                       # open version file
    exec(fileHandle.read())                                                     # -> get version number

# get package description
readmeFile=os.path.join(filePath,packageName,"README.rst")                      # README file
with open("README.rst", "r") as fileHandle:                                     # open README file
    readmeInfo = fileHandle.read()                                              # -> get README information

# set install_requires
installRequires=["numpy",
                 "gmsh",
                 "meshio>=4",
                 "pyvista>=0.24.1"]


# setup
setuptools.setup(
    name=packageName,
    version=__version__,
    author="Philipp Metsch",
    author_email="philipp.metsch@tu-dresden.de",
    url='https://github.com/NEFM-TUDresden/GmshModel',
    project_urls={
        "Code": "https://github.com/NEFM-TUDresden/GmshModel",
        "Issues": "https://github.com/NEFM-TUDresden/GmshModel/issues",
        "Documentation": "https://gmshmodel.readthedocs.io/en/latest/",
    },
    description="A mesh modeling interface to the Gmsh-Python-API",
    long_description=readmeInfo,
    long_description_content_type="text/x-rst",
    classifiers=["Development Status :: 5 - Production/Stable",
                 "Intended Audience :: Developers",
                 "Intended Audience :: Science/Research",
                 "Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 3.5",
                 "Programming Language :: Python :: 3.6",
                 "Programming Language :: Python :: 3.7",
                 "Programming Language :: Python :: 3.8",
                 "Programming Language :: Python :: 3.9",
                 "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
                 "Topic :: Scientific/Engineering",
                 "Topic :: Utilities"],
    keywords="Gmsh mesh preprocessing",
    packages=setuptools.find_packages(),
    python_requires='>=3.5',
    install_requires=installRequires,
)
