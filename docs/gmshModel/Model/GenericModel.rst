GenericModel
============
The GenericModel is the base class for other, more specific classes which aim 
to mesh models using the Gmsh- Python-API. In addition to the methods defined 
within the Gmsh-Python-API, this class provides methods for all basic steps of 
a model generation using Gmsh: some of these methods are only placeholders here 
and - if required - have to be specified/overwritten for the more specialized 
models.

Class Definition
----------------

.. autoclass:: gmshModel.Model.GenericModel.GenericModel
   :show-inheritance:
   :members:
