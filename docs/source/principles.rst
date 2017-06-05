=================
Design Principles
=================

Some design principles for the port:

  * We prefer PEP 8 naming for the Python API.

  * We raise appropriate exceptions for a Python program (*e.g.* ``ValueError`` and ``KeyError``)

  * We'll start with a fairly literal translation of the Java API, with ``getFoo`` and ``setFoo()`` but migrate to
    Python properties where appropriate.
