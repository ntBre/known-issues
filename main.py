import logging
from collections import defaultdict

import click
from openff.qcsubmit.results import TorsionDriveResultCollection
from openff.toolkit import ForceField, Molecule
from rdkit.Chem.Draw import MolsToGridImage
from rdkit.Chem.rdmolops import RemoveHs

from latex import Latex

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
        rdmols.append(rdmol)

    png = MolsToGridImage(
        rdmols,
        highlightAtomLists=highlight_atom_lists,
        subImgSize=(300, 300),
        molsPerRow=1,
        returnPNG=True,
    )

    with open(filename, 'wb') as out:
        out.write(png)


@click.command()
@click.option("--target", required=True)
@click.option("--force-field", default="openff-2.1.0.offxml")
@click.option(
    "--dataset",
    "datasets",
    multiple=True,
    default=["datasets/td-set-for-fitting-2.1.0.json"],
)
def check_coverage(target, force_field, datasets):
    coverage = []
    involved_molecules = defaultdict(set)

    ff = ForceField(force_field, allow_cosmetic_attributes=True)
    smirks = (
        ff.get_parameter_handler("ProperTorsions")
        .get_parameter(dict(id=target))[0]
        .smirks
    )
    for dataset in datasets:
        print("loading forcefield and dataset")
        td_data = TorsionDriveResultCollection.parse_file(dataset)

        print("converting dataset to molecules")
        td_data = [v for value in td_data.entries.values() for v in value]
        molecules = [
            Molecule.from_mapped_smiles(r.cmiles, allow_undefined_stereo=True)
            for r in td_data
        ]

        h = ff.get_parameter_handler("ProperTorsions")

        print("labeling torsions")
        results = defaultdict(int)
        for molecule in molecules:
            all_labels = ff.label_molecules(molecule.to_topology())[0]
            torsions = all_labels["ProperTorsions"]
            for torsion in torsions.values():
                results[torsion.id] += 1
                involved_molecules[torsion.id].add(molecule)

        smirk = h.get_parameter(dict(id=target))[0].smirks
        coverage.append(f"{target:5}{results[target]:5}   {smirk}")

    length = max([len(s) for s in dataset])
    print("Coverage:")
    for ds, cover in zip(dataset, coverage):
        print(f"{ds:<{length}s} {cover}")

    out = Latex()
    c = 0
    for m in involved_molecules[target]:
        filename = f"mol{c:02d}.png"
        draw_rdkit(m, f"output/{filename}", smirks)
        out.add_image(filename, caption=m.to_smiles())
        c += 1
    out.to_file("output/report.tex")


if __name__ == "__main__":
    check_coverage()
