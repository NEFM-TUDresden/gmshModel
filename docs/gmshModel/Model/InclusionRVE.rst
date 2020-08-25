InclusionRVE
============
The InclusionRVE provides a class definition for a generation of RVEs with inclusions
using Python and Gmsh. The class inherits from the GenericRVE class and extends
it in order to handle distance and refinement calculations

Currently, the class is restricted to RVEs with rectangular (2D)/ box-shaped
(3D) domains (explicitly assumed within the setupPeriodicity() method) which
comprise inclusions that are all of the same type (explicitly assumed by using
one inclusionInformation array and one inclusionAxis variable).

Class Definition
----------------

.. autoclass:: gmshModel.Model.InclusionRVE.InclusionRVE
   :show-inheritance:
   :members:
