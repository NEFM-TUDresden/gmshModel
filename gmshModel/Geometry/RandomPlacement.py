################################################################################
#     CLASS DEFINITIONS FOR PLACEMENT ALGORITHMS FOR RANDOM INCLUSION RVES     #
################################################################################
# Within this file, palcement algorithms for the generation of random inclusion
# distributions are defined. After a generic RandomAlgorithm class, specific
# child classes with different algorithms can be defined here. This allows for
# an increased flexibility in the RandomInclusionRVE class, since different
# algortihms can be used by just loading the corresponding class.

###########################
# Load required libraries #
###########################
# Standard Python libraries
import copy as cp                                                               # copy for deepcopies of arrays
import numpy as np                                                              # numpy for array computations
import logging                                                                  # logging for warning messages
logger=logging.getLogger(__name__)                                              # -> set logger


################################
# Define RandomAlgorithm class #
################################
class RandomAlgorithm:
    """Generic class for placement algorithms of random inclusion distributions

    This class provides the basic properties and methods for random placement
    algorithms. Some of the methods used here are only defined as placeholder
    methods that have to be specified in detail within the child classes.

    Attributes:
    -----------
    inclusionSets: list/array
        array providing the necessary information for sets of inclusions to be
        placed
        -> inclusionSets=[radius, (length), amount] (for the individual sets of inclusions)
        -> length is only required for randomly oriented cylinders

    placementInfo: dict
        number of placed inclusion sets for each type of inclusion
        -> placementInfo = {type: [number of placed inclusions] (for each set)}

    placementOptions: dict
        dictionary providing algorithm-specific placement options

    RVE: object instance
        instance of RandomInclusionRVE to place inclusions for
    """

    #########################
    # Initialization method #
    #########################
    def __init__(self,RVE=None,inclusionSets=None,placementOptions={}):
        """Initialization method of a generic RandomAlgorithm object

        Parameters:
        -----------
        RVE: object instance
            RVE to place inclusions for

        inclusionSets: list/array
            array providing the necessary information for sets of inclusions to be
            placed
            -> inclusionSets=[radius, (length), amount] (for the individual sets of inclusions)
            -> length is only required for randomly oriented cylinders

        placementOptions: dict
            dictionary providing algorithm-specific placement options
        """
        # plausibility checks for input variables
        if RVE is None:
            raise TypeError("No parent RVE object passed. Cannot place random inclusions without information from a parent RVE object. Check your input data.")
        if inclusionSets is None:
            raise TypeError("Variable \"inclusionSets\" not set! To place inclusions using a random algorithm, inclusionSets must be defined. Check your input data.")
        if RVE.inclusionType == "Cylinder" and RVE.inclusionAxis is None:       # inclusion type of parent RVE is cylinder and no global inclusion axis was passed -> random inclusion axis, i.e.: inclusionSets has to contain length information
            if np.shape(inclusionSets)[-1] != 3:                                # inclusionSets has too few columns -> error
                raise ValueError("Wrong amount of elements in variable \"inclusionSets\". To place randomly oriented inclusions of type \"Cylinder\", the cylinder length has to be specified within the \"inclusionSets\" variable. If all inclusion should have the same axis, the \"inclusionAxis\" variable has to be passed to the parent RVE object. Check your input.")

        # update inclusion sets to start placement with biggest inclusions
        inclusionSets=np.atleast_2d(inclusionSets)                              # type conversion for inclusionSets to be matrix-like
        inclusionSets=inclusionSets[inclusionSets[:,0].argsort(axis=0)[::-1]]   # sort inclusionSets (descending) to start algorithm with biggest inclusions

        # save required arguments
        self.RVE=RVE                                                            # save "parent" RVE object
        self.inclusionSets=inclusionSets                                        # save updated inclusionSets array to class object
        self.placementOptions=placementOptions                                  # save placement options

        # initialize required arguments
        self.placementOptions=None                                              # initialize empty list of placement options
        self.placementInfo = {self.RVE.inclusionType: np.zeros_like(self.RVE.inclusionSets[:,0])} # initialize to zero for every set of inclusions and every inclusion type


    ##########################################
    # Placeholder method to place inclusions #
    ##########################################
    def placeInclusions(self,placementOptions={}):
        """Placeholder method for the placement of inclusions"""
        pass


    #############################################
    # Method to update default placementOptions #
    #############################################
    def updatePlacementOptions(self,optionsUpdate):
        """Method to updated the inclusion placement options

        Parameters:
        -----------
        optionsUpdate: dict
            dictionary storing the updates for the currently set placement options
        """
        self.placementOptions.update(optionsUpdate)
        return self.placementOptions



