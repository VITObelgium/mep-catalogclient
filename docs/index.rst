.. catalogclient documentation master file, created by
   sphinx-quickstart on Fri Jan 20 07:49:16 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

catalogclient: client to search the PROBA-V MEP catalog
=======================================================

This Python client uses the REST service of the `PROBA-V MEP <https://proba-v-mep.esa.int/>`_ catalog,
making it easier to search PROBA-V EO data products.

Installation
============

The package is available in the public PROBA-V MEP PyPi repository and can be easily installed using pip::

   $ pip install catalogclient


When you are using a `PROBA-V MEP Virtual Machine (VM) <https://proba-v-mep.esa.int/proba-v-mep-toolset/user-virtual-machine>`_,
the package is already pre-installed for you.

Usage
=====

Example retrieving available data of the ROBAV_L3_S10_TOC_333M for year 2016::

>>> from catalogclient import catalog
>>> cat=catalog.Catalog()
>>> cat.get_products_for_year('PROBAV_L3_S10_TOC_333M', 2016)

API
===

.. automodule:: catalogclient.catalog
   :members:

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
