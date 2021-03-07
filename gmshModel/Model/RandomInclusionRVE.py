################################################################################
#     CLASS FOR INCLUSION RVE MESHES GENERATED USING THE GMSH-PYTHON-API       #
################################################################################
# This file provides a class definition for a generation of RVEs with randomly
# placed inclusions. The class inherits from the InclusionRVE class and extends
# it in order order to specify the remaining placeholder methods of the
# GenericModel. Methods to create the geometry, define refinement information
# and additional information for required boolean operations and physical groups
# are part of the class.

###########################
# Load required libraries #
###########################
# Standard Python libraries
import numpy as np                                                              # numpy for fast array computations
import copy as cp                                                               # copy  for deepcopies
import inspect                                                                  # inspect to search for defined classes in modules

# self defined class definitions and modules
from .InclusionRVE import InclusionRVE                                          # generic RVE class definition (parent class)
from ..Geometry import RandomPlacement                                          # defined algorithms for random placement

###################################
# Define RandomInclusionRVE class #
###################################
class RandomInclusionRVE(InclusionRVE):
    """Class definition for box-shaped RVEs with randomly distributed inclusions

    This class provides required information for box-shaped, RVEs with randomly
    distributed inclusions. It inherits from the InclusionRVE class and extends
    its attributes and methods to handle the inclusion placement as well as the
    definition of required boolean operations and physical groups.

    Additional Attributes:
    ----------------------
    placementAlgorithm: object instance
        instance of the algorithm used for the inclusion placement
    """
    #########################
    # Initialization method #
    #########################
    def __init__(self,size=None,inclusionType=None,inclusionAxis=None,origin=[0,0,0],periodicityFlags=[1,1,1],domainGroup="domain",inclusionGroup="inclusions",gmshConfigChanges={}):
        """Initialization method for RandomInclusionRVE object instances

        Parameters:
        -----------
        size: list/array
            size of the box-shaped RVE model
            -> size=[Lx, Ly, (Lz)]

        inclusionType: string
            string defining the type of inclusion
            -> iunclusionType= "Sphere"/"Cylinder"/"Circle"

        inclusionAxis:list/array
            array defining one global inclusion axis (only relevant for inclusionType "Cylinder")
            -> inclusionAxes=[Ax, Ay, Az]
            -> if not passed globally, inclusionsSets has to contain a "length" information

        origin: list/array
            origin of the box-shaped RVE model
            -> origin=[Ox, Oy, (Oz)]

        periodicityFlags: list/array
            flags indicating the periodic axes of the box-shaped RVE model
            -> periodicityFlags=[0/1, 0/1, 0/1]

        domainGroup: string
            name of the group the RVE domain should belong to

        inclusionGroup: string
            name of the group the inclusions should belong to

        gmshConfigChanges: dict
            dictionary for user updates of the default Gmsh configuration
        """
        # initialize parents classes attributes and methods
        super().__init__(size=size,inclusionType=inclusionType,inclusionAxis=inclusionAxis,origin=origin,periodicityFlags=periodicityFlags,domainGroup=domainGroup,inclusionGroup=inclusionGroup,gmshConfigChanges=gmshConfigChanges)



