.. _api_ref:

API Reference
=============

The core functionality of GmshModel is the mesh generation for complex models
using Gmsh and the Gmsh-Python-API. The creation of such complex models, often
requires methods for the geometry generation. To this end, basic geometric objects
and helper methods for, e.g., distance calculations are provided within the
``Geometry`` module of GmshModel: using boolean operations for
groups of basic geometric objects, complex models can be defined step by step.
An extension of the modules will help to broaden the range of available models.

After the geometry is defined, it has to be transferred into a Gmsh model: all
geometric objects are translated to their Gmsh representations, boolean
operations are performed and physical groups are added to the model. Within
the Model module of ``Model``, predefined models can be found.
Since, so far, the focus of GmshModel was on mesh models for representative
volume elements with multiple, randomly placed inclusions, especially those models
are already defined in GmshModel. However, since the GenericModel defines all required
methods for the model generation, the basic tasks for the development of a new
model are the definitions of required geometric objects and their arrangement within
the model, of boolean operations and physical groups to be performed/added in Gmsh
and of refinement information for an auomated mesh size computation.

Finally, basic GUIs for the geometry and mesh visualization are defined within
the ``Visualization`` module while an extension of the mesh conversion capabilities
of meshio for simulations using FEAP is defined within the ``MeshExport`` module.


.. toctree::
   :maxdepth: 2

   Model/index
   Geometry/index
   Visualization/index
   MeshExport/index
