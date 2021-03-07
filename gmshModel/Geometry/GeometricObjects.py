################################################################################
#       CLASS DEFINITIONS OF GEOMETRIC OBJECTS USED WITHIN THE RVE CLASS       #
################################################################################
# Within this file, classes for different geometric objects used in the GmshModel
# are defined. The geometric objects are used within the geometry generation to
# create Gmsh model from basic geometry entities.

###########################
# Load required libraries #
###########################
# Standard Python libraries
import numpy as np                                                              # numpy for fast array computations
import copy as cp                                                               # copy for deepcopies of objects

# self defined class definitions and modules
from DistanceCalculations import *                                              # methods for distance calculations of geometric objects

################################################################################
#                       Define generic GeometricObject                         #
################################################################################
# This class provides general properties that all geometrical objects within the
# RVE will have. Its child-classes inherit those properties and provide additional,
# more specific properties.
class GeometricObject:
    """Definition of a generic geometric object

    This class is the parent class of all geometric objects and provides general
    information that all objects should have

    Attributes:
    -----------
    dimension: int
        dimension of the RVE

    group: string
        string defining which group the geometric object belongs to

    type: string
        type of GeometricObject
    """
    #########################
    # Initialization method #
    #########################
    def __init__(self,dimension=None,group="default"):
        """Initialization method for geometric objects

        Parameters:
        ----------
        dimension: int
            dimension of the geometric object

        group: string
            group the geometric object belongs to
        """
        # error checking for dimension
        if dimension is None:
            raise TypeError("Variable \"dimension\" not defined. For a geometric object of type {}, the dimension must be specified. Check your input data.".format(self.__class__))

        # initialize relevant variables
        self.type=type(self).__name__                                           # set type of geometric object
        self.dimension=dimension                                                # dimension of the geometrical object
        self.group=group                                                        # group tag of the geometrical object (to distinguish different groups of objects)
        self._copies=[]                                                         # initialize empty list of object copies
        self._parentObj=None                                                    # initialize parent object to None


    ################################################################
    # Method to add the geometric object to a specified Gmsh model #
    ################################################################
    def addToGmshModel(self,gmshModel):
        """Add a representation of the geometric object to the Gmsh model

        Parameters:
        -----------
        gmshModel: class object
            model class of the Gmsh-Python-API that holds the Gmsh-specific
            current model information
        """
        return (self.dimension,self._getGmshRepresentation(gmshModel))


    ########################################
    # Method to duplicate geometric object #
    ########################################
    def duplicate(self):
        """Generate a duplicate of the geometric object and manage handling of
        copies and parent objects"""

        # create copy
        objCopy=cp.deepcopy(self)                                               # create deecopy of object

        # update list of copies and parent objects for the copies
        if self._parentObj is None:                                             # object has no parent object
            objCopy._parentObj=self                                             # -> set this object as the copies parent
            self._copies.append(objCopy)                                        # -> add copy to list of object copies
        else:                                                                   # object is a copy of another object
            objCopy._parentObj=self._parentObj                                  # -> set this objects parents as the copies parent
            self._parentObj._copies.append(objCopy)                             # update parents list of object copies

        # return copied object
        return objCopy


    ########################################################################
    # Placeholder method to calculate distances to other geometric objects #
    ########################################################################
    def getDistance(self,objType,objData):
        """Placeholder method to be specified by child classes in order to
        calculate the distance of other objects of type objType with data
        objData to this object."""
        pass


    #####################################################
    # Placeholder method to return an object info array #
    #####################################################
    def getInfoArray(self):
        """Placeholder method to return an object-specific info array.
        """
        pass


    ################################################
    # Placeholder method to move geometric objects #
    ################################################
    def move(self,offset):
        """Placeholder method to be specified by child classes in order to apply
        changes of the corresponding objects attributes that are caused by a
        movement."""
        pass


    ############################################################################
    # Internal placeholder method to determine the objects Gmsh representation #
    ############################################################################
    def _getGmshRepresentation(self,gmshModel):
        """Placeholder method to be specified by child classes in order to return
        the correct Gmsh representation of the geometric object under investigation
        """
        pass