################################################################################
#                 SPECIFIED/OVERWRITTEN PLACEHOLDER METHODS                    #
################################################################################

    #############################################
    # Method to generate a new inclusion object #
    #############################################
    def generateInclusion(self,radius,length=None):
        """Generate a new inclusion with given radius and, for cylinders, fixed
        axis or random axis of length l."""

        # distinguish different inclusion types
        if self.inclusionType == "Sphere" or self.inclusionType == "Circle":    # inclusion type is Sphere or Circle
            center = self.randomPoint()                                         # -> generate random center point
            incObj =super().generateInclusion(center=center,radius=radius,group=self.inclusionGroup) # -> create new Sphere object
        elif self.inclusionType == "Cylinder":                                  # inclusion type is Cylinder
            base  = self.randomPoint                                            # -> create random base point
            if length is None:                                                  # -> no length passed -> fixed axis for all cylinders
                axis = self.inclusionAxis                                       # ->-> use fixed axis of RVE
            else:                                                               # -> length of cylinder axis passed -> random axis
                axis = self.randomAxis(length)                                  # ->-> create random axis of given length
            incObj = super().generateInclusion(base=base,radius=radius,axis=axis,group=self.inclusionGroup) # -> create new Cylinder object

        # return inclusion object
        return incObj


    ###################################################
    # Method for the definition of boolean operations #
    ###################################################
    def defineBooleanOperations(self):
        """Overwritten method of the GenericModel class to define the required
        boolean operations for the model generation

        Normally, the definition of basic geometric objects is not sufficient
        to generate the RVE geometry. To this end, boolean operations can be
        used to generate more complex RVEs from the basic geometric objects.
        The required boolean operations for the generation of an RVE with
        randomly distributed inclusions is defined here.
        """
        self.booleanOperations=[{                                               # first boolean operation (intersect domain group and inclusions group to get rid of parts that exceed the domain boundary)
            "operation": "intersect",                                           # -> intersection of "domain" and "inclusions"
            "object": self.domainGroup,                                         # -> use "domain" group as object
            "tool": self.inclusionGroup,                                        # -> use "inclusions" group as tool
            "removeObject": False,                                              # -> keep the object ("domain") after the boolean operation for further use
            "removeTool": True,                                                 # -> remove the tool ("inclusions") after the boolean operation
            "resultingGroup": self.inclusionGroup                               # -> assign the result of the boolean operation to the "inclusions" group (i.e. overwrite the group) for further use
        },
        {                                                                       # second boolean operation (cut domain with resulting inclusions to create holes within the domain where the inclusions are placed)
            "operation": "cut",                                                 # -> cut "inclusions" (updated group) from "domain"
            "object": self.domainGroup,                                         # -> use "domain" group as object
            "tool": self.inclusionGroup,                                        # -> use "inclusions" group as tool
            "removeObject": True,                                               # -> remove the object ("domain") after the boolean operation
            "removeTool": False,                                                # -> keep the tool ("inclusions") after the boolean operation for further use
            "resultingGroup": self.domainGroup                                  # -> assign the result of the boolean operation to the "domain" group (i.e. overwrite the group)
        }]


    ################################################
    # Method for the definition of physical groups #
    ################################################
    def definePhysicalGroups(self):
        """Overwritten method of the GenericModel class to define and the
        required physical groups for the model mesh generation

        In order to be able to assign different material properties to different
        regions in the generated mesh, physical groups are used in Gmsh to
        combine different regions into one group. The additional definition of
        a boundary group allows to identify the boundary of the mesh without
        searching for elements on the boundary within the solver.
        """
        # append boundary group to save boundary information in the mesh, too
        self.groups.update({"boundary": self.getBoundaryEntities()})

        # define physical groups
        self.physicalGroups=[{
            "dimension": self.dimension,                                        # define dimension of the physical group
            "group": self.domainGroup,                                          # define name of the physical group
            "physicalNumber": 1                                                 # set physical number of the physical group
        },
        {
            "dimension": self.dimension,                                        # define dimension of the physical group
            "group": self.inclusionGroup,                                       # define name of the physical group
            "physicalNumber": 2                                                 # set physical number of the physical group
        },
        {
            "dimension": self.dimension-1,                                      # define dimension of the physical group
            "group": "boundary",                                                # define name of the physical group
            "physicalNumber": 3,                                                # set physical number of the physical group
        }]


    ##############################
    # Method to place inclusions #
    ##############################
    def placeInclusions(self,inclusionSets=None,algorithm=RandomSequentialAdsorption,placementOptions={}):
        """Place inclusions defined in inclusionSets with a defined algorithm and
        corresponding placementOptions.

        Parameters:
        -----------
        inclusionSets: list/array
            array providing the necessary information for sets of inclusions to be
            placed
            -> inclusionSets=[radius, (length), amount] (for the individual sets of inclusions)
            -> length is only relevant for randomly oriented cylinders

        algorithm: string
            string defining the placement algorithm to use for inclusion placement

        placementOptions: dict
            dictionary for user updates of the default placement options
        """
        # initialize algorithm from defined RandomPlacement algorithms
        placementAlgorithm=self._getPlacementAlgorithm(algorithm,inclusionSets=inclusionSets,placementOptions=placementOptions)

        # place inclusions with chosen placement algorithm
        placementAlgorithm.placeInclusions()



