from collections import defaultdict

from openff.qcsubmit.results import TorsionDriveResultCollection
from openff.toolkit import ForceField


def check_coverage():
    ff = "openff-2.1.0.offxml"
    dataset = "td-set-for-fitting-2.1.0.json"
    target = "t129"

    print("loading forcefield and dataset")
    ff = ForceField(ff, allow_cosmetic_attributes=True)
    td_data = TorsionDriveResultCollection.parse_file(dataset)

    print("converting dataset to records")
    h = ff.get_parameter_handler("ProperTorsions")
    records_and_molecules = td_data.to_records()

    print("labeling torsions")
    results = defaultdict(int)
    for _, molecule in records_and_molecules:
        all_labels = ff.label_molecules(molecule.to_topology())[0]
        torsions = all_labels["ProperTorsions"]
        for torsion in torsions.values():
            results[torsion.id] += 1

    print("Coverage:")
    smirk = h.get_parameter(dict(id=target))[0].smirks
    print(f"{target:5}{results[target]:5}   {smirk}")


if __name__ == "__main__":
    check_coverage()
