################################################################################
#          CLASS DEFINITIONS OF FREQUENTLY USED REFINEMENT FIELDS              #
################################################################################
# Within this file, frequently used refinement fields are defined to facilitate
# the handling of interacting fields and allow to easily upgrade the range of
# available mesh refinement fields within gmshModel.

###########################
# Load required libraries #
###########################
# Standard Python libraries
import numpy as np                                                              # numpy for fast array computations

###################################
# Define generic refinement field #
###################################
class RefinementField:
    """Generic RefinementField class

    Attributes:
    -----------
    data: dictionary
        dictionary containing refinement field information for Gmsh

    model: object instance
        instance of gmshModel to provide refinement field for

    tag: int
        Gmsh internal refinement field tag

    type: string
        Gmsh internal type string for refinement field
    """
    #########################
    # Initialization method #
    #########################
    def __init__(self,model=None,data=None):
        """Initialization method of generic RefinementField class

        Parameters:
        -----------
        model: object instance
            gmshModel instance to define refinement field for
        """
        # check input arguments
        if model == None:                                                       # no model instance passed -> raise error
            raise ValueError("Refinement fields have to be defined for a specific model to allow for an interaction with the Gmsh-Python-API. To this end, the variable \"model\" has to be set. Check your input.")
        if data == None:                                                        # no data for refinement field passed -> error
            raise ValueError("No data for refinement field of type \"{}\" passed. Check your input.".format(type(self).__name__))

        # save required data
        self.model=model                                                        # save model
        self.type=None                                                          # initialize (Gmsh) type to None

        # add field to Gmsh model and set tag
        self.tag=self.model.gmshAPI.mesh.field.add(self.type,tag=-1)

        # set field data with type specific data passed by user
        self.data=data

        # add field data to Gmsh model
        self.setFieldData()


    ###############################################################
    # Method to set field-specific data for current field in Gmsh #
    ###############################################################
    def setFieldData(self):
        gmshField=self.model.gmshAPI.mesh.field
        for optName, optVal in self.data.items():                               #  provide all necessary information for this field from data dictionary
            if isinstance(optVal,str):                                          # -> current option value is a string
                gmshField.setString(self.tag,optName,optVal)                    # ->-> use built-in setString method of gmsh.model.mesh.field
            elif isinstance(optVal,int) or isinstance(optVal,float):            # -> current option value is a number
                gmshField.setNumber(self.tag,optName,optVal)                    # ->-> use built-in setNumber method of gmsh.model.mesh.field
            elif isinstance(optVal,list) or isinstance(optVal,np.ndarray):      # -> current option value is a list or numpy array
                gmshField.setNumbers(self.tag,optName,optVal)                   # ->-> use built-in setNumbers method of gmsh.model.mesh.field



########################
# Define Minimum Field #
########################
class MinField(RefinementField):
    """Min refinement field: calculate the minimum mesh size from data provided
    by other refinement fields

    Additional Attributes:
    ----------------------
    none
    """
    #########################
    # Initialization method #
    #########################
    def __init__(self,model=None, fieldsList=None):
        """Initialization method of MinField class

        Parameters:
        -----------
        model: object instance
            gmshModel instance to define refinement field for

        fieldsList: list
            list of refinement fields to apply MinField for
        """
        # check inputs
        if fieldsList is None:
            raise ValueError("No list of fields passed. For a refinement field of type \"Min\", the \"fieldsList\" variable has to be passed. Check your input.")

        # save required data
        self.type="Min"                                                         # set (Gmsh) type to "Min"

        # generate dict with required options for Gmsh
        data={"FieldsList": fieldsList}                                         # set list of fields to use for "Min" field

        # initialize parent RefinementField class
        super().__init__(model=model, data=data)



#########################
# Define MathEval Field #
#########################
class MathEvalField(RefinementField):
    """MathEval refinement field: calculate mesh size from a given function
    string

    Additional Attributes:
    ----------------------
    none
    """
    #########################
    # Initialization method #
    #########################
    def __init__(self,model=None,functionString=None):
        """Initialization method of MathEvalField class

        Parameters:
        -----------
        model: object instance
            gmshModel instance to define refinement field for
        """
        # check inputs
        if functionString is None:
            raise ValueError("No function string passed. For a refinement field of type \"MathEval\", the \"functionString\" variable has to be passed. Check your input.")

        # save required data
        self.type="MathEval"                                                    # set (Gmsh) type to "MathEval"

        # generate dict with required options for Gmsh
        data={"F": functionString}                                              # set function string to use for "MathEval" field

        # initialize parent RefinementField class
        super().__init__(model=model,data=functionString)
