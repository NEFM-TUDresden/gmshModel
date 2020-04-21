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

# decide what happens for "from gmshModel import *"
__all__=["Geometry",
         "Model",
         "Visualization",
         "__version__"]

# define default Gmsh configuration changes
DEFAULT_GMSH_CONFIG_CHANGES={
    "General.Terminal": 0,                                                      # deactivate console output by default (only activated for mesh generation)
    "Mesh.CharacteristicLengthExtendFromBoundary": 0,                           # do not calculate mesh sizes from the boundary by default (since mesh sizes are specified by fields)
}