################################################################################
#               ADDITIONAL METHODS FOR THE INCLUSION PLACEMENT                 #
################################################################################

    ############################################
    # Method to determine random cylinder axis #
    ############################################
    def randomAxis(self,l,nAxes=1):
        """Determine nAxes random axes of length l for cylindrical inclusions.
        The calculated angles phi and theta describe rotations around the
        original z- and generated y'-axes, i.e. they correspond to angles of a
        spherical coordinate system with

                phi in [-pi/2, pi/2]  ,
                thetha in [-pi, pi]   .

        Parameters:
        -----------
        l: float
            length of the random cylinder axes to generate

        nAxes: int
            number of random axes to generate
        """
        # get phi and theta for all random axes
        phi, theta=(np.array([0.5, 1])*np.random.uniform(-np.pi,np.pi,(nAxes,2))).T # generate 2 random angles for nAxes axes: phi in [-pi/2, pi/2]; theta in [-pi, pi]

        # determine axis in spherical coordinates
        return (np.array([np.cos(theta)*np.cos(phi), np.cos(theta)*np.sin(phi), np.sin(theta)])*l).T


    ##########################################
    # Method to determine random seed points #
    ##########################################
    def randomPoint(self,nPoints=1):
        """Determine nPoints random points inside the RVE domain. For parallel
        cylinders and circles, account for relevantAxes.

        Parameters:
        -----------
        nPoints: int
            number of random points to generate
        """
        return np.random.rand(nPoints,3)*self.RVE.domain.size*self.relevantAxesFlags+self.RVE.domain.origin


    #######################################################
    # Method to save inclusion information to a text file #
    #######################################################
    def saveIncInfo(self,file):
        """Method to save inclusion information to delimited ascii file

        Parameters:
        -----------
        file: string
            name of the file to save the inclusion information in
        """
        fileDir,fileName,fileExt=self._getFileParts(file,"Misc")                # split fileName into file parts
        with open(fileDir+"/"+fileName+fileExt,"w") as incInfoFile:             # open file
            np.savetxt(incInfoFile,self.inclusionInfo)                          # save information to file



################################################################################
#           ADDITIONAL PRIVATE/HIDDEN METHODS FOR INTERNAL USE ONLY            #
################################################################################

    ######################################################################
    # Method to initialize an object instance of the placement algorithm #
    ######################################################################
    def _getPlacementAlgorithm(self,algName,**algArgs):
        """Internal method to initialize the placement algorithm from a given
        algorithm name and related algorithm arguments.

        Parameters:
        -----------
        algName: string
            required placement algorithm class (as a string)

        algArgs: key-value pairs of arguments
            arguments required to initialize the placement algorithm
        """
        algOK=False                                                             # flag to indicate that passed algorithm string was OK
        for algKey, algClass in inspect.getmembers(RandomPlacement,inspect.isclass): # get all classes from the RandomPlacement module
            if algKey == algName:                                               # check if class key matches the object string that was passed
                algObj = algClass(self,**algArgs)                               # get instance of algorithm class
                algOK=True
        if not algOK:
            raise ValueError("Undefined placement algorithm \"{}\". Check your input.".format(algName))

        return algObj
