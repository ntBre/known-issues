import json
import logging
from collections import defaultdict
from typing import Union

import click
import numpy as np
from matplotlib import pyplot as plt
from openff.qcsubmit.results import (
    OptimizationResultCollection,
    TorsionDriveResultCollection,
)
from openff.toolkit import ForceField, Molecule
from openff.units import unit
from qcportal.models.torsiondrive import TorsionDriveRecord
from rdkit import Chem
from rdkit.Chem.Draw import MolsToGridImage, rdDepictor, rdMolDraw2D
from rdkit.Chem.rdmolops import RemoveHs

from latex import Latex
from timer import Timer

logging.getLogger("openff").setLevel(logging.ERROR)


def draw_rdkit(mol: Molecule, filename, smirks, show_all_hydrogens=True):
    """Draw `mol` using rdkit and write the resulting PNG to `filename`.

    `smirks` is a target smirks to highlight in the resulting image.
    Adapted from openff.toolkit.Molecule.visualize
    """
    matches = mol.chemical_environment_matches(smirks)
    rdmols = []
    highlight_atom_lists = []
    for m in matches:
        highlight_atom_lists.append(sorted(m))
        rdmol = mol.to_rdkit()
        if not show_all_hydrogens:
            rdmol = RemoveHs(rdmol, updateExplicitCount=True)
        rdDepictor.SetPreferCoordGen(True)
        rdDepictor.Compute2DCoords(rdmol)
        rdmol = rdMolDraw2D.PrepareMolForDrawing(rdmol)
        rdmols.append(rdmol)

    BASE = 450
    match len(rdmols):
        case 1:
            size = (BASE, BASE)
            per_row = 1
        case 2 | 3 | 4:
            size = (BASE // 2, BASE // 2)
            per_row = 2
        case 5 | 6:
            size = (BASE // 3, BASE // 3)
            per_row = 3
        case other:
            raise TypeError(f"failed to match rdmol len {other}")

    png = MolsToGridImage(
        rdmols,
        highlightAtomLists=highlight_atom_lists,
        subImgSize=size,
        molsPerRow=per_row,
        returnPNG=True,
    )

    with open(filename, "wb") as out:
        out.write(png)


def load_dataset(
    dataset: str,
) -> Union[OptimizationResultCollection, TorsionDriveResultCollection]:
    """Peeks at the first entry of `dataset` to determine its type and
    then loads it appropriately.

    Raises a `TypeError` if the first entry is neither a `torsion`
    record nor an `optimization` record.
    """
    with open(dataset, "r") as f:
        j = json.load(f)
    entries = j["entries"]
    keys = entries.keys()
    assert len(keys) == 1  # only handling this case for now
    key = list(keys)[0]
    match j["entries"][key][0]["type"]:
        case "torsion":
            return TorsionDriveResultCollection.parse_file(dataset)
        case "optimization":
            return OptimizationResultCollection.parse_raw(dataset)
        case t:
            raise TypeError(f"Unknown result collection type: {t}")


def plot_td_record(
    record: TorsionDriveRecord, molecule: Molecule, filename: str, smirks: str
):
    """Plot a torsion drive record.

    Adapted from Lily's plot-td-energy.ipynb
    """

    assert isinstance(record, TorsionDriveRecord)
    assert len(record.keywords.dihedrals) == 1
    assert isinstance(molecule, Molecule)
    # get energies
    energies = record.get_final_energies()
    x = sorted(energies)
    y = np.array([energies[x_] for x_ in x])
    hartree = y * unit.hartree * unit.avogadro_constant
    energy = hartree.m_as(unit.kilocalories_per_mole)
    energy -= min(energy)

    # get smiles and torsion specification
    dihedrals = record.keywords.dihedrals[0]
    rdmol = molecule.to_rdkit()
    rwmol = Chem.RWMol(rdmol)
    # label or remove atoms in reverse
    for i in list(range(molecule.n_atoms))[::-1]:
        if i in dihedrals:
            rwmol.GetAtomWithIdx(i).SetAtomMapNum(i)
        else:
            rwmol.RemoveAtom(i)
    torsion_smirks = Chem.MolToSmarts(rwmol)

    # plot
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.plot(x, energy)
    ax.set_xlabel("Rotation (°)")
    ax.set_ylabel("Relative energy [kcal mol$^{-1}$]")
    ax.set_title(f"{torsion_smirks}")
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()


@click.command()
@click.option("--target", required=True)
@click.option("--force-field", default="openff-2.1.0.offxml")
@click.option("--plot-torsions", is_flag=True, default=False)
@click.option(
    "--dataset",
    "datasets",
    multiple=True,
    default=["datasets/td-set-for-fitting-2.1.0.json"],
)
def check_coverage(target, force_field, datasets, plot_torsions):
    coverage = []
    # list of molecules involved in the target torsion
    involved_molecules = defaultdict(list)
    # list of records involved in the target torsion, parallel to above
    involved_records = defaultdict(list)

    ff = ForceField(force_field, allow_cosmetic_attributes=True)
    smirks = (
        ff.get_parameter_handler("ProperTorsions")
        .get_parameter(dict(id=target))[0]
        .smirks
    )
    timer = Timer()
    for dataset in datasets:
        timer.say("loading dataset")
        data = load_dataset(dataset)

        if plot_torsions:
            timer.say("converting dataset to records and molecules")
            molecules = data.to_records()
        else:
            timer.say("converting dataset to molecules")
            # flatten values
            data = [v for value in data.entries.values() for v in value]
            molecules = [
                # this seems a bit dangerous, but I should only inspect the
                # record if plot_torsions is true too
                (
                    None,
                    Molecule.from_mapped_smiles(
                        r.cmiles, allow_undefined_stereo=True
                    ),
                )
                for r in data
            ]

        h = ff.get_parameter_handler("ProperTorsions")

        timer.say("labeling torsions")
        results = defaultdict(int)
        for record, molecule in molecules:
            all_labels = ff.label_molecules(molecule.to_topology())[0]
            torsions = all_labels["ProperTorsions"]
            env = molecule.chemical_environment_matches(smirks)
            for atoms_involved, torsion in torsions.items():
                if atoms_involved in env or atoms_involved[::-1] in env:
                    results[torsion.id] += 1
                    involved_molecules[torsion.id].append(molecule)
                    involved_records[torsion.id].append(record)

        smirk = h.get_parameter(dict(id=target))[0].smirks
        coverage.append(f"{target:5}{results[target]:5}   {smirk}")

    length = max([len(s) for s in dataset])
    print("Coverage:")
    for ds, cover in zip(dataset, coverage):
        print(f"{ds:<{length}s} {cover}")

    lr = len(involved_records[target])
    lm = len(involved_molecules[target])
    assert lr == lm, f"{lr} records vs {lm} molecules"

    # filter duplicate molecules and use the indices to filter corresponding
    # records
    molecules = involved_molecules[target]
    records = involved_records[target]

    print("before", len(molecules), "and", len(records))
    # deduplicate molecules and records by molecule inchi
    mol_keys = {
        m.to_inchi(): i for i, m in enumerate(involved_molecules[target])
    }
    molecules = [m for i, m in enumerate(molecules) if i in mol_keys.values()]
    records = [r for i, r in enumerate(records) if i in mol_keys.values()]

    print("deduplicated to", len(molecules), "and", len(records))

    out = Latex()
    if plot_torsions:
        for i, (r, m) in enumerate(zip(records, molecules)):
            # filter by ensuring the record's dihedrals are actually a match to
            # the smirks of interest
            assert len(r.keywords.dihedrals) == 1, "not sure what to do here"
            d = r.keywords.dihedrals[0]
            e = m.chemical_environment_matches(smirks)
            if d in e or d[::-1] in e:
                # draw the molecule
                filename = f"mol{i:02d}.png"
                draw_rdkit(m, f"output/{filename}", smirks)
                out.add_image(filename, caption=m.to_smiles())
                # draw the plot
                filename = f"plot{i:02d}.png"
                plot_td_record(r, m, f"output/{filename}", smirks)
                out.add_image(filename, caption=m.to_smiles())
    else:
        # just the molecule
        for i, m in enumerate(molecules):
            filename = f"mol{i:02d}.png"
            draw_rdkit(m, f"output/{filename}", smirks)
            out.add_image(filename, caption=m.to_smiles())

    timer.say("writing output")
    out.to_file("output/report.tex")


if __name__ == "__main__":
    check_coverage()
