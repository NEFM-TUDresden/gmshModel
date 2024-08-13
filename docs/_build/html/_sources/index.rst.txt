GmshModel
=========
`Gmsh <https://gmsh.info/>`_ is a powerful tool for the generation of meshes for
numerical simulations but the built-in scripting language makes the meshing
procedure and especially an automatization really hard. Luckily, Gmsh provides
a Python-API with which all the capabilites of Gmsh can be used within Python.

GmshModel is intended to be an extendable tool that facilitates the mesh generation
by interfacing the Gmsh-Python-API: it provides a basic framework for an automated
mesh generation for self-defined model types and, with that, allows to automate the
generation of complex models as, e.g., representative volume elements. To this
end, GmshModel divides the mesh modeling procedure into basic steps:

1. Setting up a geometry using basic geometric entities and boolean operations.
2. Adding the geometric objects to Gmsh, performing the boolean operations and defining physical groups.
3. Creating a mesh with user-defined refinement fields.
4. Saving the mesh to various output formats.
5. Visualizing the resulting mesh.

So far, GmshModel is especially designed to automate the generation of representative
volume elements that contain multiple inclusion objects. An extension of gmshModel
is however possible by adding new geometric objects and model types to the framework.

It is not the purpose of GmshModel to replace the Gmsh scripting language or other
great tools such as `PyGmsh <https://github.com/nschloe/pygmsh>`_  for the generation
of meshes. GmshModel rather tries to function as an interface to Gmsh to facilitate
the automation of recurring, complex meshing tasks that require the full functionality
of Gmsh in a nice and easy to use programming environment such as Python.


Getting Started
***************
To get all information on how to install gmshModel, see :ref:`installation_ref`.
If you are using ``pip``, simply use the following command to install gmshModel
and its features: ::

   $ python3 -m pip install gmshModel

For ``conda`` users, the installation command is straightforward, too: ::

   $ conda install -c conda-forge gmshModel

.. image:: images/RVE200SpheresGeo.png
    :width: 49%
    :alt: 200SpheresGeo
.. image:: images/RVE200SpheresMesh.png
    :width: 49%
    :alt: 200SpheresMesh

To check out what you can do with gmshModel and generate the above periodic mesh
with ``200`` randomly placed spherical inclusions of radius ``1`` in a ``[20x20x20]``
domain, simply use the following code:

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


Go to :ref:`examples_ref` to check out more examples of meshes generated using
gmshModel.

.. toctree::
   :maxdepth: 2
   :caption: Getting Started
   :hidden:

   gettingStarted/installation
   gettingStarted/visualization
   examples/index


Documentation
*************

Here, you can find out how gmshModel works, which classes and methods are involved
and how you can use them to generate your own model:

* :ref:`api_geometry_ref` gives information on available geometric objects
* :ref:`api_model_ref` explains all available models
* :ref:`api_visualization_ref` gives information on the visualization capabilities of gmshModel
* :ref:`api_meshExport_ref` comments on additional mesh output formats (extending meshio)

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Documentation

   gmshModel/index


Index
*****

* :ref:`genindex`
