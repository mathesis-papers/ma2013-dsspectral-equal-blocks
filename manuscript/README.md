# Equal-block spectral determination

The note credits Colbrook's prior refutation of the Mourad–Abbas conjecture and proves an exact threshold for equal blocks. For integers `k,r >= 2`, the direct sum of `r` copies of `t I_k + (1-t) C_k`, `0 <= t <= 1`, is determined up to permutation among all similar doubly stochastic matrices exactly when `t < 1/k^2` or `t = 1`. For `k >= 4` and `0 < t < 1/k^2`, the matrices have positive trace and avoid every segment proposed in the conjecture.

## Files and rebuilding

- `note.tex`: complete mathematical argument, bibliography included.
- `metadata.json`: creators, license, problem identifier and mathematical coverage.
- `verify.py`: dependency-free exact rational checks, Python 3.10 or later.
- `verification.json`: expected deterministic checker output.

Build with Tectonic 0.17.0:

```sh
tectonic --untrusted note.tex
```

Alternatively run `pdflatex -interaction=nonstopmode -halt-on-error note.tex` twice. No separate BibTeX file is needed. The source uses `geometry`, `amsmath`, `amssymb`, `amsthm`, `booktabs`, `array`, `fontenc`, `lmodern` and `hyperref`.

Check the finite identities and compare with the supplied output:

```sh
python3 verify.py > verification.actual.json
python3 -c 'import json; assert json.load(open("verification.actual.json")) == json.load(open("verification.json")); print("MATCH")'
```

## Mathematical coverage

The entire threshold theorem, including nonsymmetric competitors under ordinary similarity, has a written proof. The finite checks do not replace that proof.

Theorem 2 restates the classical structure of diagonalizable real doubly stochastic matrices with two distinct eigenvalues `1` and `lambda < 1`: their permutation classes correspond exactly to integer partitions into uniform blocks whose diagonal entries are nonnegative. Farahat (1966), Section 2, assertion (2.2) and its following paragraph, gives the idempotent partition classes; da Cruz, Dolinar, Fernandes and Kuzma (2017), Proposition 1.2, Theorem 2.1 and Remark 2.2, supply the affine-idempotent representation. A complete elementary proof is included. In particular every such matrix is symmetric. Thus spectral determination in the symmetric and full doubly stochastic sets agrees throughout this class. For `0 <= lambda < 1`, uniqueness holds exactly for eigenvalue-one multiplicity `r=1` or `r=n-1`.

The zero-trace corollary shows that the symmetric matrices with exactly two distinct eigenvalues are precisely direct sums of equally sized `C_k` blocks, `k >= 2`; they are all spectrally determined. The source's general zero-trace problem and regular-graph implication remain outside this classification. The equal-block zero-trace determination and the single-block identity-to-`C_n` segment already appear in Mourad and Abbas (2013).

The pinned Lean file is:

https://github.com/the-omega-institute/trureturing/blob/d9880e9f2c329bb3db982f33791419d5d90126b9/D5/S0/Certificates/MouradAbbasC51Refutation.lean

The declaration `D5.S0.Certificates.MouradAbbasC51Refutation.result : ¬ claim` proves the universal conjecture false using the order-eight witness. In the same file, `family_isDS` covers spectral determination for `k >= 4` and `0 < t < 1/k^2` with symmetric competitors; `family_exclusion` and `family_trace_slice` cover segment exclusion and positive trace when additionally `r >= 2`. The partition classification, zero-trace and nonnegative-eigenvalue corollaries, complete threshold and nonsymmetric-similarity extension are established by written proofs, rather than attributed to these declarations.

## References and license

The posing source is Mourad and Abbas, arXiv:1310.1273v1, Conjecture 5.1, p. 10. Colbrook's September 11, 2026 counterexample is credited in the title, abstract and bibliography. The structural antecedents are Farahat, DOI `10.1017/S2040618500035401`, and da Cruz et al., DOI `10.1016/j.laa.2017.06.029`. Flor's nonnegative-idempotent classification supplies broader context; the special case needed here is proved in full.

Creators, in order: Haobo Ma (ChronoAI Pte Ltd, Singapore); Wenlin Zhang (National University of Singapore; ChronoAI Pte Ltd, Singapore). The note and accompanying original supporting files are licensed under Creative Commons Attribution 4.0 International, CC BY 4.0 (`cc-by-4.0`): https://creativecommons.org/licenses/by/4.0/.
