.. _installation_ref:

Installation
============
As most Python packages, gmshModel can be installed in more than one way. Here,
the two most common ways of the package installation will be pointed out: the
installation via the `Python Package Index <https://pypi.org/>`_ and a manual
installation using the source code.

Dependencies
************
GmshModel is an interface tool and makes use of many great contributions of other
people. To experience the full functionality of gmshModel, several software packages
are required.

The most important software for the use of gmshModel is `Gmsh <https://gmsh.info/>`_
with an activated `Gmsh-Python-API <https://gitlab.onelab.info/gmsh/gmsh/-/blob/master/api/gmsh.py/>`_.
The compilation of Gmsh from source is described
`here <https://gitlab.onelab.info/gmsh/gmsh/-/wikis/Gmsh-compilation/>`_. While
following the installation instructions, make sure that `FLTK <https://www.fltk.org/>`_
is configured using the ``--enable-shared`` flag and Gmsh uses the
``-DENABLE_BUILD_DYNAMIC=1`` flag when `cmake <https://cmake.org/>`_ is called.
An easier way of installing Gmsh is provided using the existing `PyPi package <https://pypi.org/project/gmsh/>`_ 
which can be installed typing

.. code-block:: python

   python3 -m pip install gmsh
   
Independent of which way you choose, please make sure that the Gmsh-Python-API is 
working for you by checking its import:

.. code-block:: python

   python3 -c "import gmsh; gmsh.initialize(['', '--help'])"
   
The gmshModel package itself depends on `numpy <https://numpy.org/>`_. For advanced 
features, the following packages are required as well:

1. `meshio <https://github.com/nschloe/meshio/>`_  for the conversion of meshes to various output formats
2. `pyvista <https://www.pyvista.org/>`_ for the visualization of meshes
3. `pythonocc <https://github.com/tpaviot/pythonocc-core/>`_ for the visualization of the model geometry

If ``pip`` is used for the package installation, numpy as well as meshio and pyvista 
will be installed automatically. However, pythonocc is not available at PyPi and 
therefore has to be `compiled from source <https://github.com/tpaviot/pythonocc-core/blob/master/INSTALL.md/>`_.


Installation using PyPi
***********************
Since gmshModel is available from the `Python Package Index <https://pypi.org/>`_,
it can simply be installed using the following command:

.. code-block:: python

   python3 -m pip install gmshModel


Manual installation
*******************
For a manual installation of gmshModel, the source code has to be downloaded from
`Github <https://github.com/NEFM-TUDresden/gmshModel/>`_ or `PyPi <https://pypi.org/project/gmshModel/>`_.
Once this is done, the installation from within the downloaded source code is as
easy as using the command:

.. code-block:: python

   pip install .

