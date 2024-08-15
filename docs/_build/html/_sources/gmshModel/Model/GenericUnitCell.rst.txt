GenericUnitCell
===============
The GenericUnitCell class provides required information for inclusion-based unit
cells. It inherits from the InclusionRVE class and extends its attributes and
methods to handle the boolean operations and the definition of physical groups.

All unit cell allow to create "real" unit cells by passing the inclusion
distance to the classes initialization method. If the cells size is
specified instead, the distance is calculated automatically: this allows for
unit cells with an inclusion distribution that is close to physical unit
cells but gives more flexibility in their generation.

Class Definition
----------------

.. autoclass:: gmshModel.Model.GenericUnitCell.GenericUnitCell
   :show-inheritance:
   :members:
