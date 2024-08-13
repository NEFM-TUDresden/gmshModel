GenericRVE
==========
The GenericRVE provides a class definition for an RVE generation using Python and
Gmsh. The class inherits from the GenericModel class and extends it in order
order to handle the problems that are connected with the generation of models
with periodicity constraints.

Currently, the class is restricted to RVEs with rectangular (2D)/ box-shaped
(3D) domains (explicitly assumed within the setupPeriodicity() method).

Class Definition
----------------

.. autoclass:: gmshModel.Model.GenericRVE.GenericRVE
   :show-inheritance:
   :members:
