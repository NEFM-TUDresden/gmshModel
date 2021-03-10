################################################################################
#     CLASS FOR INCLUSION RVE MESHES GENERATED USING THE GMSH-PYTHON-API       #
################################################################################
# This file provides a class definition for a generation of RVEs with inclusions
# using Python and Gmsh. The class inherits from the GenericRVE class and extends
# it in order order to handle distance and refinement calculations
#
# Currently, the class is restricted to RVEs with rectangular (2D)/ box-shaped
# (3D) domains (explicitly assumed within the setupPeriodicity() method) which
# comprise inclusions that are all of the same type (explicitly assumed by using
# one inclusionInformation array).
###########################
# Load required libraries #
###########################
# Standard Python libraries
import numpy as np                                                              # numpy for array computations
import copy as cp                                                               # copy for deepcopies of arrays

# self-defined class definitions and modules
from .GenericRVE import GenericRVE                                              # generic RVE class definition (parent class)
from ..Geometry import GeometricObjects as geomObj                              # defined geometric objects
from ..Meshing import Refinement as ref                                         # define refinement fields


###########################
# Define GenericRVE class #
###########################
class InclusionRVE(GenericRVE):
    """Generic class for RVEs with inclusions created using the Gmsh-Python-API

    Based on the GenericRVE class, this class provides extra attributes and
    methods that all box-shaped RVEs with inclusions should have: the definition
    of an inclusion information array and relevant inclusion axes allows to
    provide additional methods for distance and refinement field calculations.

    Additional Attributes:
    ----------------------
    inclusionAxis: array
        array defining one global inclusion axis for RVEs with cylinders
        -> can - at the moment - only be parallel to one of the coordinate axes
        -> inclusionAxes=[Ax, Ay, Az]

    inclusionGroup: string
        name of the group the inclusions should belong to

    inclusionInfo: array
        array containing relevant inclusion information (center, radius) for
        distance calculations

    inclusions: list
        list of inclusion objects of the InclusionRVE

    inclusionType: string
        string defining the type of inclusion
        -> inclusionType= "Sphere"/"Cylinder"/"Circle"

    refinementOptions: dict
        dict containing mesh refinement information

    relevantAxesFlags: array
        array with flags (0/1) to indicate axes that are relevant for distance
        calculations and the inclusion placement
    """
    #########################
    # Initialization method #
    #########################
    def __init__(self,size=None,inclusionType=None,inclusionAxis=None,origin=[0,0,0],periodicityFlags=[1,1,1],domainGroup="domain",inclusionGroup="inclusions",gmshConfigChanges={}):
        """Initialization method for InclusionRVE objects

        Parameters:
        -----------
        size: list/array
            size of the box-shaped RVE model
            -> size=[Lx, Ly, (Lz)]

        inclusionType: string
            string defining the type of inclusion
            -> inclusionType= "Sphere"/"Cylinder"/"Circle"

        inclusionAxis:list/array
            array defining one global inclusion axis for RVEs with cylinders
            -> inclusionAxes=[Ax, Ay, Az]

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
        super().__init__(size=size,origin=origin,periodicityFlags=periodicityFlags,domainGroup=domainGroup,gmshConfigChanges=gmshConfigChanges)

        # plausibility checks for additional input variables
        if inclusionType is None:                                               # no inclusion type passed -> error
            raise TypeError("Variable \"inclusionType\" not set! For RVEs with inclusions, the type of inclusions must be defined. Check your input data.")
        if inclusionType == "Cylinder":                                         # inclusion type is cylinder -> further checks
            if inclusionAxis is not None:                                       # inclusion axis passed -> all cylinders will have the same axis; perform additional checks
                if len(np.shape(inclusionAxis)) > 1:                            # check for right amount of array dimensions
                    raise ValueError("Wrong amount of array dimensions for variable \"inclusionAxis\"! For RVEs with cylindrical inclusions, the variable \"inclusionAxis\" can only be one-dimensional. Check your input data.")
                elif len(inclusionAxis) != 3 or np.count_nonzero(inclusionAxis) != 1: # cylinder axis not parallel to one of the coordinate axes -> error
                    raise ValueError("Wrong amount of (non-zero) elements in \"inclusionAxis\"! For RVEs with cylindrical inclusions that are all parallel, the variable \"inclusionAxis\" has to specify the length and direction of the cylinder axis. This cylinder axis has to be parallel to one of the coordinate axes. Check your input.")
                inclusionAxis=np.asarray(inclusionAxis)

        # determine flags for relevant axes to facilitate placement and distance
        # computations for parallel cylinders and circles
        if inclusionType == "Cylinder" and inclusionAxis is not None:           # parallel cylinders
            axes=np.arange(self.dimension)                                      # -> available axes
            relevantAxesFlags=(inclusionAxis==0)*1                              # -> flags (0/1) indicating axes perpendicular to the cylinder axis
        elif self.RVE.inclusionType == "Circle":                                # circles
            relevantAxesFlags=(self.domain.size>0)*1                            # -> axes with non-zero extent are relevant
        else:                                                                   # Spheres and non-parallel cylinders
            relevantAxesFlags=np.ones(self.dimension)                           # -> all axes are relevant

        # save inclusion related information
        self.inclusionAxis=inclusionAxis                                        # save global inclusion axis
        self.inclusionType=inclusionType                                        # save inclusion type
        self.inclusionGroup=inclusionGroup                                      # save inclusion group
        self.relevantAxesFlags=relevantAxesFlags                                # save relevantAxesFlags

        # define default refinement information for setRefinementInformation()
        self.refinementOptions={
            "maxMeshSize": "auto",                                              # automatically calculate maximum mesh size with built-in method
            "inclusionRefinement": True,                                        # flag to indicate active refinement of inclusions
            "interInclusionRefinement": True,                                   # flag to indicate active refinement of space between inclusions (inter-inclusion refinement)
            "elementsPerCircumference": 18,                                     # use 18 elements per inclusion circumference for inclusion refinement
            "elementsBetweenInclusions": 3,                                     # ensure 3 elements between close inclusions for inter-inclusion refinement
            "inclusionRefinementWidth": 3,                                      # use a relative (to inclusion radius) refinement width of 1 for inclusion refinement
            "transitionElements": "auto",                                       # automatically calculate number of transitioning elements (elements in which tanh function jumps from h_min to h_max) for inter-inclusion refinement
            "aspectRatio": 1.5                                                  # aspect ratio for inter-inclusion refinement: ratio of refinement in inclusion distance and perpendicular directions
        }

        # initialize required additional attributes for all inclusionRVEs
        self.inclusions=[]                                                      # initialize empty list of inclusion objects
        self.inclusionInfo=[]                                                   # initialize unset inclusion information array



################################################################################
#                 SPECIFIED/OVERWRITTEN PLACEHOLDER METHODS                    #
################################################################################

    ############################################################################
    # Method to define the required geometric objects for the model generation #
    ############################################################################
    def defineGeometricObjects(self,**options):
        """Overwritten method of the GenericModel class to define and create the
        required geometric objects for the model generation

        Parameters:
        -----------
        options: key-value pairs of options

        """
        # generate geometry
        self.addGeometricObject(self.domain)                                    # add domain object to RVE
        self.placeInclusions(**options)                                         # call inclusion placement routine
        for incObj in self.inclusions:                                          # loop over all inclusions
            self.addGeometricObject(incObj)                                     # add inclusions to calling RVE object


    ####################################################
    # Method for automated refinementfield calculation #
    ####################################################
    def setupRefinementFields(self,refinementOptions={}):
        """Method to calculate and set refinement information for the RVE

        For inclusion-based RVEs, the inclusionInfo variable can be used to
        calculate refinement fields based on the geometric properties of the
        inclusions. These calculations are defined here so that every child
        class of InclusionRVE can use them to calculate refinement fields.

        Parameters:
        -----------
        refinementOptions: dict
            user-defined updates for the default refinement options
        """

        # load default options and update them with passed user options
        self.updateRefinementOptions(refinementOptions)

        # initialize an empty list of relevant fields for MinField calculation
        relevantFieldTags=[]

        # restrict the maximum mesh size (set domain mesh size)
        domainRefinement=self.getDomainRefinementField()                        # get refinement field from subfunction
        relevantFieldTags.append(domainRefinement.tag)                          # append tag of refinement field to list of relevant fields

        # get extended information for inclusion refinements
        inclusionList, inclusionInfo = self.getInclusionInfoForRefinement()

        # perform inclusion refinement, if activated
        if self.refinementOptions["inclusionRefinement"] == True:               # inclusion refinement is activated
            for incObj in inclusionList:                                        # -> iterate over all inclusions in extended list
                incRefinement=self.getInclusionRefinementField(incObj)          # -> create inclusion refinement field
                if incObj.type == "Cylinder":                                   # -> inclusion is a cylinder -> additional restriction fields
                    incRestrictions=self.getCylinderRestrictionFields(incObj,incRefinement) # -> get restriction fields
                    relevantFieldTags.append(incRestrictions[-1].tag)           # -> append tag of final field to list of relevant fields
                else:                                                           # -> inclusion is not a cylinder
                    relevantFieldTags.append(incRefinement.tag)                 # -> append tag of original refinement field to list of relevant fields

        # perform refinement between close inclusions, if activated
        if self.refinementOptions["interInclusionRefinement"] == True:




        self._setMathEvalField("const",self.refinementOptions["maxMeshSize"])


        if self.refinementOptions["interInclusionRefinement"] == True:          # refinement between different inclusions is active
            self.interInclusionRefinement(incInfo)                              # -> perform refinement between inclusions

        # merge all fields within one "Min"-Field
        relevantFields=np.arange(1,len(self.refinementFields)+1)                # start with "1" since Gmsh starts counting with 1
        self.refinementFields.append({"fieldType": "Min", "fieldInfos": {"FieldsList": relevantFields}})

        # set "Min"-Field as background field in Gmsh
        self.backgroundField=len(relevantFields)+1



################################################################################
#                 ADDITIONAL METHODS FOR INCLUSION PLACEMENT                   #
################################################################################

    #############################################
    # Method to generate a new inclusion object #
    #############################################
    def generateInclusion(self,**incData):
        """Generate a new inclusion with given inclusion data"""

        # distinguish different inclusion types
        if self.inclusionType == "Sphere":                                      # inclusion type is Sphere
            incObj = geomObj.Sphere(**incData)                                  # -> create new Sphere object
        elif self.inclusionType == "Circle":                                    # inclusion type is Circle
            incObj = geomObj.Circle(**incData)                                  # -> create new Circle object
        elif self.inclusionType == "Cylinder":                                  # inclusion type is Cylinder
            incObj = geomObj.Cylinder(**incData)                                # -> create new Cylinder object
        else:                                                                   # inclusion type is different
            raise NotImplementedError("Unknown inclusion type. Check your input")

        # return inclusion object
        return incObj


    ######################################################################
    # Method to determine the distance of an inclusion to the boundaries #
    ######################################################################
    def getDistanceBoundaries(self,incObj,boundaryData):
        """Calculate the distance of an inclusion object to the domain boundaries

        Parameters:
        -----------
        incObj: object instance
            inclusion object to calculate boundary distance for

        boundaryData: dict
            dictionary containing relevant information of boundary entities
        """
        # use objects distance calculation capabilities
        distance={}                                                             # initialize empty dictionary of distances to different boundary entity types
        for entityType, entityData in boundaryData.items():                     # iterate over different boundary entity types
            distance[entityType]=incObj.getDistance(entityType,entityData)      # calculate distance to current type

        # return distance dictionary
        return distance


    ########################################################################
    # Method to determine the distance of an inclusion to other inclusions #
    ########################################################################
    def getDistanceInclusions(self,thisIncObj,otherIncData):
        """Calculate the distance of an inclusion object to other inclusions.

        Parameters:
        -----------
        thisIncObj: object instance
            inclusion object to calculate distances to other inclusions for

        otherIncData: dictionary
            relevant data of other inclusion objects
            -> otherIncData={incType: incData}
            -> spheres/circles: incData=[[centers], radii]
            -> cylinders:       incData=[[base points], [axes], radii]
        """
        # use objects distance calculation capabilities
        distance={}                                                             # initialize empty dictionary of distances to different inclusion entity types
        for entityType, entityData in otherIncData.items():                     # iterate over different inclusion entity types
            distance[entityType]=incObj.getDistance(entityType,entityData)      # calculate distance to current type

        # return distance dictionary
        return distance


    #######################################################
    # Method to determine periodic copies of an inclusion #
    #######################################################
    def getPeriodicCopies(self,incObj,distBnd,maxDist=0):
        """Determine where periodic copies of the current inclusion are needed
        and create the corresponding inclusion objects.

        Parameters:
        incObj: object instance
            inclusion object to test for required periodic copies

        distBnd: array
            array containing the shortest distance of this inclusion to the
            highest-dimensional boundary entities

        maxDist: float
            maximum allowed distance to create a periodic inclusion
            -> if set, periodic copies will only be made if 0 < distBnd <= maxDist
               since it is implicitly assumed, that bndDists < 0 have already
               been handled
        """
        # get boundaries to create periodic inclusions for
        if maxDist == 0:
            relBnds = distbnd <= 0
        else:
            relBnds = distBnd > 0 and distBnd < maxDist

        # determine required arrays for periodic copies
        bndNumbers = np.arange(2*self.dimension)[relBnds]                       # numbers of intersected boundaries
        bndNormal = bndNumbers%self.dimension                                   # normals of intersected boundaries -> offset axis for periodic copy
        bndSide = np.floor(bndNumbers/self.dimension)                           # sides of intersected boundaries -> offset sign for periodic copy

        # create periodic copies
        incCopies=[incObj]                                                      # inititalize list of copies for this inclusion object
        offsets=np.eye(3)*self.domain.size                                      # calculate offsets in the individual axis directions
        for ax in bndNormal:                                                    # find all direction for which copies have to be generated
            if self.periodicityFlags[ax]==1:                                    # only create periodic copy if current direction is marked as periodic
                for inc in incCopies:                                           # iterate over all copies of this inclusion
                    objCopy=inc.duplicate()                                     # duplicate the current inclusion
                    objCopy.move((-1)**bndSide[ax]*offsets[ax])                 # move inclusion copy
                    incCopies.append(objCopy)                                   # append copy to list of inclusion copies

        # return list of inclusion object and copies
        return incCopies


    ####################################################
    # Method for the cell-specific inclusion placement #
    ####################################################
    def placeInclusions(self,**options):
        """Placeholder method to place inclusions for the inclusion-based RVE"""
        pass


    ########################################
    # Method to update incInfo  dictionary #
    ########################################
    def updateIncInfo(self,incObjs,incInfo):
        """Update incInfo dictionary with information of inclusion objects
        in incObjs list."""
        for incObj in incObjs:                                                  # iterate over all inclusion objects
            objInfo=incObj.getInfo()                                            # get information for current object
            if incObj.type in incInfo:                                          # there are already information for inclusions of this type
                for i in len(incInfo[obj.type]):                                # -> iterate over all information arrays for this type of inclusion
                    infoArray=incInfo[incObj.type][i]                           # -> get current information array
                    infoArray=np.r_[infoArray, objInfo[i]]                      # -> append object information to array
            else:                                                               # no information for this inclusion type, so far
                incInfo[obj.type]=[*objInfo]                                    # -> save information of current inclusion object



################################################################################
#          ADDITIONAL METHODS FOR REFINEMENT INFORMATION CALCULATION           #
################################################################################

    ############################################################################
    # Method to calculate restrictive MathEval fields for cylinder refinements #
    ############################################################################
    def getCylinderRestrictionFields(self,incObj,fieldObj):
        """Method to define a MathEval refinement field to restrict the
        refinement of cylinders using a hyperbolic tangent function.

        This method defines MathEval refinement fields for cylinders with
        functions of the following type:

            h(x_k)=(hMax+F))/2 +/- (hMax-F)/2*tanh( m*C_3k*( x_k-x0_k ) )  with  k in [0,1,2]

        It represents a restriction of the refinement function F in the cylinder
        axis direction to the length of the cylinder object. This allows to
        prevent an over-refinement in the domain, when the cylinder is not
        defined over its whole length.

        Parameters:
        -----------
        incObj: object instance
            cylinder object to restrict a refinement field for

        fieldObj: object instance
            refinement field object that is restricted
        """
        # get required information from refinement options
        refOpts=self.refinementOptions                                          # shortcut for refinement options
        relRefWidth=refOpts["inclusionRefinementWidth"]                         # relative (to radius) refinement width around spherical inclusions
        hMax=refOpts["maxMeshSize"]                                             # maximum mesh size (far away from sphere boundary)

        # get required information from cylinder object
        offset=relRefWidth*incObj.radius                                        # offset for starting and end points of cylinder center line to account for refinement width
        D=incObj.axis/np.linalg.norm(incObj.axis)                               # director of cylinder center line
        x0=incObj.base-offset*D                                                 # starting point of cylinder center line with offset
        C=incObj.getTransformationMatrix()[2].flatten()                         # transformation coefficients for cylinder axis direction
        x1=incObj.base+incObj.axis+offset*D                                     # end point of cylinder center line with offset
        slope=5.3/offset                                                        # slope of hyperbolic tangent function to manage transition

        # define the refinement field that limits the original refinement at
        # the "beginning" of the cylinder
        minFunctionString="1/2*( (({6})+F{7}) - ( ({6})-F{7} )*Tanh( ({8})*( ({3})*(x-({0}) + ({4})*(y-({1}) + ({5})*(z-({2}) ) ) )".format(*x0,*C,hMax,fieldObj.tag,slope)
        minRestriction=ref.MathEvalField(self,functionString=minFunctionString)
        self.refinementFields.append(minRestriction)

        # restrict the defined field at the "end" of the cylinder
        maxFunctionString="1/2*( (({6})+F{7}) + ( ({6})-F{7} )*Tanh( ({8})*( ({3})*(x-({0}) + ({4})*(y-({1}) + ({5})*(z-({2}) ) ) )".format(*x1,*C,hMax,minRestriction.tag,slope)
        maxRestriction=ref.MathEvalField(self,functionString=maxFunctionString)
        self.refinementFields.append(maxRestriction)

        # return both restriction fields
        return [minRestriction, maxRestriction]


    ####################################################################
    # Method to calculate a constant MathEval field for the RVE domain #
    ####################################################################
    def getDomainRefinementField(self):
        """Define a MathEval field to restrict the maximum mesh size within the
        RVE."""
        # get required information  from refinement options
        hMax=self.refinementOptions["maxMeshSize"]

        # define function string
        refFunction="{0}".format(hMax)

        # set up MathEval refinement field
        refField=ref.MathEvalField(self,functionString=refFunction)             # create new instance of MathEvalField and add it to Gmsh model

        # add refinement field to list of refinement fields of RVE object
        self.refinementFields.append(refField)

        # return field tag
        return refField


    ################################################################
    # Method to get an extended inclusionInfo array for refinement #
    ################################################################
    def getInclusionInfoForRefinement(self,relDistBnd=2):
        """Method to calculate an "extended" inclusionInfo for the refinement
        methods

        In order to ensure a periodicity of not only the geometry but also the
        mesh, the fields defined in the refinement methods, have to be periodic,
        i.e. present on both sides of periodic boundaries. Within this method,
        inclusions that are close to the domain boundaries are copied and stored
        in an "extended" inclusionInfo array that is only used within the
        refinement methods. This ensures that refinement fields that are found
        on one boundary will also be present on its periodic counterpart.

        Parameters:
        -----------
        relDistBnd: int/float
            distance (relative to inclusion radius) for which inclusion is considered
            to be "far" from the boundary if it is exceeded
        """

        # copy data of original inclusions
        extIncList=[]                                                           # initialize empty extended list of inclusions
        extIncInfo={}                                                           # initialize empty extended incInfo dictionary

        # determine highest-dimensional boundary entity
        if self.dimension == 2:                                                 # RVE is 2D
            relBndEnt="Line"                                                    # -> relevant boundary entity for calculation periodic copies are lines
        elif self.dimension == 3:                                               # RVE is 3D
            relBndEnt="Plane"                                                   # -> relevant boundary entity for calculation periodic copies are planes
        axes=self.relevantAxes                                                  # get relevant axes for distance calculations

        # iterate over all original inclusions
        for incObj in self.inclusions:

            # get periodic copies of inclusion object
            # -> only copy in directions, where 0 < distBnd <= radius*relDistBnd
            # -> this avoid duplicate periodic copies
            distBnd = self.getDistanceBoundaries(incObj,self.domain.boundary)
            incObjs = self.getPeriodicCopies(incObj,distBnd[relBndEnt],maxDist=incObj.radius*relDistBnd)

            # append periodic copies to extIncList and save information in extIncInfo
            extIncList.append(incObjs)
            self.updateIncInfo(incObjs,extIncInfo)

        # return extended list of inclusions and their information
        return extIncList, extIncInfo


    ############################################################################
    # Method to calculate "Gaussian" MathEval fields for inclusion refinements #
    ############################################################################
    def getInclusionRefinementField(self,incObj):
        """Method to define a "Gaussian" MathEval refinement field for a
        refinement of the inclusions.

        This method defines MathEval refinement fields with functions of the
        following type:

            Spheres:
            h(x_k)=hMax-(hMax-hMin)*exp( -1/2* (( sqrt( (x_k-x0_k)^2 ) -r0)/(b/4))^2 )  with  k in [1,2,3]

            Circles:
            h(x_k)=hMax-(hMax-hMin)*exp( -1/2* (( sqrt( (x_k-x0_k)^2 ) -r0)/(b/4))^2 )  with  k in [1,2]

            Cylinders with axes in the local x3'-direction:
            h(x_k)=hMax-(hMax-hMin)*exp( -1/2* (( sqrt( C_1k*(x_k-x0_k)^2 + C_2k*(x_k-x0_k)^2 ) -r0)/(b/4))^2 )  with  k in [1,2,3]

        It represents a refinement which decreases the mesh size from hMax to
        hMin if the distance r from the inclusion center/base (x0_1,x0_2,x0_3) is
        close to the value r0. The course of the refinement function resembles a
        normal distribution density function with mean value r0 and standard
        deviation sigma. For convenience, the refinement width (relative to the
        inclusion radius) b is used: since the interval +/-2*sigma covers about
        95% of the values in a normal distribution density function, sigma is
        calculated by b/4.

        Parameters:
        -----------
        incObj: inclusion object instance
            inclusion object to define the refinement field for
        """
        # get required information from refinement options
        refOpts=self.refinementOptions                                          # shortcut for refinement options
        elemsPerCirc=refOpts["elementsPerCircumference"]                        # desired amount of elements per sphere circumference
        relRefWidth=refOpts["inclusionRefinementWidth"]                         # relative (to radius) refinement width around spherical inclusions
        hMax=refOpts["maxMeshSize"]                                             # maximum mesh size (far away from sphere boundary)

        # calculate meshing parameters using incObj information
        hMin=2*np.pi*incObj.radius/elemsPerCirc
        b=relRefWidth*incObj.radius

        # setup MathEval refinement field functions depending on object type
        if incObj.type == "Sphere":                                             # inclusion object of type "Sphere"
            functionString="{4}-({4}-({5}))*Exp(-1/2*(((Sqrt((x-({0}))^2+(y-({1}))^2+(z-({2}))^2)-({3}))/({6}))^2)".format(*incObj.center,incObj.radius,hMax,hMin,b/4)
        elif incObj.type == "Circle":                                           # inclusion object of type "Circle"
            functionString="{4}-({4}-({5}))*Exp(-1/2*(((Sqrt((x-({0}))^2+(y-({1}))^2)^2)-({3}))/({6}))^2)".format(*incObj.center[0:2],incObj.radius,hMax,hMin,b/4)
        elif incObj.type == "Cylinder":                                         # inclusion object of type "Cylinder"
            C=incObj.getTransformationMatrix()                                  # -> get transformation matrix from global x_k to local x'_l system
            Cperp=C[0:2].flatten()                                              # -> transformation coefficients for directions perpendicular to cylinder axis
            functionString="{10}-({10}-({11}))*Exp(-1/2*(((Sqrt( ({3})*(x-({0}))^2+({4})*(y-({1}))^2+({5})*(z-({2}))^2 + ({6})*(x-({0}))^2+({7})*(y-({1}))^2+({8})*(z-({2}))^2) )-({9}))/({12}))^2)".format(*self.base,*Cperp,self.radius,hMax,hMin,b)

        # create refinement field and return it
        refField=ref.MathEvalField(self,functionString=functionString)
        return refField


    #######################################################################################
    # Method to calculate "Tanh" MathEval fields for refinements between close inclusions #
    #######################################################################################
    def getMinDistRefinementFields(self,distVec):
        pass


    ###################################################
    # Method to perform refinement between inclusions #
    ###################################################
    def interInclusionRefinement(self,incInfo):
        """Method to perform refinement between inclusions

        Within this method, the gap between close inclusions is refined using
        a tanh-function. This method ensures that the space between inclusions
        comprises the user-defined amount of elements. The applied refinement
        function of type "tanh" is described in the function definition of
        "_tanhRefinement()".

        Parameters:
        -----------
        incInfo: array
            extended inclusionInfo array containing information on inclusions
            within the RVE model as well as outside but close to the model
            boundaries
        """
        # get required refinement options
        refinementOptions=self.refinementOptions
        nElemsBetween=refinementOptions["elementsBetweenInclusions"]            # number of elements between inclusion combinations that are considered "close"
        transitionElements=refinementOptions["transitionElements"]              # number of transitioning elements for the continuous jump to go from h_min to h_max
        aspectRatio=refinementOptions["aspectRatio"]                            # aspect ratio of inclusion distance and perpendicular directions
        maxMeshSize=refinementOptions["maxMeshSize"]
        if transitionElements=="auto":                                          # number of transitioning elements is set to "auto"
            transitionElements=nElemsBetween                                    # -> use number of elements between inclusions as default/automatically calculated value
        if refinementOptions["inclusionRefinement"]==True:                      # refinement of inclusions is active and has already been performed
            minMeshSizes=2*np.pi*incInfo[:,[3]]/refinementOptions["elementsPerCircumference"] # -> calculate minimum mesh sizes for the individual inclusions
        else:                                                                   # refinement of inclusions is not active
            minMeshSizes=refinementOptions["maxMeshSize"]*np.ones((np.shape(incInfo)[0],1)) # -> set minimum mesh size for each inclusion to maxMeshSize

        # get relevant axes for distance calculations
        axes=self.relevantAxes

        # loop over all inclusions
        for iInc in range(0,np.shape(incInfo)[0]):

            thisInc=incInfo[iInc,:]                                             # inclusion information for the inclusion under consideration
            otherIncs=incInfo[iInc+1:,:]                                        # inclusion information of other inclusions (prevent double placement of refinement information by only considering inclusion combinations that have not been considered so far)

            # check distance to all remaining other inclusions
            distIncs=self._getDistanceVector(thisInc,otherIncs,axes=axes)       # get center-center distance vectors (per direction) to other inclusions
            normDistIncs=np.linalg.norm(distIncs,axis=1,keepdims=True)          # get norm of center-center distance vectors
            normDistIncBnds=normDistIncs-otherIncs[:,[3]]-thisInc[3]            # get norm of boundary-boundary distance vectors

            # decide which inclusion combinations have to be refined
            # -> Here, the maximum of the minimum mesh densities of the current
            # -> inclusion combinations is used to check whether - with this
            # -> mesh density (plus safety coefficient) - the required amount
            # -> of elements between the inclusions can be ensured
            incsForRefinement=np.array(np.where( (normDistIncBnds.flatten()<=1.1*nElemsBetween*np.maximum(minMeshSizes[iInc,[0]],minMeshSizes[iInc+1:,[0]]).flatten()) & (normDistIncBnds.flatten() > 0) ))

            # loop over all inclusion combinations that have to be refined
            for iRefine in incsForRefinement.flatten():
                refineCenter=thisInc[axes]+0.5*distIncs[iRefine,:]              # get center of refinement (half the distance between the inclusions)
                meshSize=normDistIncBnds[iRefine]/nElemsBetween                 # get required mesh size (distance diveded by required amount of elements)
                refineWidth=normDistIncBnds[iRefine]/2+transitionElements/2*meshSize # get refinement width, i.e. offset of tanh-function to jump from minimum to maximum value (allow coarsening within "transitionElems" elements)
                C=self._getTransformationMatrix(distIncs[iRefine,:],axes)      # get transformation matrix to rotated system between inclusions under consideration

                # set refinement field
                self._setMathEvalField("tanh",np.r_[C.reshape(C.size),refineCenter,refineWidth,maxMeshSize,meshSize,5.3/(nElemsBetween*meshSize),aspectRatio])


    #######################################
    # Method to update refinement options #
    #######################################
    def updateRefinementOptions(self,optionsUpdate):
        """Method to update refinement options

        Parameters:
        -----------
        optionsUpdate: dict
            dictionary containing user updates of the set refinement options
        """
        self.refinementOptions.update(optionsUpdate)                            # update refinement options
        if self.refinementOptions["maxMeshSize"] is "auto":                     # check if "maxMeshSize" is set to "auto"
            self.refinementOptions["maxMeshSize"]=self._calculateMaxMeshSize()  # -> calculate "maxMeshSize" with internal function



################################################################################
#           ADDITIONAL PRIVATE/HIDDEN METHODS FOR INTERNAL USE ONLY            #
################################################################################

    ####################################################################
    # Method to automatically calculate a reasonable maximum mesh size #
    ####################################################################
    def _calculateMaxMeshSize(self):
        """Internal method to calculate the maximum mesh size"""
        if self.domain.size is None:                                            # RVE size has not been set
            return self.getGmshOption("Mesh.CharacteristicLengthMax")           # -> use Gmsh default setting of maximum mesh size
        else:                                                                   # RVE size is set
            return np.amax(self.domain.size)/10                                 # -> ensure at least 10 elements along the longest edge of the RVE


    ############################################################################
    # Method to get transformation matrix into local system between inclusions #
    ############################################################################
    def _getTransformationMatrix(self,d,axes):
        """Internal method to calculate transformation from global x-y-z coordinate
        system to rotated local system between two inclusions

        Parameters:
        -----------
        d: array
            distance vector between the two inclusions

        axes: array
            axes to check the distance for
        """

        # distinguish 2- and 3-dimensional problems
        if len(axes)==2:                                                        # 2D cylindrical transformation -> rotate system in relevant plane without touching 3rd axis
            phi=np.arctan2(d[1],d[0])                                           # get angle in relevant plane
            C=np.array([[np.cos(phi), np.sin(phi)],[-np.sin(phi), np.cos(phi)]])# get transformation matrix according to cylindrical coordinate transformation

        elif len(axes)==3:                                                      # 3D spherical transformation -> rotate in 2 direction and place rotate x-axis in inclusion distance direction
            phi = np.arctan2(d[1], d[0])                                        # get angle of projected distance vector in original x-y-plane
            theta = np.arctan2(np.sqrt(d[0]**2 + d[1]**2), d[2])                # get 2nd inclination angle towards original x-y-plane
            C=np.array([[np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta)], # get transformation matrix according to spherical coordinate transformation
                        [np.cos(theta)*np.cos(phi), np.cos(theta)*np.sin(phi), -np.sin(theta)],
                        [-np.sin(phi), np.cos(phi), 0]])

        # return transformation matrix
        return C


    #############################################################################
    # Method to calculate "Tanh" MathEval fields for inter-inclusion refinement #
    #############################################################################
    def _tanhRefinement(self,data):
        """Internal method to set "Tanh" refinement fields

        This method defines refinement functions of the following type:

            Spheres:
            h(x1,x2,x3)=(h_max+h_min)/2 + (h_max-h_min)/2* tanh( m*( ( sqrt( ( C_1k*(xk-x_k0) )^2 ) + aspect^2*( C_2k*(xk-x_k0) )^2 + epsilon^2*( C_3k*(xk-x_k0) )^2 ) -r0) )

            Cylinders/Disks:
            h(x1,x2)=(h_max+h_min)/2 + (h_max-h_min)/2* tanh( m*( ( sqrt( ( C_1k*(xk-x_k0) )^2 ) + aspect^2*( C_2k*(xk-x_k0) )^2 ) -r0) )

        It represents a refinement within the matrix between close inclusions
        which tries to ensure the requested amount of elements and performs a
        "continuous" jump from h_min to h_max, when the distance from the origin
        (x1_0,x2_0,x3_0) reaches the value r0. To allow for different refinement
        widths in the inclusion distance and perpendicular directions, the local
        x1'-x2'-x3'-system is formulated in terms of the global x1-x2-x3 system
        by means of the transformation matrix C_kl. The local x1-axis always points
        in the inclusion distance direction - the downrating of the perpendicular
        axis is performed using the variable aspect. Finally, the width of the
        "jump" is controlled via the initial slope m.

        Parameters:
        -----------
        data: array
            array containing all parameters for the refinement
            -> data=[C_11, C_12, (C_13), C_21, C_22, (C_23), (C_31), (C_32), (C_33), x1_0, x2_0, (x3_0), r0, h_max, h_min, m, aspect]
        """
        if len(self.relevantAxes)==2:
            axesString=["x", "y", "z"]
            refineFunction="({9}+({10}))/2+({9}-({10}))/2*Tanh((Sqrt((({2})*({0}-({6}))+({3})*({1}-({7})))^2+({12})^2*(({4})*({0}-({6}))+({5})*({1}-({7})))^2)-({8}))*({11}))".format(*[axesString[ax] for ax in self.relevantAxes[:]],*data)
        elif len(self.relevantAxes)==3:
            refineFunction="({13}+({14}))/2+({13}-({14}))/2*Tanh((Sqrt((({0})*(x-({9}))+({1})*(y-({10}))+({2})*(z-({11})))^2+({16})^2*(({3})*(x-({9}))+({4})*(y-({10}))+({5})*(z-({11})))^2+({16})^2*(({6})*(x-({9}))+({7})*(y-({10}))+({8})*(z-({11})))^2)-({12}))*({15}))".format(*data)

        return refineFunction
