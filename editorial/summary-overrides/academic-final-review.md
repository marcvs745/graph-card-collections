---
type: review
title: "Academic quiz clue semantic repair 2026-11-08"
description: "Targeted subject-fragment, compound-answer and parenthetical-alias repairs against public inline content."
---

# Scope and method

[Repair overrides](academic-final-review.json) contain 77 cards with four meaning clues each (308 strings). They apply after the frozen academic packs. This review changes summaries only; it does not change titles, descriptions, relations, assets or other cards.

The scan covered all 170 academic packs, 3,128 cards and 12,512 locale clues. Heuristics looked for truncated subject fragments, named components of compound titles, and answer names concealed by parenthetical title qualifiers. The initial scan enumerated 330 candidates; this includes benign phrases such as “change,” measurement vocabulary and Chinese sentences legitimately beginning with 為. Candidates are leads, not 330 proven defects.

Priority semantic inspection covered the 79 math/physics/chemistry candidates against the public inline title and explanatory body. Sixty-three receive repairs here. Sixteen remain because their ordinary descriptive words or quantities are needed to define the subject, or the proposed fragment is a complete noun phrase. Fourteen additional cards repair concrete fragments or parenthetical/name leakage in biology, business, psychology, philosophy, literature and art. The 32 four-locale math-symbol clues were also inspected and retained; they describe operators without printing the answer glyph. Mathematical formulas in geometry clues remain when they describe a different concept, rather than disclose a symbol-title answer.

# Concrete findings

- Weighted mean: Chinese subject deletion left 數是. All four clues now independently describe the sum of value–weight products divided by total weight.
- Quartiles and IQR: the title covers both concepts, but the old clue named the second answer component and described only its formula. The replacement describes ordered-data cutoffs and their upper–lower difference without printing those names.
- Sine and cosine: the English clue lost its first subject while leaving the second name. The replacements identify the two coordinate functions without naming them.
- Paired scientific terms: replacements explain the two processes or quantities in order, rather than print their names in the clue. Conditions such as constant pressure, phase-change exclusions, reversible cells, isolated systems and specified temperature are retained where relevant.
- Several English clues lost a governing noun or verb (atomic nucleus, tissue/organ cooperation, working memory and training transfer). The repaired clauses stand on their own.
- Parenthetical or qualified titles bypassed full-title-only detection. The repairs remove the answer names for the three Chinese philosophical works, a tragic prince, a critical concept, a lyric poem, an autobiography and a Korean painter.

This review does not forbid every word shared with a compound title. In particular, “mass” in the rest-energy clue is an ordinary physical quantity needed to state the relation; it is not a distinct answer name. Treating every shared common word as forbidden would reduce accuracy. The scan is not an independent certification of all 12,512 meanings or all distractor combinations.

# Evidence

The primary evidence is the corresponding public collection’s inline translated body and title, read from the integration checkout. Each row below links the public collection source. Public main may acquire these staged changes only after integration. The authoring source pack supplies the before-clue; the override supplies the after-clue. No body was rewritten to justify a clue.

The current description integration scope is 137 art-person cards; music descriptions retain the public originals. This summary review does not alter that scope.

The painter’s identity additionally uses the previously recorded institutional evidence in [music/art review](../person-description-review.md); the public checkout still held the earlier generic artist-credit body during this check. It must receive the already authored art-person body update at integration.

