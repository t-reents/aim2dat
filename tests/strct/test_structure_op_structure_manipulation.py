"""Test  structure manipulation funcitons of the StructureCollection class."""

# Standard library imports
import os

# Third party library imports
import pytest

# Internal library imports
from aim2dat.strct import StructureOperations, StructureCollection
from aim2dat.strct.ext_manipulation import add_functional_group
from aim2dat.io.yaml import load_yaml_file

STRUCTURES_PATH = os.path.dirname(__file__) + "/structures/"
STRUCTURE_MANIPULATION_PATH = os.path.dirname(__file__) + "/structure_manipulation/"


@pytest.mark.parametrize("structure", ["Benzene"])
def test_delete_atoms(structure_comparison, structure):
    """Test delete atoms method."""
    inputs = dict(load_yaml_file(STRUCTURES_PATH + structure + ".yaml"))
    ref_p = load_yaml_file(STRUCTURE_MANIPULATION_PATH + structure + "_ref.yaml")
    ref_p["structure"]["label"] = structure

    strct_collect = StructureCollection()
    strct_collect.append(structure, **inputs)
    strct_ops = StructureOperations(strct_collect, append_to_coll=False)
    new_strct = strct_ops.delete_atoms(structure, **ref_p["function_args"], change_label=True)
    ref_p["structure"]["label"] += "_del"
    structure_comparison(new_strct, ref_p["structure"])


@pytest.mark.parametrize("structure", ["Cs2Te_62_prim", "GaAs_216_prim"])
def test_element_substitution(structure_comparison, structure):
    """Test element substitution method."""
    inputs = dict(load_yaml_file(STRUCTURES_PATH + structure + ".yaml"))
    inputs["label"] = structure
    inputs2 = dict(load_yaml_file(STRUCTURES_PATH + "Al_225_conv.yaml"))
    inputs2["label"] = "Al_test"
    ref_p = load_yaml_file(STRUCTURE_MANIPULATION_PATH + structure + "_ref.yaml")
    strct_collect = StructureCollection()
    strct_collect.append(**inputs)
    strct_collect.append(**inputs2)
    strct_ops = StructureOperations(strct_collect, append_to_coll=True)
    elements = ref_p["function_args"]["elements"]
    elements = elements if isinstance(elements[0], (list, tuple)) else [elements]
    strct_ops.substitute_elements([0], **ref_p["function_args"], change_label=True)
    assert len(strct_ops.structures) == 3
    structure_comparison(strct_ops.structures[0], inputs)
    structure_comparison(strct_ops.structures[1], inputs2)
    structure_comparison(strct_ops.structures[2], ref_p["structure"])


def test_add_functional_group(structure_comparison):
    """Test add functional group function."""
    inputs = dict(load_yaml_file(STRUCTURES_PATH + "Sc2BDC3.yaml"))
    ref_p = load_yaml_file(STRUCTURE_MANIPULATION_PATH + "Sc2BDC3_ref.yaml")
    ref_p["label"] = "test"
    strct_collect = StructureCollection()
    strct_collect.append(**inputs, label="test")
    strct_ops = StructureOperations(strct_collect, append_to_coll=True)
    strct_ops.perform_manipulation(
        0,
        method=add_functional_group,
        kwargs={
            "wrap": True,
            "host_index": 37,
            "functional_group": "H",
            "bond_length": 1.0,
            "change_label": False,
        },
    )
    strct_ops.perform_manipulation(
        0,
        method=add_functional_group,
        kwargs={
            "wrap": True,
            "host_index": 39,
            "functional_group": "CH3",
            "bond_length": 1.1,
            "change_label": False,
        },
    )
    strct_ops.perform_manipulation(
        0,
        method=add_functional_group,
        kwargs={"host_index": 41, "functional_group": "COOH", "change_label": False},
    )
    strct_ops.perform_manipulation(
        0,
        method=add_functional_group,
        kwargs={"host_index": 42, "functional_group": "NH2", "change_label": False},
    )
    strct_ops.perform_manipulation(
        0,
        method=add_functional_group,
        kwargs={"host_index": 62, "functional_group": "NO2", "change_label": False},
    )
    strct_ops.perform_manipulation(
        0,
        method=add_functional_group,
        kwargs={"host_index": 74, "functional_group": "OH", "change_label": False},
    )
    strct_ops.structures[0].set_positions(strct_ops.structures[0].positions, wrap=True)
    structure_comparison(strct_ops.structures[0], ref_p)


@pytest.mark.parametrize("new_label", ["GaAs_216_prim", "GaAs_216_prim_scaled-0.7"])
def test_scale_unit_cell(structure_comparison, new_label):
    """Test scale unit cell function."""
    inputs = dict(load_yaml_file(STRUCTURES_PATH + "GaAs_216_prim.yaml"))
    ref = dict(
        load_yaml_file(STRUCTURE_MANIPULATION_PATH + "GaAs_216_prim_scale_unit_cell_ref.yaml")
    )
    ref["structure"]["label"] = new_label
    strct_c = StructureCollection()
    strct_c.append("GaAs_216_prim", **inputs)
    strct_ops = StructureOperations(strct_c, append_to_coll=True)
    strct_ops.scale_unit_cell(
        "GaAs_216_prim", **ref["function_args"], change_label="scaled" in new_label
    )
    structure_comparison(strct_c[new_label], ref["structure"])
