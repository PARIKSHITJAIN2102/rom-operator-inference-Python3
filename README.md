# Operator Inference

This is a Python implementation of the operator learning approach for projection-based reduced order models of systems of ordinary differential equations.
The procedure is **data-driven** and **non-intrusive**, making it a viable candidate for model reduction of black-box or complex systems.
The methodology originates from following paper.
See the [References](#references) section for more papers that use or build on operator inference.

- \[1\] Peherstorfer, B. and Willcox, K.
[Data-driven operator inference for non-intrusive projection-based model reduction.](https://www.sciencedirect.com/science/article/pii/S0045782516301104)
Computer Methods in Applied Mechanics and Engineering, 306:196-215, 2016.
([Download](https://cims.nyu.edu/~pehersto/preprints/Non-intrusive-model-reduction-Peherstorfer-Willcox.pdf))<details><summary>BibTeX</summary><pre>
@article{Peherstorfer16DataDriven,
    title     = {Data-driven operator inference for nonintrusive projection-based model reduction},
    author    = {Peherstorfer, B. and Willcox, K.},
    journal   = {Computer Methods in Applied Mechanics and Engineering},
    volume    = {306},
    pages     = {196--215},
    year      = {2016},
    publisher = {Elsevier}
}</pre></details>

**Contributors**: [Renee Swischuk](https://github.com/swischuk), [Shane McQuarrie](https://github.com/shanemcq18), [Elizabeth Qian](https://github.com/elizqian), [Boris Kramer](https://github.com/bokramer).

See [this repository](https://github.com/elizqian/operator-inference) for a MATLAB implementation.

**Contents**
- [**Problem Statement**](#problem-statement)
- [**Quick Start**](#quick-start)
- [**Examples**](#examples)
- [**Documentation**](#documentation)
    - [**ReducedModel Class**](#reducedmodel-class)
    - [**Preprocessing**](#preprocessing-tools)
    - [**Postprocessing**](#postprocessing-tools)
    - [**Utility Functions**](#utility-functions)
- [**References**](#references)

## Problem Statement

Consider the (possibly nonlinear) system of _n_ ordinary differential equations with state variable **x**, input (control) variable **u**, and independent variable _t_:

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?\dot{\mathbf{x}}(t)=\mathbf{f}(t,\mathbf{x}(t),\mathbf{u}(t)),"/>
</p>

where

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?\mathbf{x}:\mathbb{R}\to\mathbb{R}^n,\qquad\mathbf{u}:\mathbb{R}\to\mathbb{R}^m,\qquad\mathbf{f}:\mathbb{R}\times\mathbb{R}^n\times\mathbb{R}^m\to\mathbb{R}^n."/>
</p>

This system is called the _full-order model_ (FOM).
If _n_ is large, as it often is in high-consequence engineering applications, it is computationally expensive to numerically solve the FOM.
This package provides tools for constructing a _reduced-order model_ (ROM) that is linear or quadratic in the state **x**, possibly with a constant term **c**, and with optional control inputs **u**.
The procedure is data-driven, non-intrusive, and relatively inexpensive.
In the most general case, the code can construct and solve a system of the form

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?\dot{\hat{\mathbf{x}}}(t)=\hat{A}\hat{\mathbf{x}}(t)+\hat{H}(\hat{\mathbf{x}}\otimes\hat{\mathbf{x}})(t)+\hat{B}\mathbf{u}(t)+\hat{\mathbf{c}},"/>
</p>

<!-- <p align="center">
  <img src="https://latex.codecogs.com/svg.latex?\dot{\hat{\mathbf{x}}}(t)=\hat{A}\hat{\mathbf{x}}(t)+\hat{H}(\hat{\mathbf{x}}\otimes\hat{\mathbf{x}})(t)+\hat{B}\mathbf{u}(t)+\sum_{i=1}^m\hat{N}_{i}\hat{\mathbf{x}}(t)u_{i}(t)+\hat{\mathbf{c}},"/>
</p> -->

where now

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?\hat{\mathbf{x}}:\mathbb{R}\to\mathbb{R}^r,\qquad\mathbf{u}:\mathbb{R}\to\mathbb{R}^m,\qquad\hat{\mathbf{c}}\in\mathbb{R}^r,\qquad%20r\ll%20n,"/>
</p>
<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?\hat{A}\in\mathbb{R}^{r\times%20r},\qquad\hat{H}\in\mathbb{R}^{r\times%20r^2},\qquad\hat{B}\in\mathbb{R}^{r\times%20m}."/>
</p>

<!-- <p align="center">
  <img src="https://latex.codecogs.com/svg.latex?\hat{A}\in\mathbb{R}^{r\times%20r},\qquad\hat{H}\in\mathbb{R}^{r\times%20r^2},\qquad\hat{B}\in\mathbb{R}^{r\times%20m},\qquad\hat{N}_{i}\in\mathbb{R}^{r\times%20r}."/>
</p> -->

This reduced low-dimensional system approximates the original high-dimensional system, but it is much easier (faster) to solve because of its low dimension _r_ << _n_.

See [DETAILS.md](DETAILS.md) for more mathematical details and an index of notation.


## Quick Start

#### Installation

```bash
$ pip3 install -i https://test.pypi.org/simple/rom-operator-inference-shanemcq18
```

_**This installation command is very temporary!**_

#### Usage

<!-- TODO: what are these variables?? -->

```python
import rom_operator_inference as roi

# Define a model of the form x' = Ax + c (no input).
>>> lc_model = roi.ReducedModel('Lc', inp=False)

# Fit the model to snapshot data X, the snapshot derivative Xdot,
# and the linear basis Vr by solving for the operators A_ and c_.
>>> lc_model.fit(X, Xdot, Vr)

# Simulate the learned model over the time domain [0,1] with 100 timesteps.
>>> t = np.linspace(0, 1, 100)
>>> X_ROM = lc_model.predict(X[:,0], t)
```


## Examples

_**WARNING: under construction!!**_

The [`examples/`](examples/) folder contains scripts and notebooks that set up and run several examples:
- `examples/TODO.ipynb`: The heat equation example from [\[1\]](https://www.sciencedirect.com/science/article/pii/S0045782516301104).
- `examples/TODO.ipynb`: The Burgers' equation from [\[1\]](https://www.sciencedirect.com/science/article/pii/S0045782516301104).
- `examples/TODO.ipynb`: The Euler equation example from [\[2\]](https://arc.aiaa.org/doi/10.2514/6.2019-3707).
This example uses MATLAB's Curve Fitting Toolbox to generate the random initial conditions.
- [`examples/heat_1D.ipynb`](examples/heat_1D.ipynb): A purely data-driven example using data generated from a one-dimensional heat equation \[4\].

<!-- TODO: actual links to the folders or files -->


## Documentation

<!-- **TODO**: The complete documentation at _\<insert link to sphinx-generated readthedocs page\>_. -->
<!-- Here we include a short catalog of functions and their inputs. -->

#### ReducedModel Class

The API for this class adopts some principles from the [scikit-learn](https://scikit-learn.org/stable/index.html) [API](https://scikit-learn.org/stable/developers/contributing.html#apis-of-scikit-learn-objects): the class has `fit()` and `predict()` methods, hyperparameters are set in the constructor, estimated attributes end with underscore, and so on.

##### Constructor

```python
import rom_operator_inference as roi

model = roi.ReducedModel(modelform, has_inputs)
```

Here `modelform` is one of the following strings denoting the structure of
the desired ROM.

| `modelform` | Model Description | Model Equation |
| :------- | :---------------- | :------------- |
|  `"L"`   |  **L**inear | <img src="https://latex.codecogs.com/svg.latex?\dot{\hat{\mathbf{x}}}(t)=\hat{A}{\hat{\mathbf{x}}(t)"/>
|  `"Lc"`  |  **L**inear with **c**onstant | <img src="https://latex.codecogs.com/svg.latex?\dot{\hat{\mathbf{x}}}(t)=\hat{A}{\hat{\mathbf{x}}(t)+\hat{\mathbf{c}}"/>
|  `"Q"`   |  **Q**uadratic | <img src="https://latex.codecogs.com/svg.latex?\dot{\hat{\mathbf{x}}}(t)=\hat{H}(\hat{\mathbf{x}}\otimes\hat{\mathbf{x}})(t)"/>
|  `"Qc"`  |  **Q**uadratic with **c**onstant | <img src="https://latex.codecogs.com/svg.latex?\dot{\hat{\mathbf{x}}}(t)=\hat{H}(\hat{\mathbf{x}}\otimes\hat{\mathbf{x}})(t)+\hat{\mathbf{c}}"/>
|  `"LQ"`  |  **L**inear-**Q**uadratic | <img src="https://latex.codecogs.com/svg.latex?\dot{\hat{\mathbf{x}}}(t)=\hat{A}\hat{\mathbf{x}}(t)+\hat{H}(\hat{\mathbf{x}}\otimes\hat{\mathbf{x}})(t)"/>
|  `"LQc"` |  **L**inear-**Q**uadratic with **c**onstant | <img src="https://latex.codecogs.com/svg.latex?\dot{\hat{\mathbf{x}}}(t)=\hat{A}\hat{\mathbf{x}}(t)+\hat{H}(\hat{\mathbf{x}}\otimes\hat{\mathbf{x}})(t)+\hat{\mathbf{c}}"/>

The `has_inputs` argument is a boolean (`True` or `False`) denoting whether or not there is an additive input term of the form <img src="https://latex.codecogs.com/svg.latex?B\mathbf{u}(t)"/>.

##### Methods

- `ReducedModel.fit(X, Xdot, Vr, U=None, G=0)`: Compute the operators of the reduced-order model that best fit the data by solving a regularized least
    squares problem. See [DETAILS.md](DETAILS.md) for more explanation.
Parameters:
    - `X`: Snapshot matrix of solutions to the full-order model. Each column is one snapshot.
    - `Xdot`: Snapshot velocity of solutions to the full-order model. Each column is the velocity `dx / dt` for the corresponding column of `X`. See the [`pre`](#preprocessing-tools) submodule for some simple derivative approximation tools.
    - `Vr`: The basis for the linear reduced space on which the full-order model will be projected (for example, a POD basis matrix). Each column is a basis vector. The column space of `Vr` should be a good approximation of the column space of `X`. See [`pre.pod_basis()`](#preprocessing-tools) for an example of computing the POD basis.
    - `U`: Input matrix. Each column is the input for the corresponding column of `X`. Only required when `has_inputs=True`.
    - `G`: Tikhonov regularization matrix for the least squares problem.

- `ReducedModel.predict(x0, t, u=None, **options)`: Simulate the learned reduced-order model with `scipy.integrate.solve_ivp()`. Parameters:
    - `x0`: The initial condition, given in the original (high-dimensional) space.
    - `t`: The time domain over which to integrate the reduced-order model.
    - `u`: The input as a function of time. Alternatively, a matrix aligned with the time domain `t` where each column is the input at the corresonding time.
    - Other keyword arguments for [`scipy.integrate.solve_ivp()`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html).

##### Attributes

- Hyperparameters: `modelform` and `has_inputs`, set in the [constructor](#constructor).

- Dimensions:
    - `n`: The dimension of the original model
    - `r`: The dimension of the learned reduced-order model
    - `m`: The dimension of the input u(t), or `None` if `has_inputs` is `False`.

- Reduced operators `A_`, `H_`, `F_`, `c_`, and `B_`: the `numpy.ndarray` objects corresponding to the learned parts of the reduced-order model. Set to `None` if the operator is not included in the prescribed `modelform` (e.g., if `modelform="LQ"`, then `c_` is `None`). Accessible as attributes (`model.A_`) or by indexing (`model['A_']`).

#### Preprocessing Tools

The `pre` submodule is a collection of common routines for preparing data to be used by the `ReducedModel` class.
None of these routines are novel, but they may be instructive for new Python users.

- `pre.mean_shift(X)`: Compute the mean of the columns of `X` and shift `X` by that mean so that the result has mean column of zero.

- `pre.pod_basis(X, r, mode="arpack", **options)`: Compute the POD basis of rank `r` for a snapshot matrix `X`.

- `pre.significant_svdvals(X, eps, plot=False)`: Count the number of singular values of `X` that are greater than `eps`.

- `pre.energy_capture(X, thresh, plot=False)`: Compute the number of singular values of `X` needed to surpass the energy threshold `thresh`; the energy of the first _j_ singular values is defined by <p align="center"><img src="https://latex.codecogs.com/svg.latex?\kappa_j=\frac{\sum_{i=1}^j\sigma_i^2}{\sum_{i=1}^n\sigma_i^2}."/></p>

- `pre.projection_error(X, Vr)`: Compute the relative projection error on _X_ induced by the basis matrix _V<sub>r</sub>_, <p align="center"><img src="https://latex.codecogs.com/svg.latex?\mathtt{proj\_err}=\frac{||X-V_rV_r^\mathsf{T}X||_F}{||X||_F}."/></p>

- `pre.minimal_projection_error(X, eps, rmax=_np.inf, plot=False, **options)`: Compute the number of POD basis vectors required to obtain a projection
error less than `eps`, capped at `rmax`.

- `pre.xdot_uniform(X, dt, order=2)`: Approximate the first derivative of a snapshot matrix `X` in which the snapshots are evenly spaced in time.

- `pre.xdot_nonuniform(X, t)`: Approximate the first derivative of a snapshot matrix `X` in which the snapshots are **not** evenly spaced in time.

- `pre.xdot(X, *args, **kwargs)`: Call `pre.xdot_uniform()` or `pre.xdot_nonuniform()`, depending on the arguments.


#### Postprocessing Tools

The `post` submodule is a collection of common routines for computing the absolute and relative errors produced by a ROM approximation.
Given a norm, "true" data _X_, and an approximation _Y_ to _X_, these errors are defined by <p align="center"><img src="https://latex.codecogs.com/svg.latex?\texttt{abs\_error}=||X-Y||,\qquad\texttt{rel\_error}=\frac{\texttt{abs\_error}}{||X||}=\frac{||X-Y||}{||X||}."/></p>

- `post.frobenius_error(X, Y)`: Compute the absolute and relative Frobenius-norm errors between snapshot sets `X` and `Y`, assuming `Y` is an approximation to `X`.
The [Frobenius matrix norm](https://en.wikipedia.org/wiki/Matrix_norm#Frobenius_norm) is defined by <p align="center"><img src="https://latex.codecogs.com/svg.latex?||X||_{F}=\sqrt{\text{tr}(X^\mathsf{T}X)}=\left(\sum_{i=1}^n\sum_{j=1}^k|x_{ij}|^2\right)^{1/2}."></p>

- `post.lp_error(X, Y, p=2, normalize=False)`: Compute the absolute and relative _l_<sup>_p_</sup>-norm errors between snapshot sets `X` and `Y`, assuming `Y` is an approximation to `X`.
The [_l_<sup>_p_</sup> norm](https://en.wikipedia.org/wiki/Lp_space#The_p-norm_in_finite_dimensions) is defined by <p align="center"><img src="https://latex.codecogs.com/svg.latex?||\mathbf{x}||_{\ell^p}=\begin{cases}\left(\displaystyle\sum_{i=1}^n|x_{i}|^p\right)^{1/p}&p<\infty,\\\\\displaystyle\sup_{i=1,\ldots,n}|x_i|&p=\infty.\end{cases}"/></p>
With _p=2_ this is the usual Euclidean norm.
The errors are calculated for each pair of columns of `X` and `Y`.
If `normalize=True`, then the _normalized absolute error_ is computed instead of the relative error: <p align="center"><img src="https://latex.codecogs.com/svg.latex?\texttt{norm\_abs\_err}_j=\frac{||\mathbf{x}_j-\mathbf{y}_j||_{\ell^p}}{\displaystyle\max_{i=1,\ldots,k}||\mathbf{x}_i||_{\ell^p}},\quad%20j=1,\ldots,k."></p>

- `post.Lp_error(X, Y, t=None, p=2)`: Approximate the absolute and relative _L_<sup>_p_</sup>-norm errors between snapshot sets `X` and `Y` corresponding to times `t`, assuming `Y` is an approximation to `X`.
The [_L_<sup>_p_</sup> norm](https://en.wikipedia.org/wiki/Lp_space#Lp_spaces) for vector-valued functions is defined by <p align="center"><img src="https://latex.codecogs.com/svg.latex?||\mathbf{x}(\cdot)||_{L^p([0,T])}=\begin{cases}\left(\displaystyle\int_{0}^{T}||\mathbf{x}(t)||_{\ell^p}^p\:dt\right)^{1/p}&p<\infty,\\\\\displaystyle\sup_{t\in[0,T]}||\mathbf{x}(t)||_{\ell^\infty}&%20p=\infty.\end{cases}"/></p>
For finite _p_, the integrals are approximated by the trapezoidal rule: <p align="center"><img src="https://latex.codecogs.com/svg.latex?||\mathbf{x}(\cdot)||_{L^2([0,T])}=\sqrt{\int_0^T||\mathbf{x}(t)||_{\ell^2}^2\:dt}\approx\Delta%20t\left(\frac{1}{2}\|\mathbf{x}(t_0)\|_{\ell^2}^2+\sum_{j=1}^{k-1}\|\mathbf{x}(t_j)\|_{\ell^2}^2+\frac{1}{2}\|\mathbf{x}(t_k)\|_{\ell^2}^2\right)."/></p>
The `t` argument can be omitted if _p_ is infinity (`p = np.inf`).

#### Utility Functions

These functions are helper routines that are used internally for `ReducedModel.fit()` or `ReducedModel.predict()`.
See [DETAILS.md](DETAILS.md) for more mathematical explanation.

- `utils.lstsq_reg(A, b, G=0)`: Solve the Tikhonov-regularized ordinary least squares problem
<p align="center"><img src="https://latex.codecogs.com/svg.latex?\underset{\mathbf{x}\in\mathbb{R}^n}{\text{min}}||A\mathbf{x}-\mathbf{b}||_{\ell^2}^2+||G\mathbf{x}||_{\ell^2}^2,"/></p>

  where _G_ is the regularization matrix. If `b` is a matrix, solve the above problem for each column of `b`. If `G` is a scalar, use the identity matrix times that scalar for the regularization matrix _G_.

-  `utils.kron_compact(x)`: Compute the column-wise compact Kronecker product of `x`.

- `utils.kron_columnwise(x, y)`: Compute the full Khatri-Rhao (column-wise) Kronecker product of `x` and `y`.

-  `utils.F2H(F)`: Convert the compact matricized quadratic operator `F` to the full, symmetric, matricized quadratic operator `H`.


## References

- \[1\] Peherstorfer, B. and Willcox, K.
[Data-driven operator inference for non-intrusive projection-based model reduction.](https://www.sciencedirect.com/science/article/pii/S0045782516301104)
Computer Methods in Applied Mechanics and Engineering, 306:196-215, 2016.
([Download](https://cims.nyu.edu/~pehersto/preprints/Non-intrusive-model-reduction-Peherstorfer-Willcox.pdf))<details><summary>BibTeX</summary><pre>
@article{Peherstorfer16DataDriven,
    title     = {Data-driven operator inference for nonintrusive projection-based model reduction},
    author    = {Peherstorfer, B. and Willcox, K.},
    journal   = {Computer Methods in Applied Mechanics and Engineering},
    volume    = {306},
    pages     = {196--215},
    year      = {2016},
    publisher = {Elsevier}
}</pre></details>

- \[2\] Qian, E., Kramer, B., Marques, A., and Willcox, K.
[Transform & Learn: A data-driven approach to nonlinear model reduction](https://arc.aiaa.org/doi/10.2514/6.2019-3707).
In the AIAA Aviation 2019 Forum, June 17-21, Dallas, TX. ([Download](https://www.dropbox.com/s/5znea6z1vntby3d/QKMW_aviation19.pdf?dl=0))<details><summary>BibTeX</summary><pre>
@inbook{QKMW2019aviation,
    author    = {Qian, E. and Kramer, B. and Marques, A. N. and Willcox, K. E.},
    title     = {Transform \&amp; Learn: A data-driven approach to nonlinear model reduction},
    booktitle = {AIAA Aviation 2019 Forum},
    doi       = {10.2514/6.2019-3707},
    URL       = {https://arc.aiaa.org/doi/abs/10.2514/6.2019-3707},
    eprint    = {https://arc.aiaa.org/doi/pdf/10.2514/6.2019-3707}
}</pre></details>

- \[3\] Swischuk, R. and Mainini, L. and Peherstorfer, B. and Willcox, K.
[Projection-based model reduction: Formulations for physics-based machine learning.](https://www.sciencedirect.com/science/article/pii/S0045793018304250)
Computers & Fluids 179:704-717, 2019.
([Download](https://kiwi.oden.utexas.edu/papers/Physics-based-machine-learning-swischuk-willcox.pdf))<details><summary>BibTeX</summary><pre>
@article{swischuk2019projection,
  title    = {Projection-based model reduction: Formulations for physics-based machine learning},
  author   = {Swischuk, Renee and Mainini, Laura and Peherstorfer, Benjamin and Willcox, Karen},
  journal  = {Computers \& Fluids},
  volume   = {179},
  pages    = {704--717},
  year     = {2019},
  publisher={Elsevier}
}</pre></details>

- \[4\] Swischuk, R. Physics-based machine learning and data-driven reduced-order modeling, Master's thesis, Massachusetts Institute of Technology, 2019.
<!-- TODO: link -->

- \[5\] Swischuk, R. and Kramer, B. and Huang, C. and Willcox, K. [Learning physics-based reduced-order models for a single-injector combustion process](https://arxiv.org/abs/1908.03620). ArXiv preprint arXiv:1908.03620.
([Download](https://arxiv.org/pdf/1908.03620.pdf))<details><summary>BibTeX</summary><pre>
@article{swischuk2019learning,
  title={Learning physics-based reduced-order models for a single-injector combustion process},
  author={Swischuk, Renee and Kramer, Boris and Huang, Cheng and Willcox, Karen},
  journal={arXiv preprint arXiv:1908.03620},
  year={2019}
}</pre></details>

- \[6\] Peherstorfer, B. [Sampling low-dimensional Markovian dynamics for pre-asymptotically recovering reduced models from data with operator inference](https://arxiv.org/abs/1908.11233). ArXiv preprint arXiv:1908.11233.
([Download](https://arxiv.org/pdf/1908.11233.pdf))<details><summary>BibTeX</summary><pre>
@article{peherstorfer2019sampling,
  title={Sampling low-dimensional Markovian dynamics for pre-asymptotically recovering reduced models from data with operator inference},
  author={Peherstorfer, Benjamin},
  journal={arXiv preprint arXiv:1908.11233},
  year={2019}
}</pre></details>
