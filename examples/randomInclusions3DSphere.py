################################################################################
#              EXAMPLE FOR 3D RANDOMINCLUSION RVE WITH SPHERES                 #
################################################################################
# This example shows the generation of a an RVE with randomly placed, spherical
# inclusions. The basic procedure of the model an mesh generation are pointed
# out and the resulting mesh is visualized. For the example, only the standard
# configuration is used. However, in order to show the available options - all
# user configurations are passed as dictionaries to the individual classes and
# methods - the dictionaries containing the default values are passed. This
# means that, if they were not passed, the resulting mesh would be the same.

# Loading of the RandomInclusionRVE class
# Before the model and mesh generation can start, the required class has to be
# loaded. In this case it is the class RandomInclusionRVE
from ..src.typeRandomInclusionRVE import RandomInclusionRVE


# Initialization of the RVE
# In order to generate a mesh for RVEs with randomly placed inclusions, relevant
# data have to be passed for the initialization of a new object instance. For
# RVEs of the type under consideration, the following parameters are possible:
#
# size: list/array (mandatory)
#   array defining the size of the RVE in the individual directions
#   size=[L_x, L_y, L_z]
#
# inclusionSets: list/array (mandatory)
#   array defining the relevant information (radius and amount) for the individual
#   groups of spherical inclusions to be placed
#   inclusionSets=[[r_1, n_1] [r_2, n_2], ..., [r_n, n_n]]
#
# inclusionType: string (mandatory)
#   string defining the type of inclusions within the RVE
#
# origin: list/array (optional)
#   array defining the origin of the RVE
#   origin=[O_x, O_y, O_z]
#
# periodicityFlags: list/array (optional)
#   array with flags (0/1) whether the current coordinate direction has to be
#   treated as periodic
#   periodicityFlags=[0/1, 0/1, 0/1]
#
# domainGroup: string (optional)
#   string defining which group the geometric objects defining the domain belong
#   to (to reference this group within boolean operations)
#
# inclusionGroup: string (optional)
#   string defining which group the geometric objects defining the inclusions
#   belong to (to reference this group within boolean operations)
#
# gmshConfig: dict (optional)
#   dictionary for user updates of the default Gmsh configuration
#
initParameters={                                                                # save all possible parameters in one dict to facilitate the method call
    "inclusionSets": [1, 10],                                                   # place 10 inclusions with radius 1
    "inclusionType": "Sphere",                                                  # define inclusionType as "Sphere"
    "size": [10, 10, 10],                                                       # set RVE size to [10,10,10]
    "origin": [0, 0, 0],                                                        # set RVE origin to [0,0,0]
    "periodicityFlags": [1, 1, 1],                                              # define all axis directions as periodic
    "domainGroup": "domain",                                                    # use "domain" as name for the domainGroup
    "inclusionGroup": "inclusions",                                             # use "inclusions" as name for the inclusionGroup
    "gmshConfig": {"General.Terminal": 0,                                       # deactivate console output by default (only activated for mesh generation)
                   "General.NumThreads": 1,                                     # use one thrad for the Gmsh-Python-API by default (multithreading only possible if compiled with OPENMP Flag)
                   "Geometry.Tolerance": 1e-08,                                 # geometrical tolerance
                   "Mesh.Binary": 0,                                            # disable generation of binary meshes by default (FEMatlab Code compatability)
                   "Mesh.Format": 10,                                           # set mesh file format to "auto" (determined from file extension)
                   "Mesh.MshFileVersion": 2,                                    # use Gmsh MeshFileVersion 2 by default (FEMatlab Code compatability)
                   "Mesh.Algorithm": 6,                                         # use Frontal-Delauney algorithm for 2D meshing by default
                   "Mesh.Algorithm3D": 1,                                       # use Delauney algorithm for 3D meshing by default
                   "Mesh.CharacteristicLengthExtendFromBoundary": 0,            # do not calculate mesh sizes from the boundary by default (since mesh sizes are specified by fields)
                   "Mesh.CharacteristicLengthFromCurvature": 0,                 # do not calculate mesh sizes from curvature by default (since mesh sizes are specified by fields)
                   "Mesh.CharacteristicLengthFromPoints": 0,                    # do not calculate mesh sizes from points by default
                   "Mesh.CharacteristicLengthMin": 0,                           # do not restrict the minimum mesh size
                   "Mesh.CharacteristicLengthMax": 1e22,                        # do not restrict the maximum mesh size
                   "Mesh.ElementOrder": 1,                                      # use linear elements by default
                   "Mesh.MinimumCirclePoints": 7,                               # define default number of circle points used for calculation of element sizes from curvature
                   "Mesh.MaxNumThreads1D": 1,                                   # use one thrad for 1D meshing by default (multithreading only possible if compiled with OPENMP Flag)
                   "Mesh.MaxNumThreads2D": 1,                                   # use one thrad for 2D meshing by default (multithreading only possible if compiled with OPENMP Flag)
                   "Mesh.MaxNumThreads3D": 1,                                   # use one thrad for 3D meshing by default (multithreading only possible if compiled with OPENMP Flag)
                   "Mesh.OptimizeThreshold": 0.3,                               # optimize mesh until no elements with a Jacobian smaller the 0.3 are found
    }
}
testRVE=RandomInclusionRVE(**initParameters)