| Card | Public source |
| --- | --- |
| `math-statistics-weighted` | [math-statistics](https://github.com/marcvs745/graph-card-collections/blob/main/collections/math-statistics/collection.json) |
| `math-statistics-quartiles` | [math-statistics](https://github.com/marcvs745/graph-card-collections/blob/main/collections/math-statistics/collection.json) |
| `math-statistics-frequency` | [math-statistics](https://github.com/marcvs745/graph-card-collections/blob/main/collections/math-statistics/collection.json) |
| `math-statistics-space` | [math-statistics](https://github.com/marcvs745/graph-card-collections/blob/main/collections/math-statistics/collection.json) |
| `math-functions-sine-cosine` | [math-functions](https://github.com/marcvs745/graph-card-collections/blob/main/collections/math-functions/collection.json) |
| `physics-measurement-quantity` | [physics-measurement](https://github.com/marcvs745/graph-card-collections/blob/main/collections/physics-measurement/collection.json) |
| `physics-measurement-si-base` | [physics-measurement](https://github.com/marcvs745/graph-card-collections/blob/main/collections/physics-measurement/collection.json) |
| `physics-measurement-scalar-vector` | [physics-measurement](https://github.com/marcvs745/graph-card-collections/blob/main/collections/physics-measurement/collection.json) |
| `physics-measurement-precision-accuracy` | [physics-measurement](https://github.com/marcvs745/graph-card-collections/blob/main/collections/physics-measurement/collection.json) |
| `physics-measurement-mean` | [physics-measurement](https://github.com/marcvs745/graph-card-collections/blob/main/collections/physics-measurement/collection.json) |
| `physics-measurement-significant-figures` | [physics-measurement](https://github.com/marcvs745/graph-card-collections/blob/main/collections/physics-measurement/collection.json) |
| `physics-electromagnetism-charge` | [physics-electromagnetism](https://github.com/marcvs745/graph-card-collections/blob/main/collections/physics-electromagnetism/collection.json) |
| `physics-electromagnetism-potential` | [physics-electromagnetism](https://github.com/marcvs745/graph-card-collections/blob/main/collections/physics-electromagnetism/collection.json) |
| `chemistry-electrochemistry-redox` | [chemistry-electrochemistry](https://github.com/marcvs745/graph-card-collections/blob/main/collections/chemistry-electrochemistry/collection.json) |
| `chemistry-electrochemistry-agents` | [chemistry-electrochemistry](https://github.com/marcvs745/graph-card-collections/blob/main/collections/chemistry-electrochemistry/collection.json) |
| `chemistry-electrochemistry-electrodes` | [chemistry-electrochemistry](https://github.com/marcvs745/graph-card-collections/blob/main/collections/chemistry-electrochemistry/collection.json) |
| `chemistry-electrochemistry-free-energy` | [chemistry-electrochemistry](https://github.com/marcvs745/graph-card-collections/blob/main/collections/chemistry-electrochemistry/collection.json) |
| `chemistry-electrochemistry-faraday` | [chemistry-electrochemistry](https://github.com/marcvs745/graph-card-collections/blob/main/collections/chemistry-electrochemistry/collection.json) |
| `chemistry-electrochemistry-corrosion` | [chemistry-electrochemistry](https://github.com/marcvs745/graph-card-collections/blob/main/collections/chemistry-electrochemistry/collection.json) |
| `physics-optics-tir` | [physics-optics](https://github.com/marcvs745/graph-card-collections/blob/main/collections/physics-optics/collection.json) |
| `physics-optics-dispersion` | [physics-optics](https://github.com/marcvs745/graph-card-collections/blob/main/collections/physics-optics/collection.json) |
| `physics-optics-interference` | [physics-optics](https://github.com/marcvs745/graph-card-collections/blob/main/collections/physics-optics/collection.json) |
| `physics-modern-time-dilation` | [physics-modern](https://github.com/marcvs745/graph-card-collections/blob/main/collections/physics-modern/collection.json) |
| `physics-modern-length-contraction` | [physics-modern](https://github.com/marcvs745/graph-card-collections/blob/main/collections/physics-modern/collection.json) |
| `physics-modern-rest-energy` | [physics-modern](https://github.com/marcvs745/graph-card-collections/blob/main/collections/physics-modern/collection.json) |
| `physics-modern-nucleus` | [physics-modern](https://github.com/marcvs745/graph-card-collections/blob/main/collections/physics-modern/collection.json) |
| `physics-modern-half-life` | [physics-modern](https://github.com/marcvs745/graph-card-collections/blob/main/collections/physics-modern/collection.json) |
| `physics-modern-fission-fusion` | [physics-modern](https://github.com/marcvs745/graph-card-collections/blob/main/collections/physics-modern/collection.json) |
| `physics-waves-period-frequency` | [physics-waves](https://github.com/marcvs745/graph-card-collections/blob/main/collections/physics-waves/collection.json) |
| `physics-waves-wave-speed` | [physics-waves](https://github.com/marcvs745/graph-card-collections/blob/main/collections/physics-waves/collection.json) |
| `physics-waves-standing-wave` | [physics-waves](https://github.com/marcvs745/graph-card-collections/blob/main/collections/physics-waves/collection.json) |
| `physics-energy-inelastic` | [physics-energy](https://github.com/marcvs745/graph-card-collections/blob/main/collections/physics-energy/collection.json) |
| `chemistry-organic-chirality` | [chemistry-organic](https://github.com/marcvs745/graph-card-collections/blob/main/collections/chemistry-organic/collection.json) |
| `chemistry-organic-ester-hydrolysis` | [chemistry-organic](https://github.com/marcvs745/graph-card-collections/blob/main/collections/chemistry-organic/collection.json) |
| `chemistry-organic-polymers` | [chemistry-organic](https://github.com/marcvs745/graph-card-collections/blob/main/collections/chemistry-organic/collection.json) |
| `chemistry-phases-vapor-pressure` | [chemistry-phases](https://github.com/marcvs745/graph-card-collections/blob/main/collections/chemistry-phases/collection.json) |
| `chemistry-phases-solubility` | [chemistry-phases](https://github.com/marcvs745/graph-card-collections/blob/main/collections/chemistry-phases/collection.json) |
| `chemistry-phases-colligative` | [chemistry-phases](https://github.com/marcvs745/graph-card-collections/blob/main/collections/chemistry-phases/collection.json) |
| `chemistry-phases-phases` | [chemistry-phases](https://github.com/marcvs745/graph-card-collections/blob/main/collections/chemistry-phases/collection.json) |
| `chemistry-phases-dipoles` | [chemistry-phases](https://github.com/marcvs745/graph-card-collections/blob/main/collections/chemistry-phases/collection.json) |
| `chemistry-thermochemistry-system` | [chemistry-thermochemistry](https://github.com/marcvs745/graph-card-collections/blob/main/collections/chemistry-thermochemistry/collection.json) |
| `chemistry-thermochemistry-heat-work` | [chemistry-thermochemistry](https://github.com/marcvs745/graph-card-collections/blob/main/collections/chemistry-thermochemistry/collection.json) |
| `chemistry-thermochemistry-exo-endo` | [chemistry-thermochemistry](https://github.com/marcvs745/graph-card-collections/blob/main/collections/chemistry-thermochemistry/collection.json) |
| `chemistry-thermochemistry-reaction-enthalpy` | [chemistry-thermochemistry](https://github.com/marcvs745/graph-card-collections/blob/main/collections/chemistry-thermochemistry/collection.json) |
| `chemistry-thermochemistry-entropy` | [chemistry-thermochemistry](https://github.com/marcvs745/graph-card-collections/blob/main/collections/chemistry-thermochemistry/collection.json) |
| `chemistry-thermochemistry-heat-capacity` | [chemistry-thermochemistry](https://github.com/marcvs745/graph-card-collections/blob/main/collections/chemistry-thermochemistry/collection.json) |
| `physics-thermodynamics-temperature` | [physics-thermodynamics](https://github.com/marcvs745/graph-card-collections/blob/main/collections/physics-thermodynamics/collection.json) |
| `physics-thermodynamics-heat` | [physics-thermodynamics](https://github.com/marcvs745/graph-card-collections/blob/main/collections/physics-thermodynamics/collection.json) |
| `physics-thermodynamics-specific-heat` | [physics-thermodynamics](https://github.com/marcvs745/graph-card-collections/blob/main/collections/physics-thermodynamics/collection.json) |
| `physics-thermodynamics-latent-heat` | [physics-thermodynamics](https://github.com/marcvs745/graph-card-collections/blob/main/collections/physics-thermodynamics/collection.json) |
| `physics-thermodynamics-convection` | [physics-thermodynamics](https://github.com/marcvs745/graph-card-collections/blob/main/collections/physics-thermodynamics/collection.json) |
| `chemistry-bonding-valence` | [chemistry-bonding](https://github.com/marcvs745/graph-card-collections/blob/main/collections/chemistry-bonding/collection.json) |
| `chemistry-bonding-vsepr` | [chemistry-bonding](https://github.com/marcvs745/graph-card-collections/blob/main/collections/chemistry-bonding/collection.json) |
| `chemistry-bonding-lone-pair-shape` | [chemistry-bonding](https://github.com/marcvs745/graph-card-collections/blob/main/collections/chemistry-bonding/collection.json) |
| `chemistry-matter-homogeneity` | [chemistry-matter](https://github.com/marcvs745/graph-card-collections/blob/main/collections/chemistry-matter/collection.json) |
| `chemistry-matter-coefficients` | [chemistry-matter](https://github.com/marcvs745/graph-card-collections/blob/main/collections/chemistry-matter/collection.json) |
| `chemistry-atomic-shells` | [chemistry-atomic](https://github.com/marcvs745/graph-card-collections/blob/main/collections/chemistry-atomic/collection.json) |
| `chemistry-atomic-electron-affinity` | [chemistry-atomic](https://github.com/marcvs745/graph-card-collections/blob/main/collections/chemistry-atomic/collection.json) |
| `biology-homeostasis-organization` | [biology-homeostasis](https://github.com/marcvs745/graph-card-collections/blob/main/collections/biology-homeostasis/collection.json) |
| `biology-cells-nucleus` | [biology-cells](https://github.com/marcvs745/graph-card-collections/blob/main/collections/biology-cells/collection.json) |
| `business-foundations-leading` | [business-foundations](https://github.com/marcvs745/graph-card-collections/blob/main/collections/business-foundations/collection.json) |
| `psychology-attention-dreams` | [psychology-attention](https://github.com/marcvs745/graph-card-collections/blob/main/collections/psychology-attention/collection.json) |
| `psychology-memory-working-memory` | [psychology-memory](https://github.com/marcvs745/graph-card-collections/blob/main/collections/psychology-memory/collection.json) |
| `business-people-development` | [business-people](https://github.com/marcvs745/graph-card-collections/blob/main/collections/business-people/collection.json) |
| `philosophy-chinese-mengzi-text` | [philosophy-chinese](https://github.com/marcvs745/graph-card-collections/blob/main/collections/philosophy-chinese/collection.json) |
| `philosophy-chinese-xunzi-text` | [philosophy-chinese](https://github.com/marcvs745/graph-card-collections/blob/main/collections/philosophy-chinese/collection.json) |
| `philosophy-chinese-mozi-text` | [philosophy-chinese](https://github.com/marcvs745/graph-card-collections/blob/main/collections/philosophy-chinese/collection.json) |
| `art-korean-artist-5d8a78eb474e` | [art-korean](https://github.com/marcvs745/graph-card-collections/blob/main/collections/art-korean/collection.json) |
| `literature-drama-hamlet-prince` | [literature-drama](https://github.com/marcvs745/graph-card-collections/blob/main/collections/literature-drama/collection.json) |
| `literature-criticism-mimesis` | [literature-criticism](https://github.com/marcvs745/graph-card-collections/blob/main/collections/literature-criticism/collection.json) |
| `literature-poetry-daffodils` | [literature-poetry](https://github.com/marcvs745/graph-card-collections/blob/main/collections/literature-poetry/collection.json) |
| `literature-nonfiction-douglass-narrative` | [literature-nonfiction](https://github.com/marcvs745/graph-card-collections/blob/main/collections/literature-nonfiction/collection.json) |
| `physics-energy-conservative` | [physics-energy](https://github.com/marcvs745/graph-card-collections/blob/main/collections/physics-energy/collection.json) |
| `physics-mechanics-inertia` | [physics-mechanics](https://github.com/marcvs745/graph-card-collections/blob/main/collections/physics-mechanics/collection.json) |
| `math-geometry-parallel` | [math-geometry](https://github.com/marcvs745/graph-card-collections/blob/main/collections/math-geometry/collection.json) |
| `chemistry-atomic-ionic-radius` | [chemistry-atomic](https://github.com/marcvs745/graph-card-collections/blob/main/collections/chemistry-atomic/collection.json) |
| `physics-rotation-gravity-field` | [physics-rotation](https://github.com/marcvs745/graph-card-collections/blob/main/collections/physics-rotation/collection.json) |
