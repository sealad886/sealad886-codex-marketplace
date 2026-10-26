# Oracles, differential checks, and justified properties

Use when a direct expected result is expensive, incomplete, or unavailable.
Choose evidence that challenges the relevant contract without treating another
implementation, historical output, or appealing mathematical relation as truth.
Keep comparison records in the existing [audit ledger](../templates/audit-ledger.md).

## Define the comparison first

1. Pin the target revision, supported input domain, accepted contract, and the
   specific output/state being compared. Separate deterministic fields from
   randomness, time, ordering, platform effects, or approximate computation.
2. Identify the oracle's provenance, revision, configuration, input identity,
   and acceptance basis. Record shared code/data/assumptions that weaken its
   independence. A previous release or golden file may preserve an old bug.
3. Define any normalization and tolerance before observing differences. Justify
   units, absolute/relative bounds, aggregation, and treatment of NaN, infinities,
   missing values, empty output, or boundary inputs when relevant. Do not strip
   meaningful order, multiplicity, identity, or error information to obtain a pass.
4. State the property or relation and why it holds for this contract and input
   domain. Fix transformation preconditions and excluded cases. An unspecified
   requirement remains a question, not a new invariant imposed by the audit.
5. Run a small permitted comparison, inspect mismatches, and retain raw versus
   normalized evidence as appropriate without exposing sensitive inputs. Bound
   input size, repetitions, runtime, and any external use.

Do not choose tolerances after seeing results or silently loosen a bound. If the
contract or justified bound changes, record the decision and rerun separately.
Metamorphic transformations must preserve the stated preconditions; an input
outside them cannot falsify the relation.

## Select the oracle or property

| Method | Justified use | Limits to record |
| --- | --- | --- |
| Independent reference | A specification, analytically solved fixture, trusted measurement, or independently implemented algorithm with an accepted correctness basis | Reference defects, incompatible versions/configuration, measurement uncertainty, and shared assumptions |
| Accepted historical check | Approved prior behavior remains required for this input/version domain | Historical acceptance is evidence of intent, not universal correctness; deliberate changes and known defects need separate treatment |
| Differential implementations | Two compatible implementations process identical supported inputs | Disagreement identifies a candidate; determine which output, if either, satisfies the contract |
| Round trip | Decode/encode, serialize/parse, or transform/inverse must preserve specified information | Two stages can share a compensating defect; normalization or lossy transforms may preserve only a defined equivalence class |
| Conservation | A contract preserves a quantity such as account balance, count, mass, or total contribution | Account for permitted loss, fees, rounding, filtering, duplication, or external inflow/outflow before summing |
| Order invariance | The operation explicitly treats inputs as an unordered set or commutative combination | Ordered events, floating-point accumulation, tie-breaking, or first/last-wins rules can make order meaningful |
| Monotonicity | Increasing a defined input cannot decrease a defined output over a justified domain | Saturation, thresholds, normalization, ranking, interactions, or constraints may invalidate the relation |
| Bounded error | An accepted approximation has a defined metric and error bound against a justified reference | Input distribution/domain, reference uncertainty, absolute versus relative error near zero, and worst-case versus aggregate claims |

Use only the relations supported by evidence; no audit needs all methods. An
unavailable oracle may leave a useful consistency check, but does not convert it
into accuracy proof. Combining several checks can strengthen a conclusion only
to the extent their failure modes are independent.

## Resolve a disagreement

First check identical inputs and relevant environment/configuration, supported
versions, transformation preconditions, normalization, and precision. Minimize
the case without erasing its cause. Inspect target and reference independently
against the accepted contract. A third implementation is another evidence source,
not a majority vote that settles correctness.

If the historical reference is known to mishandle this input, a different new
output is not by itself a regression. Verify the new output with an independent
basis or leave the target claim `needs evidence`; record the reference defect
separately only if it is within scope. If intent conflicts, report the required
decision before remediation. Do not change source, golden files, or acceptance
criteria in an audit-only task.

## Worked interpretations

- A lossy media codec reconstructs a fixture within a pre-agreed error bound on
  the chosen metric. That supports this round-trip property for those inputs. It
  does not establish perceptual fidelity, scientific accuracy, or the truth of
  the original signal; those need their own accepted reference and evaluation.
- Reordering import events changes the result under a documented last-write-wins
  policy. An order-invariance test was inapplicable. Test the actual version/order
  policy instead, without relabeling expected order dependence as a defect.
- A new parser and an accepted historical parser disagree on a truncated record.
  The old parser silently fabricated a value. Without a specified error contract
  or independent oracle for the new output, keep the target's correctness
  unresolved. Historical acceptance alone cannot establish that fabricated value
  as the required result.

## Report the supported conclusion

Record oracle provenance and independence, property/rule, input scope,
normalization/tolerance, actual result, and uncertainty under one evidence ID.
Separate synthetic fixture evidence from representative real-input evidence;
neither establishes untested production/provider behavior. Label a demonstrated
contract violation as a finding, an unexplained disagreement as `needs evidence`,
and a disproved hypothesis accurately. Remediation remains separately authorized.
