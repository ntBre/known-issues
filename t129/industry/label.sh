#!/bin/bash

# mol00.png   [H]c1c(c(c(c(c1[H])[H])N2C(=NOS2)C3=C(C(=O)Oc4c3c(c(c(c4[H])[H])[H])[H])[H])[H])[H]
# mol16.png   [H]c1c(c(c(c(c1C2=NO[C@@]3([C@]2(C(N(C3([H])[H])C(=O)OC(C([H])([H])[H])(C([H])([H])[H])C([H])([H])[H])([H])[H])[H])[H])[H])[H])Cl)[H]
# mol24.png   [H]c1c(c(c(c(c1[H])c2c(c3c(c(c2[H])Cl)N(C(=N3)C4=NOC5(C4([H])[H])C(C(C(C(C5([H])[H])([H])[H])([H])[H])([H])[H])([H])[H])[H])[H])F)[H])[H]
# mol43.png   [H]c1c(c(c(c(c1C(=O)C2=C([N-]N(C2=O)C([H])([H])[H])[H])C([H])([H])[H])C3=NOC(C3([H])[H])([H])[H])S(=O)(=O)C([H])([H])[H])[H]
# mol55.png   [H]c1c(c(c(c(c1[H])c2c(c(c3c(n2)N=C(N3[H])C4=NOC5(C4([H])[H])C(C(C(C(C5([H])[H])([H])[H])([H])[H])([H])[H])([H])[H])[H])[H])C(F)(F)F)[H])[H]
# mol91.png   [H]c1c(c(c(c(c1[H])c2c(c(c3c(c2C([H])([H])[H])N(C(=N3)C4=NOC5(C4([H])[H])C(C(C(C(C5([H])[H])([H])[H])([H])[H])([H])[H])([H])[H])[H])C([H])([H])[H])[H])C(F)(F)F)[H])[H]
# mol106.png  [H]c1c(c(c(c(c1[H])c2c(c3c(c(c2[H])Br)N(C(=N3)C4=NOC5(C4([H])[H])C(C(OC(C5([H])[H])([H])[H])([H])[H])([H])[H])[H])[H])C(F)(F)F)[H])[H]
# mol107.png  [H]c1c(c(c(c(c1[H])c2c(c3c(c(c2[H])Cl)N=C(N3[H])C4=NOC5(C4([H])[H])C(C(C(C(C5([H])[H])([H])[H])(C([H])([H])[H])C([H])([H])[H])([H])[H])([H])[H])[H])C(F)(F)F)[H])[H]
# mol110.png  [H]c1c(c(c2c(c1[H])C3=NO[C@]([C@@]3(C(O2)([H])[H])[H])([H])C([H])([H])N4C(C(N(C(C4([H])[H])([H])[H])C([H])([H])C([H])([H])[H])([H])[H])([H])[H])[H])[H]
# mol123.png  [H]c1c(c(c(c(c1[H])F)c2c(c(c3c(c2[H])N=C(N3[H])C4=NOC5(C4([H])[H])C(C(C(C(C5([H])[H])([H])[H])([H])[H])([H])[H])([H])[H])[H])[H])OC(F)(F)F)[H]
# mol139.png  [H]c1c(c(c(c(c1[H])[H])[C@]2(C(C(=NO2)c3c(c(c4c(c3[H])N=C(N(C4=O)[H])[H])[H])[H])([H])[H])C([H])([H])[H])[H])[H]
# mol156.png  [H]c1c(c(c(c(c1[H])c2c(c(c3c(c2[H])N(C(=N3)C4=NOC5(C4([H])[H])C(C(C(C(C5([H])[H])([H])[H])([H])[H])([H])[H])([H])[H])[H])C(F)(F)F)[H])Cl)[H])[H]
# mol185.png  [H]c1c(c(c(c(c1[H])[H])[C@@]2(C(C(=NO2)c3c(c(c4c(c3[H])C(C(C(=C4[H])[H])([H])[H])([H])[H])[H])[H])([H])[H])[H])[H])[H]
# mol199.png  [H]c1c(c(c(c(c1[H])[H])C2=NO[C@](C2([H])[H])([H])c3c(c(c4c(c3[H])C(=O)N(C(=N4)[H])[H])[H])[H])[H])[H]
# mol223.png  [H]c1c(c(c(c(c1C2=NO[C@@](C2([H])[H])([H])C3=Nc4c(c(c(c(c4C(=O)O3)[H])Cl)[H])[H])[H])[H])Cl)[H]
# mol239.png  [H]c1c(c(c(c(c1[H])c2c(c(c3c(c2[H])N=C(N3[H])C4=NOC5(C4([H])[H])C(C(OC(C5([H])[H])([H])[H])([H])[H])([H])[H])[H])[H])Cl)[H])[H]

mols=( mol00.png mol16.png mol24.png mol43.png mol55.png mol91.png mol106.png
    mol107.png mol110.png mol123.png mol139.png mol156.png mol185.png mol199.png
    mol223.png mol239.png )

