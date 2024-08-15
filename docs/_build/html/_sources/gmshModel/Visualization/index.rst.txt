.. _api_visualization_ref:

Visualization
=============

To see, if the generated mesh matches the own requirements, a basic visualization
tool using `pyvista <https://www.pyvista.org/>`_ has been defined in the ``MeshVisualization``
class. If a mesh generation does not work and the `pythonocc <https://github.com/tpaviot/pythonocc-core/>`_
package is available, the geometry of the Gmsh model can also be visualized using
the ``GeometryVisualization`` class.

.. toctree::
   :maxdepth: 1

   GeometryVisualization
   MeshVisualization
