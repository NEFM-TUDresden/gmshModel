.. _installation_ref:

Installation
============
As most Python packages, gmshModel can be installed in more than one way. Here,
the two common ways of the package installation will be pointed out: the
installation via the `Conda <https://anaconda.org/>`_ and `PyPi <https://pypi.org/>`_
package managers.


Dependencies
************
GmshModel is an interface tool and makes use of many great contributions of other
people. To experience the full functionality of Gmsh model, the following (non-standard)
software packages are required:

1. a `dynamically built Gmsh <https://gitlab.onelab.info/gmsh/gmsh/-/wikis/Gmsh-compilation/>`_  to use the Gmsh-Python-API
2. `meshio <https://github.com/nschloe/meshio/>`_  for the conversion of meshes to various output formats
3. `pyvista <https://www.pyvista.org/>`_ for the visualization of meshes
4. `pythonocc-core <https://github.com/tpaviot/pythonocc-core/>`_ for the visualization of the model geometry

Using the supported PyPi and Conda package managers, all dependencies that
are necessary to run gmshModel will be automatically installed. Since the ``pythonocc-core``
package does not provide an installation for PyPi, the geometry visualization feature
will not be available for it.


Installation using Conda
************************
The availability of gmshModel in the `conda-forge channel <https://anaconda.org/conda-forge/gmshmodel>`_
allows a straightforward installation of the package using the following command: ::

   $ conda install -c conda-forge gmshModel


Installation using PyPi
***********************
Since gmshModel is also available from the `Python Package Index <https://pypi.org/project/gmshModel/>`_,
PyPi users can simply install it using the following command: ::

   $ python3 -m pip install gmshModel

If the package does not work after the installation due to an import error of
the Gmsh-Python-API, your system probably cannot find the file ``gmsh.py``. In order
to fix this, a symbolic link from its installation location into the ``site-packages``
directory of your Python installation can be created: ::

   # example for linux users:
   $ ln -s <PATH TO GMSH>/lib/gmsh.py $HOME/.local/lib/<PYTHON VERSION>/site-packages/gmsh.py

If you also want to have a working geometry visualization, you can
`compile pythonocc-core from source <https://github.com/tpaviot/pythonocc-core/blob/master/INSTALL.md/>`_.
