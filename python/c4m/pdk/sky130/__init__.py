# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
from importlib import import_module
from typing import List, Any

from pdkmaster.design import library as _lbry

from c4m.flexcell import factory as _stdfab

from .klayout import register_primlib as pya_register_primlib


# This module uses lazy submodule importing using __getattr__() to avoid that all
# libraries are generated when this module is imported.


from .pdkmaster import __all__ as _pdkmaster_all
from .pyspice import __all__ as _pyspice_all
from .stdcell import __all__ as _stdcell_all
from .io import __all__ as _io_all
from .factory import __all__ as _factory_all

__all__ = [*_pdkmaster_all, *_pyspice_all, *_stdcell_all, *_io_all, *_factory_all]


StdCellFactory: type
stdcellcanvas: _stdfab.StdCellCanvas
stdcelllib: _lbry.RoutingGaugeLibrary
StdCellLambdaFactory: type
stdcelllambdacanvas: _stdfab.StdCellCanvas
stdcelllib: _lbry.RoutingGaugeLibrary
Sky130IOFactory: type
iolib: _lbry.Library
macrolib: _lbry.Library
libs: List[_lbry.Library]
def __getattr__(name: str) -> Any:
    if name in _pdkmaster_all:
        pdkmaster = import_module(".pdkmaster", __name__)
        return getattr(pdkmaster, name)
    elif name in _pyspice_all:
        pyspice = import_module(".pyspice", __name__)
        return getattr(pyspice, name)
    elif name in _stdcell_all:
        stdcell = import_module(".stdcell", __name__)
        return getattr(stdcell, name)
    elif name in _io_all:
        io = import_module(".io", __name__)
        return getattr(io, name)
    elif name in _factory_all:
        factory = import_module(".factory", __name__)
        return getattr(factory, name)
    elif name == "libs":
        from .stdcell import stdcelllib
        from .io import iolib
        from .factory import macrolib
        return [
            stdcelllib,
            iolib,
            macrolib,
        ]
    else:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    self = import_module(__name__)
    return sorted((
        *(name for name in self.__dict__.keys() if name.startswith("__")),
        *_pdkmaster_all, *_pyspice_all,
        "pya_register_primlib",
        *_stdcell_all, *_io_all, *_factory_all,
        "libs",
    ))