# Gmsh model generation
# After all parameters for the RVE are set, the Gmsh model can be generated.
# This process involves the definition of geometric objects, their combination
# to more complex shapes using boolean operations and the definition of physical
# groups, i.e. groups of elements that belong to the same material or part of
# the boundary. For RVEs with randomly placed inclusions, only the placement
# options can be changed by the user. To this end, the possible parameters are:
#
# placementOptions: dict (optional)
#   user updates for the inclusion placement algorithm
modelingParameters={                                                            # save all possible parameters in one dict to facilitate the method call
    "placementOptions": {"maxAttempts": 10000,                                  # maximum number of attempts to place one inclusion
                         "minRelDistBnd": 0.1,                                  # minimum relative (to inclusion radius) distance to the domain boundaries
                         "minRelDistInc": 0.1,                                  # minimum relative (to inclusion radius) distance to other inclusions}
    }
}
testRVE.createGmshModel(**modelingParameters)


# Gmsh mesh creation
# After the model has been created using the Gmsh-Python-API, the meshing
# can be performed. To this end, refinement fields defining the mesh sizes
# within the model have to be calculated and added to the Gmsh model. Once, the
# mesh sizes are specified,the mesh can be generated. Available parameters are:
#
# refinementOptions: dict (optional)
#   dictionary containing user updates for the refinement field calculation
#
meshingParameters={                                                             # save all possible parameters in one dict to facilitate the method call
    "refinementOptions": {"maxMeshSize": "auto",                                # automatically calculate maximum mesh size with built-in method
                          "inclusionRefinement": True,                          # flag to indicate active refinement of inclusions
                          "interInclusionRefinement": True,                     # flag to indicate active refinement of space between inclusions (inter-inclusion refinement)
                          "elementsPerCircumference": 18,                       # use 18 elements per inclusion circumference for inclusion refinement
                          "elementsBetweenInclusions": 3,                       # ensure 3 elements between close inclusions for inter-inclusion refinement
                          "inclusionRefinementWidth": 3,                        # use a relative (to inclusion radius) refinement width of 1 for inclusion refinement
                          "transitionElements": "auto",                         # automatically calculate number of transitioning elements (elements in which tanh function jumps from h_min to h_max) for inter-inclusion refinement
                          "aspectRatio": 1.5                                    # aspect ratio for inter-inclusion refinement: ratio of refinement in inclusion distance and perpendicular directions
    }
}
testRVE.createMesh(**meshingParameters)


# Save resulting mesh to file
# The mesh is generated and can be saved to a file. To this end, only the file
# name - possibly containing a directory and the extension of the wanted mesh
# format - has to be passed. The package supports all mesh file formats that are
# supported by meshio. If no filename is passed, meshes are stored to the current
# directory using the unique model name and the default mesh file format (.msh)
testRVE.saveMesh("randomInclusions3DSphere.msh")


# Show resulting mesh
# To check the generated mesh, the result can also be visualized using built-in
# methods.
testRVE.visualizeMesh()


# Close Gmsh model
# For a proper closing of the Gmsh-Python-API, thAPI has to be finalized. This
# can be achieved by calling the close() method of the model
testRVE.close()
