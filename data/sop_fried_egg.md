# SOP: Fried egg (G1 test procedure)

Shot from 30-60 cm, indoors, no faces, no screens. Photo names: `egg_s<step>_<pass|fail>_<n>.jpg` in `data/raw/`. Truth labels go in `data/labels.csv`.

| Step | Instruction | Pass looks like | Fail looks like (stage on purpose) | Photos |
|---|---|---|---|---|
| S1 | Put oil in the pan | Pan has a visible oil sheen or pool | Dry pan | 1 pass, 1 fail |
| S2 | Crack the egg into the pan, no shell | Egg in pan, no shell pieces | A shell piece visible in or on the egg | 1 pass, 1 fail |
| S3 | Cook until the whites are fully set | Whites opaque white | Whites still clear / glossy raw | 1 pass, 1 fail |
| S4 | Finish without burning | Golden or white edges | Dark brown or black edges | 1 pass, 1 fail |
| S5 | Plate the egg | Egg on a plate | Plate empty, egg still in pan | 1 pass, 1 fail |

10 photos total (5 pass, 5 fail), about 4-6 eggs. Vary angle and lighting a little.
