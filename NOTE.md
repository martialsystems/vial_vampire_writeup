# Closed-vial vampire claims: note

Locks stay on the trees. Index: gist [12835f74](https://gist.github.com/martialsystems/12835f747d6360781f3cc7f91f243178).

## Abstract

Two questions. First: under an explicit diet ladder and an allowed population crash, does a Drosophila-like sponging labellum evolve prestomal-tooth rasping and a costly bite that becomes the host meal, with F off 1? Second: can diploid sponging flies live on vertebrate blood already in an engorged mosquito, without a mammal-biting pierce kit?

Parent engine [fly_vial](https://github.com/martialsystems/fly_vial) `@e2e22b7`: k=3, seed 1, N=1,000, 80 generations, IBD F = 0.524 versus random F = 0.034. Census held. Courtship fell on both arms.

[vial_sanguis](https://github.com/martialsystems/vial_sanguis) `@97aa7c8` (index still names `@b7347ce`): crash and exudate recovery are repeatable. Random flickers a biter and loses it. k-NN majority kit at F=1. Origin seed-1 knn: `t_first_biter=211`, census to 3 at t=6, recovered t=28, majority t=1,468, at t=2,500 n=1,200, F=1.000, p_biter=1. Kinship cap `phi_max=0.25`: two of three seeds, F about 0.24. Closing wounds and tears/sweat together extincts everyone. Engine retired.

[vial_sanguis2](https://github.com/martialsystems/vial_sanguis2) science `4946ab5` `@7e32830`: delayed cap plus pair fallback. One of three k-NN seeds held a kit at F about 0.23. That kit is exudate. Peak bite share 5.74% at t=4,644 with p_biter=1. Sweat plus wound at least 93.34% of host after hold. Vampire-as-bite fails as a 3-seed claim and as a meal share.

[vial_morsus](https://github.com/martialsystems/vial_morsus) science `b106228` `@69f4f6d`: decaying exudate bridge `T_bridge=400`. 0 of 3 k-NN. Recovered from crash, lived on the bridge, extinct when exudate hit 0 around t=400. Bite share never held at 0.50. Mid-bridge sweat plus wound about 0.98.

[vial_culex](https://github.com/martialsystems/vial_culex) science `fa819c7` `@ddb73a8`: blank fruit founders. 0 of 3 k-NN. Extinct at t=5. Cargo still 200. Stolen share 0. They never found the mosquito.

[vial_handoff](https://github.com/martialsystems/vial_handoff) science `e843b8c` `@12d6952`: living morsus k-NN at t=200 into the culex kitchen. 0 of 3. Hemolymph share 1.000. Stolen share at most 0.000067. gut_probe stayed untrained. Fail-predator.

Halt on every vampire tree.

## 1. Questions

Q1. Under an explicit diet ladder and an allowed population crash, does a Drosophila-like sponging labellum evolve prestomal-tooth rasping and then a costly bite, and how many generations / how deep a bottleneck does that take?

Q1b. Can that kit hold with F off 1 if kinship cap waits until after recovery and falls back to random pairing instead of vetoing every pair?

Q1c. After fruit is gone, does a prestomal rasp plus shallow bite become the majority of host calories on a decaying exudate bridge, with F off 1, on at least two of three seeds?

Q2. Can diploid sponging flies switch from fruit to stealing vertebrate blood already in an engorged mosquito, then find the next mosquito, without evolving a mammal-biting pierce kit?

Q2b. If living mid-bridge morsus k-NN flies (already past fruit-off, already rasping films) are put in the culex kitchen (finite engorged mosquitoes, no mammal skin, no exudate), can they add a gut probe and live on stolen midgut blood?

PASS on Q1c, Q2, Q2b is at least two of three k-NN seeds. 0 of 3 is a fail. Do not average.

## 2. Engine

Closed-form diploid QTL vial. Mating is k=3 nearest-neighbor on morphology plus courtship QTLs, or random. Hidden recessive load is excluded from similarity. F is founder-allele IBD, `1 - H_t/H_0`. Census ceiling 1,200 after the parent 1,000. Extinction is logged.

fly_vial `@e2e22b7` is fruit only, 80 generations, N=1,000. Assortative F = 0.524 versus random F = 0.034 on seed 1. Wright random-mating form 1-(1-1/2000)^80 ≈ 0.039. Courtship t=1 to t=80: 0.934 to 0.595 assortative, 0.930 to 0.599 random. The courtship drop is not the assortative signature. Logs: `logs/assort_80.json`, `logs/random_80.json`. Do not restamp 0.524 / 0.034.

Vampire trees add a diet ladder. Fruit off at `t_starve=5`. Host channels: tears (`k_tears=40`), sweat, wound, bite. `bite_weight=1.0`. Standing costs on unused pierce, digest, heme_safe. `phi_max=0.25` when the cap is on. `z_max=3.0` from sanguis2 on. Fruit-forever is the negative control.

## 3. Vampire-as-bite

### 3.1 vial_sanguis (2026-09-16)

Six vials, k=3, N=1,000, 2,500 generations, t_starve=5.

| seed | mate | min n | t_recover | flicker | t_held_biter | t_majority | final F | final p_biter |
|-----:|------|------:|----------:|--------:|-------------:|-----------:|--------:|--------------:|
| 1 | knn | 3 | 28 | 211 | 1,108 | 1,468 | 1.000 | 1.000 |
| 1 | random | 1 |  |  |  |  | extinct t=11 | 0 |
| 2 | knn | 18 | 22 | 412 | 638 | 1,211 | 1.000 | 0.914 |
| 2 | random | 6 | 16 | 162 |  |  | 0.821 | 0 |
| 3 | knn | 13 | 21 | 792 | 1,111 | 1,301 | 1.000 | 0.998 |
| 3 | random | 6 | 22 | 128 |  |  | 0.830 | 0 |

Fruit-forever to t=400: p_biter=0. Origin lock `logs/vampire_2500_s1.json`: `t_first_biter=211`.

Kinship cap `phi_max=0.25`: two of three seeds, F about 0.24 at 10k. Pierce still moved. Saliva did not. Seed 3 extinct at t=9.

Cap after recover: seed 1 extinct t=12 (all pairs vetoed). Seeds 2 and 3 held biters at F=0.238 / 0.236.

Host shift after hold: p_biter collapsed (0.005 / 0.007). Saliva left the negative region. Pierce did not keep rising.

Scab plus exudate-cap: closing wounds and tears/sweat together extincts both lines in one generation. Cliff. `bite_weight` stayed 1.0. Halt. Successor vial_sanguis2.

### 3.2 vial_sanguis2 (2026-09-16)

Delayed cap (`n>=50` after starve, then `phi_max=0.25`). If the cap would accept fewer than 8 pairs, that generation uses random pairing.

| seed | mate | min n | t_recover | flicker | t_held | F@1500 | F@2500 | final p_biter | fallback gens |
|-----:|------|------:|----------:|--------:|-------------:|-------:|-------:|--------------:|--------------:|
| 1 | fallback-dominated | 2 | 28 | 128 |  | 0.887 | 0.939 | 0.001 | 2,490 |
| 1 | random | 7 | 19 | 137 |  | 0.680 | 0.805 | 0 | 0 |
| 2 | knn delayed-cap | 1 |  |  |  |  |  | extinct t=11 | 0 |
| 2 | random | 3 |  |  |  |  |  | extinct t=5 | 0 |
| 3 | knn delayed-cap | 11 | 21 | 109 | 754 | 0.228 | 0.236 | 0.936 | 1 |
| 3 | random | 23 | 16 | 142 |  | 0.578 | 0.760 | 0 | 0 |

Seed 1 is not a delayed-cap result. Seed 2 is bottleneck extinction. Seed 3 held a kit.

Host calories from `logs/knn_delayed_2500_s3.json` and `logs/knn_delayed_10000_s3.json`. Host calories: tears + sweat + usable_blood. Wound and bite split usable_blood in proportion to the logged channel means.

| t | p_biter | F | tears % | sweat % | wound % | bite % | sweat+wound % |
|--:|--------:|--:|--------:|--------:|--------:|-------:|--------------:|
| 754 hold | 0.058 | 0.236 | 1.32 | 52.20 | 45.42 | 1.06 | 97.62 |
| 2,500 | 0.936 | 0.236 | 0.95 | 57.25 | 39.49 | 2.31 | 96.74 |
| 4,644 peak bite | 1.000 | 0.223 | 0.91 | 55.08 | 38.26 | 5.74 | 93.34 |
| 10,000 | 0.066 | 0.228 | 0.97 | 58.32 | 40.57 | 0.15 | 98.88 |

After t_held=754, sweat+wound is at least 93.34% of host. Peak bite share is 5.74%. `p_biter` counts flies with non-zero `energy_bite` on an exudate meal. Science `4946ab5`. End of vial_sanguis2.

### 3.3 vial_morsus (2026-09-16)

The standing film is replaced by a decaying bridge (`T_bridge=400` after first `n>=50` post-starve). Then only bite is host food.

| seed | mate | crash min n | t_recover | last live t | last n | last F | sw+wnd | bite share | extinct |
|-----:|------|------------:|----------:|------------:|-------:|-------:|-------:|-----------:|:-------:|
| 1 | knn | 11 | 8 | 400 | 4 | 0.250 | 0.788 | 0 | yes |
| 2 | knn | 17 | 8 | 399 | 11 | 0.253 | 0.783 | 0.00016 | yes |
| 3 | knn | 38 | 6 | 398 | 8 | 0.264 | 0.770 | 0 | yes |
| 1 | random | 4 | 7 | 400 | 2 | 0.722 | 0.625 | 0.215 | yes |
| 2 | random | 4 | 7 | 400 | 16 | 0.521 | 0.801 | 0.00030 | yes |
| 3 | random | 12 | 7 | 398 | 8 | 0.542 | 0.787 | 0.000017 | yes |
| 1 | fruit-forever |  |  | 400 | 1,200 | 0.488 | 0 | 0.0000036 | no |

Mid-bridge (t_recover+200) every starve arm sat at n=1,200 with sweat+wound about 0.98. Rasp rose; pierce did not. When exudate_scale hit 0, census collapsed. 0 of 3 k-NN. Do not raise `bite_weight`. Science `b106228`. Halt. No 10k arm.

## 4. Vampire-as-mosquito-thief

### 4.1 vial_culex (2026-09-16)

Blank founders. Mosquito is the host. Stolen midgut blood and hemolymph are separate liquids. M0=200 at t_starve, arrivals a0=8 per generation.

| seed | mate | last live t | last live n | last live F | t_end | cargo at t=5 | stolen share | hemolymph share | extinct |
|-----:|------|------------:|------------:|------------:|------:|-------------:|-------------:|----------------:|:-------:|
| 1 | knn | 4 | 1,200 | 0.008 | 5 | 200 | 0 | 0 | yes |
| 2 | knn | 4 | 1,200 | 0.004 | 5 | 200 | 0 | 0 | yes |
| 3 | knn | 4 | 1,200 | 0.007 | 5 | 200 | 0 | 0 | yes |
| 1 | random | 4 | 1,200 | 0.001 | 5 | 200 | 0 | 0 | yes |
| 2 | random | 4 | 1,200 | 0.001 | 5 | 200 | 0 | 0 | yes |
| 3 | random | 4 | 1,200 | 0.001 | 5 | 200 | 0 | 0 | yes |
| 1 | fruit-forever | 400 | 1,200 | 0.551 | 400 | 0 | 0 | 0 | no |

None lived on hemolymph. None drained cargo. 0 of 3 k-NN. Science `fa819c7`. Halt. A hand-off of living morsus genomes is a different git.

### 4.2 vial_handoff (2026-09-16)

Mapped full living census at morsus t=200 (n=1,200, sweat+wound about 0.98). rasp copied to cuticle_rasp. find_mosquito = 0.5 fluid_detect + 0.5 seek. pierce not mapped. gut_probe ~ N(0, 0.08). Exudate off. Hemolymph meals kill bodies.

| seed | mate | F@200 | rasp | find | n@2500 | stolen | hemolymph | probe end | PASS |
|-----:|------|------:|-----:|-----:|-------:|-------:|----------:|----------:|:----:|
| 1 | knn | 0.235 | 1.000 | 0.343 | 1,200 | 0.000001 | 1.000 | -0.475 | no |
| 2 | knn | 0.218 | 0.800 | 0.376 | 1,200 | 0 | 1.000 | -0.386 | no |
| 3 | knn | 0.230 | 0.833 | 0.281 | 1,200 | 0.000067 | 1.000 | -0.278 | no |
| 1 | fruit-forever | 0.235 | 1.000 | 0.343 | 1,200 at t=400 | 0.00081 | 0.111 | -0.046 | control |
| 1 | random | 0.235 | 1.000 | 0.343 | 1,200 | 0.000011 | 1.000 | -0.908 | contrast |

killed/gen=8 on every arm. map probe at snap is about 0. Film-rasp flies became mosquito predators (rasp × find). They did not add a gut probe. Fruit-forever stolen share 0.00081 < 0.05. 0 of 3 k-NN. Science `e843b8c`. Halt. No 10k.

## 5. Repo table

| Tree | SHA | Allowed sentence | Lock file |
|------|-----|------------------|-----------|
| [fly_vial](https://github.com/martialsystems/fly_vial) | `e2e22b7` | k=3, seed 1, N=1,000, 80 generations: F = 0.524 vs random F = 0.034. Census held. Courtship fell on both arms. | `logs/assort_80.json` |
| [vial_sanguis](https://github.com/martialsystems/vial_sanguis) | `97aa7c8` | Crash and exudate recovery are repeatable. k-NN majority kit at F=1. Kinship cap two of three at F about 0.24. Exudate-cap is a cliff. | `logs/vampire_2500_s1.json` |
| [vial_sanguis2](https://github.com/martialsystems/vial_sanguis2) | `7e32830` | Delayed-cap can hold F about 0.23. Peak bite share 5.74%. Sweat plus wound at least 93.34% of host. Science 4946ab5. | `logs/knn_delayed_2500_s3.json` |
| [vial_morsus](https://github.com/martialsystems/vial_morsus) | `69f4f6d` | 0 of 3 k-NN. Lived on the bridge, extinct at t~400 when exudate hit 0. Science b106228. | `logs/knn_2500_s1.json` |
| [vial_culex](https://github.com/martialsystems/vial_culex) | `ddb73a8` | 0 of 3 k-NN. Blank founders extinct at t=5; cargo still 200. Science fa819c7. | `logs/knn_2500_s1.json` |
| [vial_handoff](https://github.com/martialsystems/vial_handoff) | `12d6952` | 0 of 3. Fail-predator: lived on hemolymph. Science e843b8c. | `logs/handoff_2500_s1.json` |

Figure 1 (`figures/stack.png`): parent F lock to bite arm to mosquito arm.

Index (pointers only): https://gist.github.com/martialsystems/12835f747d6360781f3cc7f91f243178

## 6. Replay

How to run: in each tree, `.venv/bin/python -m pytest`. Do not overwrite the listed lock files. Do not raise `bite_weight`. Do not raise gut_probe payoff. Do not restamp fly_vial F.

| Tree | Lock |
|------|------|
| fly_vial | `logs/assort_80.json`, `logs/random_80.json` |
| vial_sanguis | `logs/vampire_2500_s{1,2,3}.json`, `logs/random_2500_s{1,2,3}.json`, `logs/fruit_forever_400_s1.json` |
| vial_sanguis2 | `logs/knn_delayed_2500_s{1,2,3}.json`, `logs/knn_delayed_10000_s3.json` |
| vial_morsus | `logs/knn_2500_s{1,2,3}.json` |
| vial_culex | `logs/knn_2500_s{1,2,3}.json` |
| vial_handoff | `logs/handoff_2500_s{1,2,3}.json`; map `maps/morsus_to_culex.json`; t_snap=200 |
