from openff.toolkit import Molecule
from rdkit.Chem.Draw import rdDepictor, rdMolDraw2D
from rdkit.Chem.rdmolops import RemoveHs


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
