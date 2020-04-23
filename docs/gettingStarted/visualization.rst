.. _visualization_ref:

Using the visualization features
================================
After the mesh generation, it is sometimes advantageous to have the possibility
to visualize the resulting mesh in order to check if it matches the own requirements.
In gmshModel, this can be accomplished by using the ``visualizeMesh()`` functionality
of the ``GenericModel``: since all available model types inherit the methods of
``GenericModel``, the method is available for all models.

.. code-block:: python

   ...
   # visualize the mesh of myModel
   myModel.visualizeMesh()


The mesh visualization is based on the `pyvista <https://github.com/pyvista/pyvista/>`_
library and uses its features. If the visualization method is called, the mesh
is written to a temporary ``.vtk``-file which is then visualized with pyvista.
Within an active visualization window, several ``key-events`` allow for extended
features:

+-----------+--------------------------------+
| ``x``     | set view to y-z-plane          |
+-----------+--------------------------------+
| ``y``     | set view to z-x-plane          |
+-----------+--------------------------------+
| ``z``     | set view to x-y-plane          |
+-----------+--------------------------------+
| ``q``     | close visualization window     |
+-----------+--------------------------------+
| ``m``     | toggle visualization menu      |
+-----------+--------------------------------+
| ``space`` | confirm settings and re-render |
+-----------+--------------------------------+
| ``d``     | restore default settings       |
+-----------+--------------------------------+


Since the `normal` way of generating meshes in Gmsh involves the definition of
physical groups to, e.g., distinguish different materials, threshold sliders can
be used if the visualization menu is activated. They allow to enable or disable
different groups according to the defined physical groups in the gmshModel.
Additionally, an extraction box widget can be used to extract regions of the mesh
and have a closer look to them.

.. image:: ../images/VisualizationBasic.png
   :width: 80%
   :align: center
   :alt: basic visualization

.. image:: ../images/VisualizationMenu.png
   :width: 80%
   :align: center
   :alt: visualization menu