################################################################################
#                Define Box as a child of GeometricObject                      #
################################################################################
# This class provides more specified attributes and methods for geometrical
# objects of type "Box". It inherits basic properties from its parent class
# "GeometricObject".
class Box(GeometricObject):
    """Definition of a Box object

    This class is a child class of geometricObject and provides additional
    information for objetcs of type Box

    Additional Attributes:
    ----------------------
    boundary: dict
        dictionary of planes E, lines L and points P defining the boundary of
        the box object (in a parameterized form)
        -> boundary={"Plane": [Q_i], [R1_i], [R2_i]],
                     "Line": [A_j], [D_j],
                     "Point": [P_k]}
        -> E_i(u,v) = Q_i+R1_i*u+R2_i*v  with u,v in [0,1]
        -> L_j(t) = A_j + D_j*t

    origin: array/list
        origin of the box object
        -> origin=[Ox, Oy, Oz]

    size: array/list
        size of the box object
        -> size=[Lx, Ly, Lz]
    """


    ##########################
    # Initialization method  #
    ##########################
    def __init__(self,size=None,origin=[0,0,0],group="default"):
        """Initialization method for Box objects

        Parameters:
        -----------
        size: array/list
            size of the box object -> size=[Lx, Ly, Lz]

        origin: array/list
            origin of the box object -> origin=[Ox, Oy, Oz]

        group: string
            group the box object belongs to
        """

        # initialize parent classes attributes and methods
        super().__init__(dimension=3,group=group)

        # plausibility checks for input variables:
        for varName, varValue in {"size": size, "origin": origin}.items():
            if varValue is None:                                                # check if variable has a value
                raise TypeError("Variable \"{0}\" not set! For a geometric object of type \"{1}\", the {0} must be specified. Check your input data.".format(varName,self.__class__))
            elif len(np.shape(varValue)) > 1:                                   # check for right amount of array dimensions
                raise ValueError("Wrong amount of array dimensions for variable \"{0}\"! For a geometric object of type \"{1}\", the variable \"{0}\" can only be one-dimensional. Check your input data.".format(varName,self.__class__))
            elif len(varValue) != 3:                                            # check for right amount of values
                raise ValueError("Wrong number of (non-zero) values for variable \"{0}\"! For a geometric object of type \"{1}\", the variable \"{0}\" has to have 3 values. Check your input data.".format(varName,self.__class__))
            elif varName is "size" and np.count_nonzero(varValue) != 3:         # check for right amount of non-zero values (size only)
                raise ValueError("Wrong number of non-zero values for variable \"{0}\"! For a geometric object of type \"{1}\", the variable \"{0}\" has to have 3 non-zero values. Check your input data.".format(varName,self.__class__))

        # set object attributes
        self.origin=np.asarray(origin)                                          # set origin of the box object
        self.size=np.asarray(size)                                              # set size of the box object
        self.boundary=self.getBoundary()                                        # set boundary informatiomn of the box object


    ##############################
    # Method to get box boundary #
    ##############################
    def getBoundary(self):
        """Determine a dictionary with all of the boxes boundary entities. The
        ordering of the entities with the highest dimension (here: planes) is
        according to their normal directions [-x, -y, -z, x, y, z]. This allows
        for an easy identification of boundary sides and directions.
        """
        # get required information
        axDirs = np.eye(3)*self.size                                            # directors in the individual axes directions

        # determine 8 vertices
        V1=self.origin                                                          # origin of planes on negative side of boundary
        V2, V3, V4 = V1 + axDirs                                                # remaining vertices reachable from V1
        V5=self.origin + self.size                                              # origin of planes on positive side of boundary
        V6, V7, V8 = V5 - axDirs                                                # remaining vertices reachable from V5

        # determine 12 line origins and directors
        A=np.array([V1, V1, V1, V5, V5, V5, V6, V6, V7, V7, V8, V8])            # line starting points
        D=np.array([*axDirs, *-axDirs, -axDirs[1], -axDirs[2], -axDirs[0], -axDirs[2], -axDirs[0], -axDirs[1]]) # corresponding line directors

        # determine 6 plane origins and directors in 2 perpendicular directions
        Q=np.array([V1, V1, V1, V5, V5, V5])                                    # plane origins
        R1=np.array([axDirs[1], axDirs[2], axDirs[0], -axDirs[1], -axDirs[2], -axDirs[0]]) # plane directors in u direction
        R2=np.array([axDirs[2], axDirs[0], axDirs[1], -axDirs[2], -axDirs[0], -axDirs[1]]) # plane directors in v-direction

        # determine dictionary of boundary entitites
        boundary={"Plane": [Q, R1, R2],
                  "Line": [A,D],
                  "Point": np.r_[V1, V2, V3, V4, V5, V6, V7, V8]
        }

        # return boundary dict
        return boundary


    #####################################################
    # Overwrite placeholder method to return info array #
    #####################################################
    def getInfoArray(self):
        """Return a Numpy array that contains the box size and origin."""
        return np.r_[self.size, self.origin]


    ###################################################
    # Overwrite placeholder method to move Box object #
    ###################################################
    def move(self,offset):
        """Move the box, i.e. its origin, to its new place"""
        self.origin = self.origin+np.asarray(offset)


    ################################################################
    # Internal method to determine the objects Gmsh representation #
    ################################################################
    def _getGmshRepresentation(self,gmshModel):
        """Return a Gmsh OCC entity of type Box"""
        return gmshModel.occ.addBox(*np.r_[self.origin, self.size])



