gmshModel
=========

.. |pypi| image:: https://img.shields.io/pypi/v/gmshModel?color=blue
   :target: https://pypi.org/project/gmshModel

.. |conda| image:: https://img.shields.io/conda/v/conda-forge/gmshModel?color=blue
   :target: https://anaconda.org/conda-forge/gmshmodel

.. |pyver| image:: https://img.shields.io/pypi/pyversions/gmshModel.svg?color=green3
   :target: https://www.python.org/

.. |GPL| image:: https://img.shields.io/pypi/l/gmshModel?color=orange
   :target: https://opensource.org/licenses/gpl-3.0.html

.. |pypiStats| image:: https://img.shields.io/pypi/dm/gmshModel?color=yellow
   :target: https://pypistats.org/packages/gmshmodel

|pypi| |conda| |pyver| |GPL| |pypiStats|

`Gmsh <https://gmsh.info/>`_ is a powerful tool for the generation of meshes for
numerical simulations but the built-in scripting language makes the meshing
procedure and especially an automatization really hard. Luckily, Gmsh provides
a Python-API with which all the capabilites of Gmsh can be used within Python.

GmshModel is intended to be an extendable tool that facilitates the mesh generation
by interfacing the Gmsh-Python-API: it provides a basic framework for an automated
mesh generation for self-defined model types and, with that, allows to automate the
generation of complex models as, e.g., representative volume elements. To this
end, gmshModel divides the mesh modeling procedure into basic steps:

1. Setting up a geometry using basic geometric entities and boolean operations.
2. Adding the geometric objects to Gmsh, performing boolean operations and defining physical groups.
3. Creating a mesh with user-defined refinement fields.
4. Saving the mesh to various output formats.
5. Visualizing the resulting mesh.

So far, gmshModel is especially designed to automate the generation of representative
volume elements that contain multiple inclusion objects and well-known unit cells
with different types of inclusions. An extension of gmshModel is, however, possible by
adding new geometric objects and model types to the framework.

It is not the purpose of gmshModel to replace the Gmsh scripting language or other
great tools such as `pygmsh <https://github.com/nschloe/pygmsh>`_  for the generation
of meshes. GmshModel rather tries to function as an interface to Gmsh to facilitate
the automation of recurring, complex meshing tasks that require the full functionality
of Gmsh within a nice and easy to use environment such as Python.


Installation
************
GmshModel is available from the `Python Package Index <https://pypi.org/project/gmshModel/>`_ and
can be installed using the following command: ::

   $ python3 -m pip install gmshModel

The integration of gmshModel into the `conda-forge <https://anaconda.org/conda-forge/gmshmodel>`_
channel allows to use a similar procedure for Conda users: ::

   $ conda install -c conda-forge gmshModel

It is also possible to download the source code from `GitHub <https://github.com/NEFM-TUDresden/GmshModel/>`_
or `PyPi <https://pypi.org/project/gmshModel/>`_ and install gmshModel manually. For more details, check
the `installation page <https://gmshmodel.readthedocs.io/en/latest/gettingStarted/installation.html>`_ of 
the documentation.


Dependencies
************
GmshModel is an interface tool and makes use of many great contributions of other
people. To experience the full functionality of Gmsh model, the following (non-standard)
software packages are required:

1. a `dynamically built Gmsh <https://gitlab.onelab.info/gmsh/gmsh/-/wikis/Gmsh-compilation/>`_  to use the Gmsh-Python-API
2. `meshio <https://github.com/nschloe/meshio/>`_  for the conversion of meshes to various output formats
3. `pyvista <https://www.pyvista.org/>`_ for the visualization of meshes
4. `pythonocc <https://github.com/tpaviot/pythonocc-core/>`_ for the visualization of the model geometry


Getting Started
***************

.. image:: https://github.com/NEFM-TUDresden/gmshModel/raw/master/docs/images/GettingStarted.png
   :alt: Sample Geometry and Mesh

To generate the above periodic box in a ``[20x20x20]`` domain which contains ``200`` spherical
inclusions of radius ``1``, simply type:

.. code-block:: python

   # import required model type
   from gmshModel.Model import RandomInclusionRVE as RVE

   # initialize new RVE
   myRVE=RVE(size=[20,20,20], inclusionType="Sphere", inclusionSets=[1, 200])

   # create Gmsh model
   myRVE.createGmshModel()

   # generate mesh
   myRVE.createMesh()

   # save resulting mesh to vtk
   myRVE.saveMesh("myRVE.vtk")

   # visualize result
   myRVE.visualizeMesh()

   # finalize Gmsh-Python-API
   myRVE.close()


Documentation
*************

The gmshModel documentation is available `here <https://gmshmodel.readthedocs.io/en/latest/>`_.


License
*******
GmshModel is published under the `GPLv3 license <https://www.gnu.org/licenses/gpl-3.0.en.html>`_
