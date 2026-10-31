# SciPy numerical methods: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Check optimizer success/status and residuals rather than accepting returned parameters; derivative-free methods do not guarantee reliable optimization of every nonsmooth problem.

- Solve linear systems rather than forming an inverse; select dense/structured/sparse solvers and diagnose conditioning.

- For new 1-D interpolation, choose current alternatives such as CubicSpline, PchipInterpolator, or make_interp_spline as appropriate; interp1d and UnivariateSpline are legacy APIs.

- Specify extrapolation and missing/duplicate-point behavior; a smooth interpolant may overshoot physical bounds.

- Use solve_ivp methods and Jacobians matching stiffness; validate event conditions and conservation rather than trusting termination alone.

- For digital filtering consider second-order sections for numerical stability; forward-backward filtering is noncausal and needs boundary/length handling.

- Statistical tests require justified independence/distribution assumptions and explicit missing-data/multiple-testing policy.

- Set numerical tolerances from scale and units; float64 is not a proof of adequate precision and float32 is not always acceptable.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [interp1d is legacy and modern interpolation alternatives are recommended.](https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp1d.html)
- [Signal filtering includes second-order-section and forward-backward APIs with distinct behavior.](https://docs.scipy.org/doc/scipy/reference/signal.html)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
