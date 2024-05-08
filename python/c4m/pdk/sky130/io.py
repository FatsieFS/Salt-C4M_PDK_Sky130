# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
from typing import cast

from pdkmaster.technology import property_ as _prp, primitive as _prm
from pdkmaster.design import circuit as _ckt, layout as _lay, library as _lbry
from pdkmaster.io.klayout import merge

from c4m.flexio import IOSpecification, TrackSpecification, IOFrameSpecification, IOFactory

from .pdkmaster import tech, cktfab, layoutfab
from .stdcell import stdcelllib

__all__ = ["Sky130IOFactory", "iolib"]


_prims = tech.primitives


class Sky130IOFactory(IOFactory):
    iospec = IOSpecification(
        stdcelllib=stdcelllib,
        nmos=cast(_prm.MOSFET, _prims.nfet_01v8), pmos=cast(_prm.MOSFET, _prims.pfet_01v8),
        ionmos=cast(_prm.MOSFET, _prims.nfet_g5v0d10v5),
        iopmos=cast(_prm.MOSFET, _prims.pfet_g5v0d10v5),
        monocell_width=90,
        metal_bigspace=0.6, topmetal_bigspace=4.0,
        clampnmos=None, clampnmos_w=16.90, clampnmos_l=0.6,
        clamppmos=None, clamppmos_w=38.20, clamppmos_l=0.6,
        clampfingers=32, clampfingers_analog=12, clampdrive=4,
        clampgate_gatecont_space=0.24, clampgate_sourcecont_space=0.44,
        clampgate_draincont_space=0.51,
        add_clampsourcetap=True,
        clampsource_cont_tap_enclosure=_prp.Enclosure((0.265, 0.06)), clampsource_cont_tap_space=0.075,
        clampdrain_layer=None, clampgate_clampdrain_overlap=None, clampdrain_active_ext=None,
        clampdrain_gatecont_space=None, clampdrain_contcolumns=2, clampdrain_via1columns=4,
        nres=cast(_prm.Resistor, _prims.poly_res),
        pres=cast(_prm.Resistor, _prims.poly_res),
        ndiode=cast(_prm.Diode, _prims.ndiode),
        pdiode=cast(_prm.Diode, _prims.pdiode),
        secondres_width=1.0, secondres_length=5.0,
        secondres_active_space=0.6,
        corerow_height=5.5, corerow_nwell_height=3.3,
        iorow_height=8.5, iorow_nwell_height=5.25,
        nwell_minspace=2.0, levelup_core_space=1.0,
        resvdd_prim=cast(_prm.Resistor, _prims.poly_res),
        resvdd_w=0.33, resvdd_lfinger=58.0, resvdd_fingers=46, resvdd_space=0.48,
        invvdd_n_mosfet=cast(_prm.MOSFET, _prims.nfet_g5v0d10v5),
        invvdd_n_l=0.5, invvdd_n_w=14.0, invvdd_n_fingers=7,
        invvdd_p_mosfet=cast(_prm.MOSFET, _prims.pfet_g5v0d10v5),
        invvdd_p_l=0.5, invvdd_p_w=7.0, invvdd_p_fingers=50,
        capvdd_l=10.0, capvdd_w=14.0, capvdd_fingers=5,
    )
    ioframespec = IOFrameSpecification(
        cell_height=188,
        tracksegment_viapitch=1.6,
        pad_width=79.0, pad_height=60.0, pad_viapitch=None,
        pad_viacorner_distance=23.0, pad_viametal_enclosure=3.0,
        tracksegment_maxpitch=21.0, tracksegment_space={
            None: 1.2,
            cast(_prm.MetalWire, _prims.m5): 4.0,
        },
        track_specs=(
            TrackSpecification(name="iovss", bottom=0.0, width=22.0),
            TrackSpecification(name="iovdd", bottom=90.0, width=43.8),
            TrackSpecification(name="secondiovss", bottom=142.0, width=10.0),
            TrackSpecification(name="vddvss", bottom=(188.0 - 31.0), width=30.0),
        ),
        pad_y=55.32,
    )

    def __init__(self, *,
        lib: _lbry.Library, cktfab: _ckt.CircuitFactory, layoutfab: _lay.LayoutFactory,
    ):
        super().__init__(
            lib=lib, cktfab=cktfab, layoutfab=layoutfab,
            spec=self.iospec, framespec=self.ioframespec,
        )


iolib = _lbry.Library(name="IOLib", tech=tech)
_iofab = Sky130IOFactory(lib=iolib, cktfab=cktfab, layoutfab=layoutfab)
# Generate the gallery and layout of all subcells. Layout generation is done so all
# cells exist in the library before merge is called.
_iofab.get_cell("Gallery").layout
merge(iolib)