################################################################################
#               Define Rectangle as a child of GeometricObject                 #
################################################################################
# This class provides more specified attributes and methods for geometrical
# objects of type "Rectangle". It inherits basic properties from its parent
# class "GeometricObject".
class Rectangle(GeometricObject):
    """Definition of a Rectangle object

    This class is a child class of geometricObject and provides additional
    information for objetcs of type Rectangle.

    Additional Attributes:
    ----------------------
    boundary: dict
        dictionary of lines L and points P defining the boundary of the
        rectangle object (in a parameterized form)
        -> boundary={"Line": [A_j], [D_j],
                     "Point": [P_k]}
        -> L_j(t) = A_j + D_j*t

    origin: array/list
        origin of the box object
        -> origin=[Ox, Oy, Oz]

    size: array/list
        size of the box object
        -> size=[Lx, Ly, Lz]
    """
    ##########################
    # Initialization method  #
    ##########################
    def __init__(self,size=None,origin=[0,0,0],group="default"):
        """Initialization method for Rectangle objects

        Parameters:
        -----------
        size: array/list
            size of the rectangle object -> size=[Lx, Ly, (Lz)]

        origin: array/list
            origin of the rectangle object -> origin=[Ox, Oy, (Oz)]

        group: string
            group the rectangle object belongs to
        """

        # initialize parent classes attributes and methods
        super().__init__(dimension=2,group=group)

        # plausibility checks for input variables:
        for varName, varValue in {"size": size, "origin": origin}.items():
            if varValue is None:                                                # check if variable has a value
                raise TypeError("Variable \"{0}\" not set! For a geometric object of type \"{1}\", the {0} must be specified. Check your input data.".format(varName,self.__class__))
            elif len(np.shape(varValue)) > 1:                                   # check for right amount of array dimensions
                raise ValueError("Wrong amount of array dimensions for variable \"{0}\"! For a geometric object of type \"{1}\", the variable \"{0}\" can only be one-dimensional. Check your input data.".format(varName,self.__class__))
            elif not len(varValue) in [2,3]:                                    # check for right amount of values
                raise ValueError("Wrong number of (non-zero) values for variable \"{0}\"! For a geometric object of type \"{1}\", the variable \"{0}\" has to have 2 or 3 values. Check your input data.".format(varName,self.__class__))
            elif varName is "size" and np.count_nonzero(varValue) != 2:         # check for right amount of non-zero values (size only)
                raise ValueError("Wrong number of non-zero values for variable \"{0}\"! For a geometric object of type \"{1}\", the variable \"{0}\" has to have 2 non-zero values. Check your input data.".format(varName,self.__class__))

        # Correct potentially two-dimensional arrays
        if len(size) != 3:                                                      # check if size is not a three-dimensional array
            size=np.r_[size,0]                                                  # -> append 0
        if len(origin) != 3:                                                    # check if origin is not a three-dimensional array
            newOrigin=np.zeros(3)                                               # -> create new three-dimensional array
            newOrigin[size != 0]=origin                                         # -> assign values of origin to non-zero dimensions of new array
            origin=newOrigin                                                    # -> overwrite origin with new array

        # set object attributes
        self.origin=np.asarray(origin)                                          # set origin of the rectangle object
        self.size=np.asarray(size)                                              # set size of the rectangle object
        self.boundary=self.getBoundary()                                        # set boundary information of the rectangle object


    ####################################
    # Method to get rectangle boundary #
    ####################################
    def getBoundary(self):
        """Determine a dictionary with all of the rectangles boundary entities.
        The ordering of the entities with the highest dimension (here: lines) is
        according to their normal directions [-x, -y, x, y]. This allows
        for an easy identification of boundary sides and directions."""

        # get required information
        axDirs = np.eye(3)*self.size                                            # directors in the individual axes directions
        axDirs = axDirs[0:self.dimension]                                       # take only first two directors, since rectangles are supposed to be in the x-y-plane

        # determine 4 vertices
        V1=self.origin                                                          # origin of planes on negative side of boundary
        V2, V3 = V1 + axDirs                                                    # remaining vertices reachable from V1
        V4=self.origin + self.size                                              # origin of planes on positive side of boundary

        # determine 4 line origins and directors
        A=np.array([V1, V1, V4, V4])                                            # line starting points
        D=np.array([*axDirs, *-axDirs])                                         # corresponding line directors

        # determine dictionary of boundary entities
        boundary={"Line": [A,D],
                  "Point": np.r_[V1, V2, V3, V4]
        }

        # retrun boundary dict
        return boundary


    #####################################################
    # Overwrite placeholder method to return info array #
    #####################################################
    def getInfoArray(self):
        """Return a Numpy array that contains the rectangle size and origin."""
        return np.r_[self.size, self.origin]


    #########################################################
    # Overwrite placeholder method to move Rectangle object #
    #########################################################
    def move(self,offset):
        """Move the rectangle, i.e. its origin, to its new place"""
        self.origin = self.origin+np.asarray(offset)


    ################################################################
    # Internal method to determine the objects Gmsh representation #
    ################################################################
    def _getGmshRepresentation(self,gmshModel):
        """Return a Gmsh entity of type Rectangle"""
        return gmshModel.occ.addRectangle(*np.r_[self.origin, self.size[0:self.dimension]])



