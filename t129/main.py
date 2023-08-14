import logging
from collections import defaultdict

from openff.qcsubmit.results import TorsionDriveResultCollection
from openff.toolkit import ForceField, Molecule

logging.getLogger("openff").setLevel(logging.ERROR)


def check_coverage():
    ff_name = "openff-2.1.0.offxml"
    target = "t129"

    datasets = [
        # from
        # sage-2.1.0/inputs-and-outputs/data-sets/td-set-for-fitting-2.1.0.json
        "td-set-for-fitting-2.1.0.json",
        # from valence-fitting/02_curate-data/datasets/filtered-sage-td.json
        "filtered-sage-td.json",
        # from valence-fitting/02_curate-data/datasets/filtered-td.json
        "filtered-td.json",
    ]
    coverage = []

    for dataset in datasets:
        print("loading forcefield and dataset")
        ff = ForceField(ff_name, allow_cosmetic_attributes=True)
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

        smirk = h.get_parameter(dict(id=target))[0].smirks
        coverage.append(f"{target:5}{results[target]:5}   {smirk}")

    length = max([len(s) for s in datasets])
    print("Coverage:")
    for ds, cover in zip(datasets, coverage):
        print(f"{ds:<{length}s} {cover}")


if __name__ == "__main__":
    check_coverage()