################################################################################

###########################################
# Define RandomSequentialAdsorption class #
###########################################
class RandomSequentialAdsorption(RandomAlgorithm):
    """Based on the generic RandomAlgorithm class, this class implements a simple
    random sequential adsorption algorithm. That means: inclusions are randomly
    generated and checked for admissibility. This procedure is repeated until all
    inclusions have been placed or the maximum amount of attempts is reached.

    Additional Arguments:
    ---------------------
    none
    """
    #########################
    # Initialization method #
    #########################
    def __init__(self,RVE=None,inclusionSets=None,placementOptions={}):
        """Initialization method of a RandomSequentialAdsorption object.

        Parameters:
        -----------
        RVE: object instance
            instance of RandomInclusionRVE to place inclusions for

        inclusionSets: list/array
            array providing the necessary information for sets of inclusions to be
            placed
            -> inclusionSets=[radius, (length), amount] (for the individual sets of inclusions)
            -> length is only required for randomly oriented cylinders

        placementOptions: dict
            dictionary for user updates of the default placement options
        """
        # define default placement options
        defaultPlacementOptions={
            "maxAttempts": 10000,                                               # maximum number of attempts to place one inclusion
            "minRelDistBnd": 0.1,                                               # minimum relative (to inclusion radius) distance to the domain boundaries
            "minRelDistInc": 0.1,                                               # minimum relative (to inclusion radius) distance to other inclusions
        }
        # initialize parent RandomAlgorithm class
        super().__init__(RVE=RVE,inclusionSets=inclusionSets,placementOptions=defaultPlacementOptions)

        # update placementOptions
        self.updatePlacementOptions(placementOptions)


    #############################################################
    # Define method to check distance of inclusions to boundary #
    #############################################################
    def checkDistanceBoundaries(self,incObj,distBnd):
        """Method to decide whether an inclusion object is accepted or rejected
        depending on its distance to the boundaries.

        Parameters:
        -----------
        incObj: object instance
            inclusion object to check distance of other inclusions for

        distBnd: dict
            dictionary containing distances of inclusion object to different
            entities of the boundary
        """
        # get minimum admissible distance to boundaries to avoid problems
        # during mesh generation
        minDistBnd=self.placementOptions["minRelDistBnd"]*incObj.radius

        # assess boundary distances
        acceptInc = True                                                        # initialize flag for acceptance of inclusion to True
        for entittyType, entityDists in distBnd.items():                        # iterate over all boundary entity types
            if np.any(np.linalg.norm(entityDists,axis=1) < minDistBnd):         # check if absolute distance to current boundary entity type is below minimum distance
                acceptInc = False                                               # -> reject inclusion
                break                                                           # -> stop iteration

        # return decision
        return acceptInc


    ##############################################################
    # Method to check distance of inclusions to other inclusions #
    ##############################################################
    def checkDistanceInclusions(self,incObj,distInc):
        """Method to decide whether an inclusion object is accepted or rejected
        depending on its distance to other inclusions.

        Parameters:
        -----------
        incObj: object instance
            inclusion object to check distance of other inclusions for

        distInc: dict
            dictionary containing distances of inclusion object to different
            types of other inclusions
        """
        # get minimum admissible distance to other inclusions to avoid problems
        # during mesh generation
        minDistInc=self.placementOptions["minRelDistInc"]*incObj.radius

        # assess inclusion distances
        acceptInc = True                                                        # initialize flag for acceptance of inclusion to True
        for incType, incDists in distInc.items():                               # iterate over all inclusion object types
            if np.any(np.linalg.norm(incDists,axis=1) < minDistInc):            # check if absolute distance to objects of current inclusion type is below minimum distance
                acceptInc = False                                               # -> reject inclusion
                break                                                           # -> stop iteration

        # return decision
        return acceptInc


    ####################################################
    # Overwrite placeholder method to place inclusions #
    ####################################################
    def placeInclusions(self):
        """Method to implement the random sequential adsorption (RSA) algorithm."""

        # get information from parent RVE object
        RVE=self.RVE                                                            # shortcut for parent RVE object
        incInfo=RVE.inclusionInfo                                               # incInfo dict
        boundary=RVE.domain.boundary                                            # domain boundary information
        if RVE.dimension == 2:                                                  # RVE is 2D
            relBndEnt="Line"                                                    # -> relevant boundary entity for calculation periodic copies are lines
        elif RVE.dimension == 3:                                                # RVE is 3D
            relBndEnt="Plane"                                                   # -> relevant boundary entity for calculation periodic copies are planes

        # get required data from inclusionSets depending on inclusion type
        if RVE.inclusionType in ["Sphere", "Circle"]:                           # spherical/circular inclusions
            rSets, nSets = self.inclusionSets.T                                 # -> get radii and amounts for different inclusion sets
        elif self.RVE.inclusionType == "Cylinder":                              # cylindrical inclusions
            if RVE.inclusionAxis is None:                                       # no global inclusionAxis passed -> inclusionSets must contain cylinder lengths
                rSets, lSets, nSets = self.inclusionSets.T                      # -> get radii, lengths and amounts for different inclusion sets
            else:                                                               # global inclusionAxis passed -> inclusionSets only contains radii and amounts
                rSets, nSets = self.inclusionSets.T                             # -> get radii and amounts for different inclusion sets

        # iterate over all inclusion sets
        for iSet in range(0,np.shape(rSets)[0]):

            # get information for current set
            rSet = rSets[iSet]                                                  # inclusion radius for current set
            nSet = nSets[iSet]                                                  # inclusion amout for current set
            if lSets is None:                                                   # length is not required
                lSet=None                                                       # -> set it to None
            else:                                                               # length is required
                lSet=lSets[iSet]                                                # -> set length of current set

            # try to place all inclusions for the current set
            nAttempts=0                                                         # attempts to place the current inclusion
            placedIncsForSet=0                                                  # amount of placed inclusions for the current set
            while placedIncsForSet < nSet and nAttempts < self.placementOptions["maxAttempts"]:

                # create new inclusion object
                incObj = RVE.generateInclusion(rSet,length=lSet)

                # check distance of inclusion object to boundary entities
                distBnd = RVE.getDistanceBoundaries(incObj,boundary)            # get distance to boundary entities (dict)
                acceptInc = self.checkDistanceBoundaries(incObj,distBnd)        # check distance
                if not acceptInc:                                               # try again, if inclusion is not accepted
                    nAttempts += 1                                              # -> increase number of attempts
                    if nAttempts == self.placementOptions["maxAttempts"]:       # -> print warning if maxAttempts has been reached
                        logger.warning("Could not place all inclusions for the current set. For r={0:.2f}, {1:.0f}/{2:.0f} have been placed.".format(rSet,placedIncsForSet,nSet)")
                    continue

                # get list of required periodic copies of incObj, if necessary
                if np.any(RVE.periodicityFlags == True):                        # check if periodicity is activated
                    incObjs=RVE.getPeriodicCopies(incObj,distBnd[relBndEnt])    # -> get list of periodic copies of inclusion object (including original)

                # check distance to all inclusions placed so far
                if totalInstancesSet > 0:                                       # only check if there are already placed inclusions
                    for obj in incObjs:                                         # check for every copy of current inclusion
                        distIncs = RVE.getDistanceInclusions(obj,incInfo)       # -> get dictionary with distances to all other types of inclusions
                        acceptCopy = self.checkDistanceInclusions(obj,distIncs) # -> check if copy is admissible
                        if not acceptCopy:                                      # -> copy is not accepted
                            acceptInc = False                                   # ->-> inclusion is not accepted
                            break                                               # ->-> stop testing other
                if acceptInc:                                                   # inclusion and copies are accepted
                    RVE.inclusions.append(incObjs)                              # -> append inclusions to list of placed inclusions
                    RVE.updateIncInfo(incObjs,incInfo)                          # -> update incInfo dictionary
                    placedIncsForSet += len(incObjs)                            # -> increase counter for already placed inclusions
                else:                                                           # try again, if inclusion is not accepted
                    nAttempts += 1                                              # -> increase number of attempts
                    if nAttempts == self.placementOptions["maxAttempts"]:       # -> print warning if maxAttempts has been reached
                        logger.warning("Could not place all inclusions for the current set. For r={0:.2f}, {1:.0f}/{2:.0f} have been placed.".format(rSet,placedIncsForSet,nSet)")
                    continue

                # save number of placed inclusions for the current set to placementInfo
                self.placementInfo[incObj.type][iSet]=placedIncsForSet
