import logging
from collections import defaultdict

import click
from openff.qcsubmit.results import TorsionDriveResultCollection
from openff.toolkit import ForceField, Molecule
from rdkit.Chem.Draw import rdDepictor, rdMolDraw2D
from rdkit.Chem.rdmolops import RemoveHs

from latex import Latex

logging.getLogger("openff").setLevel(logging.ERROR)


def draw_rdkit(mol: Molecule, filename, show_all_hydrogens=True):
    """Draw `mol` using rdkit and write the resulting PNG to `filename`.

    Adapted from openff.toolkit.Molecule.visualize
    """
    rdmol = mol.to_rdkit()
    if not show_all_hydrogens:
        rdmol = RemoveHs(rdmol, updateExplicitCount=True)
    rdDepictor.SetPreferCoordGen(True)
    rdDepictor.Compute2DCoords(rdmol)
    rdmol = rdMolDraw2D.PrepareMolForDrawing(rdmol)

    drawer = rdMolDraw2D.MolDraw2DCairo(300, 300)
    drawer.DrawMolecule(rdmol)
    drawer.FinishDrawing()

    drawer.WriteDrawingText(filename)


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

    for dataset in datasets:
        print("loading forcefield and dataset")
        ff = ForceField(force_field, allow_cosmetic_attributes=True)
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
        draw_rdkit(m, f"output/{filename}")
        out.add_image(filename, caption=m.to_smiles())
        c += 1
    out.to_file("output/report.tex")


if __name__ == "__main__":
    check_coverage()