################################################################################
#                 Define Sphere as child of GeometricObject                    #
################################################################################
# This class provides more specified attributes and methods for geometrical
# objects of type "Sphere". It inherits basic properties from its parent class
# "GeometricObject".
class Sphere(GeometricObject):
    """Definition of a Sphere object

    This class is a child class of geometricObject and provides additional
    information for objetcs of type Sphere

    Additional Attributes:
    ----------------------
    center: array/list
        array that defines the center of the Sphere object
        -> center=[Cx, Cy, (Cz)]

    radius: float
        radius of the Sphere object
    """
    #########################
    # Initialization method #
    #########################
    def __init__(self,center=None,radius=None,group="default"):
        """Initialization method for Sphere objects

        Parameters:
        -----------
        center: array/list
            center of the Sphere object -> center=[Cx, Cy, Cz]

        radius: float
            radius of the Sphere object

        group: string
            group the Sphere object belongs to
        """

        # initialize parent classes attributes and methods
        super().__init__(dimension=3,group=group)

        # error checking
        if radius is None:                                                      # no radius defined -> error
            raise TypeError("Variable \"radius\" not set! For a geometric object of type \"{}\", the radius must be specified. Check your input data.".format(self.__class__))
        if center is None:                                                      # no center defined -> error
            raise TypeError("Variable \"center\" not set! For a geometric object of type \"{}\", the center must be specified. Check your input data.".format(self.__class__))
        elif len(np.shape(center)) > 1:                                         # check if center has the right number of array dimensions
            raise ValueError("Wrong amount of array dimensions for variable \"center\"! For a geometric object of type \"{}\", the variable center can only be one-dimensional. Check your input data.".format(self.__class__))
        elif len(center) != 3:                                                  # check if center has 3 values
            raise ValueError("Wrong number of values for variable \"center\"! For a geometric object of type \"{}\", the variable \"center\" has to have 3 values. Check your input data.".format(self.__class__))

        # set object attributes
        self.radius=radius
        self.center=np.asarray(center)


    ##################################################################################
    # Overwrite placeholder method to calculate distances to other geometric objects #
    ##################################################################################
    def getDistance(self,type,*data):
        """Calculate the shortest distance of other objects of type "type" with
        data "data" to this Sphere.

        REMARK:
        Distance calculation which involve cylinders are only exact for capsules.
        This leads to too small distances in some special cases and has to be
        fixed in the future.

        Parameters:
        -----------
        type: string
            type of objects the distance has to be calculated with
            -> "Plane": calculate distance to planes
            -> "Line": calculate distance to lines
            -> "Point": calculate distance to points
            -> "Sphere": calculate distance to spheres
            -> "Cylinder": calculate distance to cylinders

        data: list
            list of arrays and numbers containing relevant information on the
            other objects the distance should be calculated with
            -> "Plane":     data=[[origins], [directors 1], [ directors 2]]
            -> "Line":      data=[[base points], [directors]]
            -> "Point":     data=[[points]]
            -> "Sphere":    data=[[centers], radii]
            -> "Cylinder":  data=[[base points], [axes], radii]
        """
        # distinguish different types
        if type == "Plane":                                                     # distance of planes to this sphere
            distVec, *_ = distancePlanesPoint(self.center,*data)                # -> calculate distance of planes to sphere center
            distance = np.linalg.norm(distVec,axis=1)-self.radius               # -> determine distance of planes to sphere surface
        elif type == "Line":                                                    # distance of lines to this sphere
            distVec, *_ = distanceLinesPoint(self.center,*data)                 # -> calculate distance of lines to sphere center
            distance = np.linalg.norm(distVec,axis=1)-self.radius               # -> determine distance of lines to sphere surface
        elif type == "Point":                                                   # distance of points to this sphere
            distVec, *_ = distancePointsPoint(self.center,*data)                # -> calculate distance of points to sphere center
            distance = np.linalg.norm(distVec,axis=1)-self.radius               # -> calculate distance of points to sphere surface
        elif: type == "Sphere":                                                 # distance of other spheres to this sphere
            distVec, *_ = distancePointsPoint(self.center,data[0])              # -> calculate distance of sphere centers
            distance = np.linalg.norm(distVec,axis=1)-self.radius-data[1]       # -> determine distance of sphere surfaces
        elif: type == "Cylinder":                                               # distance of cylinders to this sphere
            distVec, *_ = distanceLinesPoint(self.center,data[0],data[1])       # -> calculate distance of cylinders center lines to sphere center
            distance = np.linalg.norm(distVec,axis=1)-self.radius-data[2]       # -> determine distance of cylinder to sphere surfaces
        return distance


    #####################################################
    # Overwrite placeholder method to return info array #
    #####################################################
    def getInfoArray(self):
        """Return a list that contains the sphere center and radius."""
        return [self.center, self.radius]


    #############################################################
    # Method to define a refinement field for the Sphere object #
    #############################################################
    def getRefinementField(self,hMax,hMin,width):
        """Define a refinement field (string) for a "gaussian" refinement of
        the sphere object according to the function:

            h(x1,x2,x3)=hMax-(hMax-hMin)*exp( -1/2* (( sqrt( (x_1-x0_1)^2 + (x_2-x0_2)^2 + (x_3-x0_3)^2 ) -r)/(b/4))^2 )

        It represents a refinement which decreases the mesh size from hMax to
        hMin if the distance r from the inclusion center (x0_1,x0_2,x0_3) is
        close to the radius r. The course of the refinement function resembles a
        normal distribution density function with mean value r and standard
        deviation sigma. For convenience, the refinement width (relative to the
        inclusion radius) b is used: since the interval +/-2*sigma covers about
        95% of the values in a normal distribution density function, sigma is
        calculated by b/4.

        Parameters:
        -----------
        hMax: float
            maximum mesh size within the inclusion and far away from its boundary

        hMin: float
            mesh size at the inclusion boundary

        width: float
            width of the refinement area
        """
        # set string for refinement field and return it
        refineFunction="{4}-({4}-({5}))*Exp(-1/2*(((Sqrt((x-({0}))^2+(y-({1}))^2+(z-({2}))^2)-({3}))/({6}))^2))".format(*self.center,self.radius,hMax,hMin,width/4)
        return refineFunction


    ####################################################################################
    # Method to determine transformation matrix from local to global coordinate system #
    ####################################################################################
    def getTransformationMatrix(self):
        """Determine the transformation matrix from the local sphere to the
        global x-y-z-coordinate system.

        Here, no calculations are required, since the matrix is the identity
        matrix."""
        return np.eye(3)


    ######################################################
    # Overwrite placeholder method to move Sphere object #
    ######################################################
    def move(self,offset):
        """Move the sphere, i.e. its center, to its new place"""
        self.center = self.center+np.asarray(offset)


    ################################################################
    # Internal method to determine the objects Gmsh representation #
    ################################################################
    def _getGmshRepresentation(self,gmshModel):
        """Return a Gmsh entity of type Sphere"""
        return gmshModel.occ.addSphere(*np.r_[self.center, self.radius])