labels=(
    '[H]c1c(c(c(c(c1[H])[H])N2C(=NOS2)C3=C(C(=O)Oc4c3c(c(c(c4[H])[H])[H])[H])[H])[H])[H]'
    '[H]c1c(c(c(c(c1C2=NO[C@@]3([C@]2(C(N(C3([H])[H])C(=O)OC(C([H])([H])[H])(C([H])([H])[H])C([H])([H])[H])([H])[H])[H])[H])[H])[H])Cl)[H]'
    '[H]c1c(c(c(c(c1[H])c2c(c3c(c(c2[H])Cl)N(C(=N3)C4=NOC5(C4([H])[H])C(C(C(C(C5([H])[H])([H])[H])([H])[H])([H])[H])([H])[H])[H])[H])F)[H])[H]'
    '[H]c1c(c(c(c(c1C(=O)C2=C([N-]N(C2=O)C([H])([H])[H])[H])C([H])([H])[H])C3=NOC(C3([H])[H])([H])[H])S(=O)(=O)C([H])([H])[H])[H]'
    '[H]c1c(c(c(c(c1[H])c2c(c(c3c(n2)N=C(N3[H])C4=NOC5(C4([H])[H])C(C(C(C(C5([H])[H])([H])[H])([H])[H])([H])[H])([H])[H])[H])[H])C(F)(F)F)[H])[H]'
    '[H]c1c(c(c(c(c1[H])c2c(c(c3c(c2C([H])([H])[H])N(C(=N3)C4=NOC5(C4([H])[H])C(C(C(C(C5([H])[H])([H])[H])([H])[H])([H])[H])([H])[H])[H])C([H])([H])[H])[H])C(F)(F)F)[H])[H]'
    '[H]c1c(c(c(c(c1[H])c2c(c3c(c(c2[H])Br)N(C(=N3)C4=NOC5(C4([H])[H])C(C(OC(C5([H])[H])([H])[H])([H])[H])([H])[H])[H])[H])C(F)(F)F)[H])[H]'
    '[H]c1c(c(c(c(c1[H])c2c(c3c(c(c2[H])Cl)N=C(N3[H])C4=NOC5(C4([H])[H])C(C(C(C(C5([H])[H])([H])[H])(C([H])([H])[H])C([H])([H])[H])([H])[H])([H])[H])[H])C(F)(F)F)[H])[H]'
    '[H]c1c(c(c2c(c1[H])C3=NO[C@]([C@@]3(C(O2)([H])[H])[H])([H])C([H])([H])N4C(C(N(C(C4([H])[H])([H])[H])C([H])([H])C([H])([H])[H])([H])[H])([H])[H])[H])[H]'
    '[H]c1c(c(c(c(c1[H])F)c2c(c(c3c(c2[H])N=C(N3[H])C4=NOC5(C4([H])[H])C(C(C(C(C5([H])[H])([H])[H])([H])[H])([H])[H])([H])[H])[H])[H])OC(F)(F)F)[H]'
    '[H]c1c(c(c(c(c1[H])[H])[C@]2(C(C(=NO2)c3c(c(c4c(c3[H])N=C(N(C4=O)[H])[H])[H])[H])([H])[H])C([H])([H])[H])[H])[H]'
    '[H]c1c(c(c(c(c1[H])c2c(c(c3c(c2[H])N(C(=N3)C4=NOC5(C4([H])[H])C(C(C(C(C5([H])[H])([H])[H])([H])[H])([H])[H])([H])[H])[H])C(F)(F)F)[H])Cl)[H])[H]'
    '[H]c1c(c(c(c(c1[H])[H])[C@@]2(C(C(=NO2)c3c(c(c4c(c3[H])C(C(C(=C4[H])[H])([H])[H])([H])[H])[H])[H])([H])[H])[H])[H])[H]'
    '[H]c1c(c(c(c(c1[H])[H])C2=NO[C@](C2([H])[H])([H])c3c(c(c4c(c3[H])C(=O)N(C(=N4)[H])[H])[H])[H])[H])[H]'
    '[H]c1c(c(c(c(c1C2=NO[C@@](C2([H])[H])([H])C3=Nc4c(c(c(c(c4C(=O)O3)[H])Cl)[H])[H])[H])[H])Cl)[H]'
    '[H]c1c(c(c(c(c1[H])c2c(c(c3c(c2[H])N=C(N3[H])C4=NOC5(C4([H])[H])C(C(OC(C5([H])[H])([H])[H])([H])[H])([H])[H])[H])[H])Cl)[H])[H]'
)

# for i in ${!mols[@]}; do
#     mol=${mols[$i]}
#     label=${labels[$i]}
#     out=${mol%.png}.label.png
#     convert $mol label:$label -gravity Center -append $out
# done
# montage ${mols[@]} -geometry 450x450\> -tile 4x4 non-aromatic.png

echo ${mols[@]}
