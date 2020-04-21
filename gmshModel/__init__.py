################################################################################
#                              __INIT__.PY                                     #
################################################################################
# This function represents the __init__.py for the collection of modules that
# should allow to generate Gmsh models for meshes using the Gmsh-Python-API.

# set version information
from gmshModel._version import __version__

# import modules
from . import (
    Geometry,
    Model,
    Visualization,
)

__all__=["Geometry",
         "Model",
         "Visualization",
         "__version__"]