################################################################################
#               Define Cylinder as child of GeometricObject                    #
################################################################################
# This class provides more specified attributes and methods for geometrical
# objects of type "Cylinder". It inherits basic properties from its parent class
# "GeometricObject".
class Cylinder(GeometricObject):
    """Definition of a Cylinder object

    This class is a child class of geometricObject and provides additional
    information for objetcs of type Cylinder

    Additional Attributes:
    ----------------------
    axis: array/list
        array that defines the axis (direction and length) of the Cylinder object
        -> axis=[Ax, Ay, Az]

    base: array/list
        array that defines the base point, i.e. starting point of its center
        line, of the Cylinder object
        -> base=[Bx, By, Bz]

    radius: float
        radius of the Cylinder object
    """
    #########################
    # Initialization method #
    #########################
    def __init__(self,base=None,radius=None,axis=None,group="default"):
        """Initialization method for Cylinder objects

        Parameters:
        -----------
        base: array/list
            base point of the Cylinder object (starting point of center line)
            -> base=[Bx, By, Bz]

        radius: float
            radius of the Cylinder object

        axis: array
            axis (direction and length) of the cylinder object

        group: string
            group the Cylinder object belongs to
        """

        # initialize parent classes attributes and methods
        super().__init__(dimension=3,group=group)

        # error checking
        if radius is None:                                                      # no radius defined -> error
            raise TypeError("Variable \"radius\" not set! For a geometric object of type \"{}\", the radius must be specified. Check your input data.".format(self.__class__))
        for varName, varValue in {"base": base, "axis": axis}.items():
            if varValue is None:                                                # check if variable is defined
                raise TypeError("Variable \"{0}\" not set! For a geometric object of type \"{1}\", the variable {0} must be specified. Check your input data.".format(varName,self.__class__))
            elif len(np.shape(varValue)) > 1:                                   # check for correct amount of array dimensions
                raise ValueError("Wrong amount of array dimensions for variable \"{0}\"! For a geometric object of type \"{1}\", the variable \"{0}\" can only be one-dimensional. Check your input data.".format(varName,self.__class__))
            elif len(varValue) != 3:                                            # check for correct amount of variable values
                raise ValueError("Wrong number of values for variable \"{0}\"! For a geometric object of type \"{1}\", the variable \"{0}\" has to have 3 values. Check your input data.".format(center,self.__class__))

        # set object attributes
        self.radius=radius
        self.base=np.asarray(base)
        self.axis=np.asarray(axis)


    ##################################################################################
    # Overwrite placeholder method to calculate distances to other geometric objects #
    ##################################################################################
    def getDistance(self,type,*data):
        """Calculate the shortest distance of other objects of type "type" with
        data "data" to this Cylinder.

        REMARK:
        Distance calculation which involve cylinders are only exact for capsules.
        This leads to too small distances in some special cases and has to be
        fixed in the future.

        Parameters:
        -----------
        type: string
            type of objects the distance has to be calculated with
            -> "Plane": calculate distance to planes
            -> "Line": calculate distance to lines
            -> "Point": calculate distance to points
            -> "Sphere": calculate distance to spheres
            -> "Cylinder": calculate distance to cylinders

        data: list
            list of arrays and numbers containing relevant information on the
            other objects the distance should be calculated with
            -> "Plane":     data=[[origins], [directors 1], [ directors 2]]
            -> "Line":      data=[[base points], [directors]]
            -> "Point":     data=[[points]]
            -> "Sphere":    data=[[centers], radii]
            -> "Cylinder":  data=[[base points], [axes], radii]
        """
        # distinguish different types
        if type == "Plane":                                                     # distance of planes to this cylinder
            distVec, *_ = distancePlanesLine(self.base,self.axis,*data)         # -> calculate distance of planes to center line
            distance = np.linalg.norm(distVec,axis=1)-self.radius               # -> determine distance of planes to cylinder surface
        elif type == "Line":                                                    # distance of lines to this cylinder
            distVec, *_ = distanceLinesLine(self.base,self.axis,*data)          # -> calculate distance of lines to center line
            distance = np.linalg.norm(distVec,axis=1)-self.radius               # -> determine distance of lines to cylinder surface
        elif type == "Point":                                                   # distance of points to this cylinder
            distVec, *_ = distancePointsLine(self.base,*data)                   # -> calculate distance of points to center line
            distance = np.linalg.norm(distVec,axis=1)-self.radius               # -> calculate distance of points to cylinder surface
        elif: type == "Sphere":                                                 # distance of spheres to this cylinder
            distVec, *_ = distancePointsLine(self.base,self.axis,data[0])       # -> calculate distance of sphere centers to center line
            distance = np.linalg.norm(distVec,axis=1)-self.radius-data[1]       # -> determine distance of sphere surfaces to cylinder surface
        elif: type == "Cylinder":                                               # distance of other cylinders to this cylinder
            distVec, *_ = distanceLinesLine(self.base,self.axis,data[0],data[1])# -> calculate distance of cylinder center lines
            distance = np.linalg.norm(distVec,axis=1)-self.radius-data[2]       # -> determine distance of cylinder surfaces
        return distance

    # Overwrite placeholder method to return info array #
    #####################################################
    def getInfo(self):
        """Return a list that contains the cylinder base point, axis and
        radius."""
        return [self.base, self.axis, self.radius]


    #############################################################
    # Method to define a refinement field for the Sphere object #
    #############################################################
    def getRefinementField(self,hMax,hMin,width):
        """Define a refinement field (string) for a "gaussian" refinement of
        the sphere object according to the function:

            h(x1,x2,x3)=hMax-(hMax-hMin)*exp( -1/2* (( sqrt( C_1k*(x_k-x0_k)^2 + C_2k*(x_k-x0_k)^2 + C_3k*(x_k-x0_k)^2 ) -r)/(b/4))^2 )

        It represents a refinement which decreases the mesh size from hMax to
        hMin if the distance r from the inclusion center line is close to the
        radius r. The course of the refinement function resembles a normal
         distribution density function with mean value r and standard deviation
        sigma. For convenience, the refinement width (relative to the inclusion
        radius) b is used: since the interval +/-2*sigma covers about 95% of the
        values in a normal distribution density function, sigma is calculated
        by b/4.

        Here, the cylinders axis is assumed to point in the x3'-direction: since
        x'_k=C_kl*x_l with C being a transformation matrix, only the first to
        rows of this system are relevant here.

        Parameters:
        -----------
        hMax: float
            maximum mesh size within the inclusion and far away from its boundary

        hMin: float
            mesh size at the inclusion boundary

        width: float
            width of the refinement area
        """
        # get transformation matrix:
        C=self.getTransformationMatrix()
        relC=C[0:2].flatten()

        # set string for refinement field and return it
        refineFunction="({9})-(({9})-({10}))*Exp(-1/2*((Sqrt( {0}*(x-({6}))^2 + {1}*(y-({7}))^2 + {2}*(z-({8}))^2 ) + ( {3}*(x-({6}))^2 + {4}*(y-({7}))^2 + {5}*(z-({8}))^2 ) - {11})/({12}))^2))".format(*self.center,*relC,self.radius,hMax,hMin,width/4)
        return refineFunction


    ####################################################################################
    # Method to determine transformation matrix from local to global coordinate system #
    ####################################################################################
    def getTransformationMatrix(self):
        """Determine the transformation matrix from the local cylinder to the
        global x-y-z-coordinate system - assume that the transformed cylinder
        axis points into the global z-direction.

        For the angles of the required 2 rotations, phi assumed to be always
        in [-pi/2, pi/2], whereas theta is in [-pi, pi]."""

        # determine angles from cylinder axis
        phi = np.arctan2(axis[0],np.sqrt(axis[1]**2+axis[2]**2))                # rotation angle around y-axis
        theta = np.arctan2(axis[1],axis[2])                                     # rotation angle arount x'-axis (x-axis after first rotation)

        # determine transformation matrix
        C=np.array([[np.cos(phi), -np.sin(theta)*np.sin(phi), -np.cos(theta)*np.sin(phi)],
                    [0, np.cos(theta), -np.sin(theta)],
                    [np.sin(phi), np.sin(theta)*np.cos(phi), np.cos(theta)*np.cos(phi)]])

        # save transformation matrix
        return C


    ########################################################
    # Overwrite placeholder method to move Cylinder object #
    ########################################################
    def move(self,offset):
        """Move the cylinder, i.e. its base point, to its new place"""
        self.base = self.base+np.asarray(offset)


    ################################################################
    # Internal method to determine the objects Gmsh representation #
    ################################################################
    def _getGmshRepresentation(self,gmshModel):
        """Return a Gmsh entity of type Cylinder"""
        return gmshModel.occ.addCylinder(*np.r_[self.base, self.axis, self.radius])



