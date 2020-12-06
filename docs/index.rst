.. include:: ../README.rst

Version: |version|

Command Line Options
====================

.. argparse::
    :filename: ../bin/torq
    :func: parser
    :prog: torq


Actions
=======

``torq`` runs a series of actions on the file or directory passed in on the
command line. Each action can be turned off with a ``--no-action`` argument,
where *action* is replaced with the name of the action in lower case. For
example, ``HeaderCheck`` can be turned off with ``-no-headercheck``.

The following actions are run in this order:

.. automodule:: torquemada.actions
    :members:
    :member-order: bysource


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