################################################################################
#                  Define Circle as child of GeometricObject                   #
################################################################################
# This class provides more specified attributes and methods for geometrical
# objects of type "Sphere". It inherits basic properties from its parent class
# "GeometricObject".
class Circle(GeometricObject):
    """Definition of an Circle object

    This class is a child class of geometricObject and provides additional
    information for objetcs of type Circle

    Additional Attributes:
    ----------------------
    center: array/list
        array that defines the center of the Circle object
        -> center=[Cx, Cy, Cz]

    radius: float
        radius of the Circle object
    """
    #########################
    # Initialization method #
    #########################
    def __init__(self,center=None,radius=None,group="default"):
        """Initialization method for Circle objects

        Parameters:
        -----------
        center: array/list
            center of the Circle object
            -> center=[Cx, Cy, (Cz)]

        radius: float
            radius of the Circle object

        group: string
            group the Circle object belongs to
        """

        # initialize parent classes attributes and methods
        super().__init__(dimension=2,group=group)

        # error checking
        if radius is None:                                                      # radius not defined -> error
            raise TypeError("Variable \"radius\" not set! For a geometric object of type \"{}\", the radius must be specified. Check your input data.".format(self.__class__))
        if center is None:                                                      # no center defined -> error
            raise TypeError("Variable \"center\" not set! For a geometric object of type \"{}\", the center must be specified. Check your input data.".format(self.__class__))
        elif len(np.shape(center)) > 1:                                         # check for correct amount of array dimensions
            raise ValueError("Wrong amount of array dimensions for variable \"center\"! For a geometric object of type \"{}\", the variable \"center\" can only be one-dimensional. Check your input data.".format(self.__class__))
        elif not len(center) in [2,3]:                                          # check for correct amount of variable values
            raise ValueError("Wrong number of values for variable \"center\"! For a geometric object of type \"{}\", the center has to have 2 or 3 values. Check your input data.".format(self.__class__))

        # Correct potentially two-dimensional arrays
        if len(center) != 3:                                                    # check if center is not a three-dimensional array
            center=np.r_[center,0]                                               # -> append 0

        # set object attributes
        self.radius=radius
        self.center=np.asarray(center)


    ##################################################################################
    # Overwrite placeholder method to calculate distances to other geometric objects #
    ##################################################################################
    def getDistance(self,type,*data):
        """Calculate the shortest distance of other objects of type "type" with
        data "data" to this Circle.

        Parameters:
        -----------
        type: string
            type of objects the distance has to be calculated with
            -> "Line": calculate distance to lines
            -> "Point": calculate distance to points
            -> "Circle": calculate distance to circles

        data: list
            list of arrays and numbers containing relevant information on the
            other objects the distance should be calculated with
            -> "Line":      data=[[origins], [directors]]
            -> "Point"      data=[[points]]
            -> "Circle":    data=[[centers], radii]
        """
        # distinguish different types
        if type == "Line":                                                      # distance of lines to this circle
            distVec, *_ = distanceLinesPoint(self.center,*data)                 # -> calculate distance of lines to circle center
            distance = np.linalg.norm(distVec,axis=1)-self.radius               # -> determine distance of lines to circle
        elif type == "Point":                                                   # distance of points to this circle
            distVec, *_ = distancePointsPoint(self.center,*data)                # -> calculate distance of points to circle center
            distance = np.linalg.norm(distVec,axis=1)-self.radius               # -> determine distance of points to circle
        elif: type == "Circle":                                                 # distance of other circles to this circle
            distVec, *_ = distancePointsPoint(self.center,data[0])              # -> calculate distance of circle centers
            distance = np.linalg.norm(distVec,axis=1)-self.radius-data[1]       # -> determine distance of circles
        return distance


    #####################################################
    # Overwrite placeholder method to return info array #
    #####################################################
    def getInfo(self):
        """Return a list that contains the circle center and radius."""
        return [self.center, self.radius]


    ####################################################################################
    # Method to determine transformation matrix from local to global coordinate system #
    ####################################################################################
    def getTransformationMatrix(self):
        """Determine the transformation matrix from the local circle to the
        global x-y-z-coordinate system.

        Assume that circles are placed in the x-y-plane since this is the only
        supported way in Gmsh."""
        C=np.eye(3)
        C[2,2]=0
        return C


    ######################################################
    # Overwrite placeholder method to move Circle object #
    ######################################################
    def move(self,offset):
        """Move the circle, i.e. its center, to its new place"""
        self.center = self.center+np.asarray(offset)


    ################################################################
    # Internal method to determine the objects Gmsh representation #
    ################################################################
    def _getGmshRepresentation(self,gmshModel):
        """Return a Gmsh entity of type Disk"""
        return gmshModel.occ.addDisk(*np.r_[self.center, self.radius, self.radius])
