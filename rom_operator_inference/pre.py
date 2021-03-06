# pre.py
"""Tools for preprocessing data."""

import numpy as _np
from scipy import linalg as _la
from scipy.linalg import svd as _svd
from scipy.sparse import linalg as _spla
from sklearn.utils import extmath as _sklmath
from matplotlib import pyplot as _plt


# Basis computation ===========================================================
def mean_shift(X):
    """Compute the mean of the columns of X, then use it to shift the columns
    so that they have mean zero.

    Parameters
    ----------
    X : (n,k) ndarray
        A matrix of k snapshots. Each column is a single snapshot.

    Returns
    -------
    xbar : (n,) ndarray
        The mean snapshot. Since this is a one-dimensional array, it must be
        reshaped to be applied to a matrix: Xshifted + xbar.reshape((-1,1)).

    Xshifted : (n,k) ndarray
        The matrix such that Xshifted[:,j] + xbar = X[:,j] for j=1,2,...,k.
    """
    # Check dimensions.
    if X.ndim != 2:
        raise ValueError("data X must be two-dimensional")

    xbar = _np.mean(X, axis=1)               # Compute the mean column.
    Xshifted = X - xbar.reshape((-1,1))     # Shift the columns by the mean.
    return xbar, Xshifted


def pod_basis(X, r, mode="simple", **options):
    """Compute the POD basis of rank r corresponding to the data in X.
    This function does NOT shift or scale the data before computing the basis.

    Parameters
    ----------
    X : (n,k) ndarray
        A matrix of k snapshots. Each column is a single snapshot.

    r : int
        The number of POD basis vectors to compute.

    mode : str
        The strategy to use for computing the truncated SVD of X. Options:
        * "simple" (default): Use scipy.linalg.svd() to compute the entire SVD
            of X, then truncate it to get the first r left singular vectors of
            X. May be inefficient for very large matrices.
        * "arpack": Use scipy.sparse.linalg.svds() to compute only the first r
            left singular vectors of X. This uses ARPACK for the eigensolver.
        * "randomized": Compute an approximate SVD with a randomized approach
            using sklearn.utils.extmath.randomized_svd(). This gives faster
            results at the cost of some accuracy.

    options
        Additional parameters for the SVD solver, which depends on `mode`:
        * "simple": scipy.linalg.svd()
        * "arpack": scipy.sparse.linalg.svds()
        * "randomized": sklearn.utils.extmath.randomized_svd()

    Returns
    -------
    Vr : (n,r) ndarray
        The first r POD basis vectors of X. Each column is one basis vector.
    """
    if mode == "simple":
        return _la.svd(X, full_matrices=False, **options)[0][:,:r]
    if mode == "arpack":
        return _spla.svds(X, r, which="LM", **options)[0][:,::-1]
    elif mode == "randomized":
        return _sklmath.randomized_svd(X, r, **options)[0][:,::-1]
    else:
        raise NotImplementedError(f"invalid mode '{mode}'")


# Reduced dimension selection =================================================
def significant_svdvals(X, eps, plot=False):
    """Count the number of singular values of X that are greater than eps.

    Parameters
    ----------
    X : (n,k) ndarray
        A matrix of k snapshots. Each column is a single snapshot.

    eps : float or list(floats)
        Cutoff value(s) for the singular values of X.

    plot : bool
        If True, plot the singular values and the cutoff value(s) against the
        singular value index.

    Returns
    -------
    ranks : int or list(int)
        The number of singular values greater than the cutoff value(s).
    """
    # Check dimensions.
    if X.ndim != 2:
        raise ValueError("data X must be two-dimensional")

    # Calculate the number of singular values above the cutoff value(s).
    singular_values = _la.svdvals(X)
    one_eps = _np.isscalar(eps)
    if one_eps:
        eps = [eps]
    ranks = [_np.count_nonzero(singular_values > ep) for ep in eps]

    if plot:
        # Visualize singular values and cutoff value(s).
        fig, ax = _plt.subplots(1, 1, figsize=(12,4))
        j = _np.arange(1, singular_values.size + 1)
        ax.semilogy(j, singular_values, 'C0*', ms=4, zorder=3)
        ax.set_xlim((0,j.size))
        ylim = ax.get_ylim()
        for ep,r in zip(eps, ranks):
            ax.hlines(ep, 0, r+1, color="black", linewidth=1)
            ax.vlines(r, ylim[0], singular_values[r-1] if r > 0 else ep,
                      color="black", linewidth=1)
        ax.set_ylim(ylim)
        ax.set_xlabel(r"Singular value index $j$")
        ax.set_ylabel(r"Singular value $\sigma_j$")

    return ranks[0] if one_eps else ranks


def energy_capture(X, thresh, plot=False):
    """Compute the number of singular values of X needed to surpass a given
    energy threshold. The energy of j singular values is defined by

        energy_j = sum(singular_values[:j]**2) / sum(singular_values**2).

    Parameters
    ----------
    X : (n,k) ndarray
        A matrix of k snapshots. Each column is a single snapshot.

    thresh : float or list(floats)
        Energy capture threshold(s).

    plot : bool
        If True, plot the singular values and the energy capture against
        the singular value index.

    Returns
    -------
    ranks : int or list(int)
        The number of singular values required to capture more than each
        energy capture threshold.
    """
    # Check dimensions.
    if X.ndim != 2:
        raise ValueError("data X must be two-dimensional")

    # Calculate singular values and cumulative energy.
    singular_values = _la.svdvals(X)
    svdvals2 = singular_values**2
    cumulative_energy = _np.cumsum(svdvals2) / _np.sum(svdvals2)

    # Determine the points at which the cumulative energy passes the threshold.
    one_thresh = _np.isscalar(thresh)
    if one_thresh:
        thresh = [thresh]
    ranks = [_np.searchsorted(cumulative_energy, th) + 1 for th in thresh]

    if plot:
        # Visualize cumulative energy and threshold value(s).
        fig, ax = _plt.subplots(1, 1, figsize=(12,4))
        j = _np.arange(1, singular_values.size + 1)
        ax.semilogy(j, cumulative_energy, 'C2.-', ms=4, zorder=3)
        ax.set_xlim(0, j.size)
        ylim = ax.get_ylim()
        for th,r in zip(thresh, ranks):
            ax.hlines(th, 0, r+1, color="black", linewidth=1)
            ax.vlines(r, ylim[0], cumulative_energy[r-1] if r > 0 else th,
                      color="black", linewidth=1)
        ax.set_ylim(ylim)
        ax.set_xlabel(r"Singular value index")
        ax.set_ylabel(r"Cumulative energy")

    return ranks[0] if one_thresh else ranks


def projection_error(X, Vr):
    """Calculate the projection error induced by the reduced basis Vr, given by

        err = ||X - Vr Vr^T X|| / ||X||,

    since (Vr Vr^T) is the orthogonal projector onto the range of Vr.

    Parameters
    ----------
    X : (n,k) or (k,) ndarray
        A 2D matrix of k snapshots where each column is a single snapshot, or a
        single 1D snapshot. If 2D, use the Frobenius norm; if 1D, the l2 norm.

    Vr : (n,r) ndarray
        The reduced basis of rank r. Each column is one basis vector.

    Returns
    -------
    error : float
        The projection error.
    """
    return _la.norm(X - Vr @ Vr.T @ X) / _la.norm(X)


def minimal_projection_error(X, eps, rmax=_np.inf, plot=False, **options):
    """Compute the number of POD basis vectors required to obtain a projection
    error less than eps. The projection error is defined by

        err = ||X - Vr Vr^T X||_F / ||X||_F,

    since (Vr Vr^T) is the orthogonal projection onto the range of Vr.

    Parameters
    ----------
    X : (n,k) ndarray
        A matrix of k snapshots. Each column is a single snapshot.

    eps : float or list(floats)
        Cutoff value(s) for the projection error.

    rmax : int
        The maximal number of basis vectors to check the projection error for.

    plot : bool
        If True, plot the POD basis rank r against the projection error.

    options
        Additional parameters for pre.pod_basis().

    Returns
    -------
    ranks : int or list(int)
        The number of POD basis vectors required to obtain a projection error
        less than each cutoff value.
    """
    # Check dimensions.
    if X.ndim != 2:
        raise ValueError("data X must be two-dimensional")

    # Get the largest POD basis and calculate the norm ||X||_F.
    rmax = min(min(X.shape), rmax)
    V = pod_basis(X, rmax, **options)
    X_norm = _la.norm(X, ord="fro")

    one_eps = _np.isscalar(eps)
    if one_eps:
        eps = [eps]

    errors = []
    rs = _np.arange(1, rmax)
    for j,r in enumerate(rs):
        # Get the POD basis of rank r and calculate the projection error.
        Vr = V[:,:r]
        errors.append(_la.norm(X - Vr @ Vr.T @ X, ord="fro") / X_norm)
    # Calculate the ranks needed to get under each cutoff value.
    errors = _np.array(errors)
    ranks = [_np.count_nonzero(errors > ep)+1 for ep in eps]

    if plot:
        fig, ax = _plt.subplots(1, 1, figsize=(12,4))
        ax.semilogy(rs, errors, 'C1.-', ms=4, zorder=3)
        ax.set_xlim((0,rs.size))
        ylim = ax.get_ylim()
        for ep,r in zip(eps, ranks):
            ax.hlines(ep, 0, r+1, color="black", linewidth=1)
            ax.vlines(r, ylim[0], ep, color="black", linewidth=1)
        ax.set_ylim(ylim)
        ax.set_xlabel(r"POD basis rank $r$")
        ax.set_ylabel(r"Projection error")

    return ranks[0] if one_eps else ranks


# Reprojection schemes ========================================================
def reproject_discrete(f, Vr, x0, niters, U=None):
    """Sample re-projected trajectories of the discrete dynamical system

        x_{j+1} = f(x_{j}, u_{j}),  x_{0} = x0.

    Parameters
    ----------
    f : callable mapping (n,) ndarray to (n,) ndarray
        Function defining the (full-order) discrete dynamical system.

    Vr : (n,r) ndarray
        Basis for the low-dimensional linear subspace (e.g., POD basis).

    x0 : (n,) ndarray
        Initial condition for the iteration in the high-dimensional space.

    niters : int
        The number of iterations to do.

    U : (m,niters-1) ndarray
        Control inputs, one for each iteration beyond the initial condition.

    Returns
    -------
    X_reprojected : (n,niters) ndarray
        Re-projected state trajectories in the original high-dimensional space.
    """
    # Validate and extract dimensions.
    n,_ = Vr.shape
    if x0.shape != (n,):
        raise ValueError("basis Vr and initial condition x0 not aligned")

    # Create the solution array and fill in the initial condition.
    Pr = Vr @ Vr.T                          # Projector onto linear subspace.
    X_rp = _np.empty((n,niters))
    X_rp[:,0] = Pr @ x0

    # Run the re-projection iteration.
    if U is None:
        for j in range(niters-1):
            X_rp[:,j+1] = Pr @ f(X_rp[:,j])
    elif U.ndim == 1:
        for j in range(niters-1):
            X_rp[:,j+1] = Pr @ f(X_rp[:,j], U[j])
    else:
        for j in range(niters-1):
            X_rp[:,j+1] = Pr @ f(X_rp[:,j], U[:,j])

    return X_rp


def reproject_continuous(f, Vr, X, U=None):
    """Sample with re-projection trajectories of the continuous system of ODEs

        dx / dt = f(t, x(t), u(t)),     x(0) = x0.

    Parameters
    ----------
    f : callable mapping (n,) ndarray to (n,) ndarray
        Function defining the differential equation.

    Vr : (n,r) ndarray
        Basis for the low-dimensional linear subspace.

    X : (n,k) ndarray
        State trajectories (training data).

    U : (m,k) ndarray
        Control inputs corresponding to the state trajectories.

    Returns
    -------
    X_reprojected : (n,k) ndarray
        Re-projected state trajectories in the original high-dimensional space.

    Xdot_reprojected : (n,k) ndarray
        Re-projected velocities in the original high-dimensional space.
    """
    # Validate and extract dimensions.
    if X.shape[0] != Vr.shape[0]:
        raise ValueError("X and Vr not aligned, first dimension "
                         f"{X.shape[0]} != {Vr.shape[0]}")
    n,_ = Vr.shape
    _,k = X.shape

    # Create the solution arrays.
    X_rp = Vr @ Vr.T @ X
    Xdot_rp = _np.empty_like(X)

    # Run the re-projection iteration.
    if U is None:
        for j in range(k):
            Xdot_rp[:,j] = f(X_rp[:,j])
    elif U.ndim == 1:
        for j in range(k):
            Xdot_rp[:,j] = f(X_rp[:,j], U[j])
    else:
        for j in range(k):
            Xdot_rp[:,j] = f(X_rp[:,j], U[:,j])

    return X_rp, Xdot_rp


# Derivative approximation ====================================================
def _fwd4(y, dt):                                           # pragma: no cover
    """Compute the first derivative of a uniformly-spaced-in-time array with a
    fourth-order forward difference scheme.

    Parameters
    ----------
    y : (5,...) ndarray
        Data to differentiate. The derivative is taken along the first axis.

    Returns
    -------
    dy0 : float or (...) ndarray
        Approximate derivative of y at the first entry, i.e., dy[0] / dt.
    """
    return (-25*y[0] + 48*y[1] - 36*y[2] + 16*y[3] - 3*y[4]) / (12*dt)


def _fwd6(y, dt):                                           # pragma: no cover
    """Compute the first derivative of a uniformly-spaced-in-time array with a
    sixth-order forward difference scheme.

    Parameters
    ----------
    y : (7,...) ndarray
        Data to differentiate. The derivative is taken along the first axis.

    Returns
    -------
    dy0 : float or (...) ndarray
        Approximate derivative of y at the first entry, i.e., dy[0] / dt.
    """
    return (-147*y[0] + 360*y[1] - 450*y[2] + 400*y[3] - 225*y[4] \
                                              + 72*y[5] - 10*y[6]) / (60*dt)


def xdot_uniform(X, dt, order=2):
    """Approximate the time derivatives for a chunk of snapshots that are
    uniformly spaced in time.

    Parameters
    ----------
    X : (n,k) ndarray
        The data to estimate the derivative of. The jth column is a snapshot
        that corresponds to the jth time step, i.e., X[:,j] = x(t[j]).

    dt : float
        The time step between the snapshots, i.e., t[j+1] - t[j] = dt.

    order : int {2, 4, 6}
        The order of the derivative approximation.
        See https://en.wikipedia.org/wiki/Finite_difference_coefficient.

    Returns
    -------
    Xdot : (n,k) ndarray
        Approximate time derivative of the snapshot data. The jth column is
        the derivative dx / dt corresponding to the jth snapshot, X[:,j].
    """
    # Check dimensions and input types.
    if X.ndim != 2:
        raise ValueError("data X must be two-dimensional")
    if not _np.isscalar(dt):
        raise TypeError("time step dt must be a scalar (e.g., float)")

    if order == 2:
        return _np.gradient(X, dt, edge_order=2, axis=1)

    Xdot = _np.empty_like(X)
    n,k = X.shape
    if order == 4:
        # Central difference on interior
        Xdot[:,2:-2] = (X[:,:-4] - 8*X[:,1:-3] + 8*X[:,3:-1] - X[:,4:])/(12*dt)

        # Forward difference on the front.
        for j in range(2):
            Xdot[:,j] = _fwd4(X[:,j:j+5].T, dt)                 # Forward
            Xdot[:,-j-1] = -_fwd4(X[:,-j-5:k-j].T[::-1], dt)    # Backward

    elif order == 6:
        # Central difference on interior
        Xdot[:,3:-3] = (-X[:,:-6] + 9*X[:,1:-5] - 45*X[:,2:-4] \
                        + 45*X[:,4:-2] - 9*X[:,5:-1] + X[:,6:]) / (60*dt)

        # Forward / backward differences on the front / end.
        for j in range(3):
            Xdot[:,j] = _fwd6(X[:,j:j+7].T, dt)                 # Forward
            Xdot[:,-j-1] = -_fwd6(X[:,-j-7:k-j].T[::-1], dt)    # Backward

    else:
        raise NotImplementedError(f"invalid order '{order}'; "
                                  "valid options: {2, 4, 6}")

    return Xdot


def xdot_nonuniform(X, t):
    """Approximate the time derivatives for a chunk of snapshots with a
    second-order finite difference scheme.

    Parameters
    ----------
    X : (n,k) ndarray
        The data to estimate the derivative of. The jth column is a snapshot
        that corresponds to the jth time step, i.e., X[:,j] = x(t[j]).

    t : (k,) ndarray
        The times corresponding to the snapshots. May not be uniformly spaced.
        See xdot_uniform() for higher-order computation in the case of
        evenly-spaced-in-time snapshots.

    Returns
    -------
    Xdot : (n,k) ndarray
        Approximate time derivative of the snapshot data. The jth column is
        the derivative dx / dt corresponding to the jth snapshot, X[:,j].
    """
    # Check dimensions.
    if X.ndim != 2:
        raise ValueError("data X must be two-dimensional")
    if t.ndim != 1:
        raise ValueError("time t must be one-dimensional")
    if X.shape[-1] != t.shape[0]:
        raise ValueError("data X not aligned with time t")

    # Compute the derivative with a second-order difference scheme.
    return _np.gradient(X, t, edge_order=2, axis=-1)


def xdot(X, *args, **kwargs):
    """Approximate the time derivatives for a chunk of snapshots with a finite
    difference scheme. Calls xdot_uniform() or xdot_nonuniform(), depending on
    the arguments.

    Parameters
    ----------
    X : (n,k) ndarray
        The data to estimate the derivative of. The jth column is a snapshot
        that corresponds to the jth time step, i.e., X[:,j] = x(t[j]).

    Additional parameters
    ---------------------
    dt : float
        The time step between the snapshots, i.e., t[j+1] - t[j] = dt.
    order : int {2, 4, 6} (optional)
        The order of the derivative approximation.
        See https://en.wikipedia.org/wiki/Finite_difference_coefficient.

    OR

    t : (k,) ndarray
        The times corresponding to the snapshots. May or may not be uniformly
        spaced.

    Returns
    -------
    Xdot : (n,k) ndarray
        Approximate time derivative of the snapshot data. The jth column is
        the derivative dx / dt corresponding to the jth snapshot, X[:,j].
    """
    n_args = len(args)          # Number of positional arguments (excluding X).
    n_kwargs = len(kwargs)      # Number of keyword arguments.
    n_total = n_args + n_kwargs # Total number of arguments (excluding X).

    if n_total == 0:
        raise TypeError("at least one other argument required (dt or t)")
    elif n_total == 1:              # There is only one other argument.
        if n_kwargs == 1:               # It is a keyword argument.
            arg_name = list(kwargs.keys())[0]
            if arg_name == "dt":
                func = xdot_uniform
            elif arg_name == "t":
                func = xdot_nonuniform
            elif arg_name == "order":
                raise TypeError("keyword argument 'order' requires float "
                                "argument dt")
            else:
                raise TypeError("xdot() got unexpected keyword argument "
                                f"'{arg_name}'")
        elif n_args == 1:               # It is a positional argument.
            arg = args[0]
            if isinstance(arg, float):          # arg = dt.
                func = xdot_uniform
            elif isinstance(arg, _np.ndarray):  # arg = t; do uniformity test.
                func = xdot_nonuniform
            else:
                raise TypeError(f"invalid argument type '{type(arg)}'")
    elif n_total == 2:              # There are two other argumetns: dt, order.
        func = xdot_uniform
    else:
        raise TypeError("xdot() takes from 2 to 3 positional arguments "
                        f"but {n_total+1} were given")

    return func(X, *args, **kwargs)


__all__ = [
            "mean_shift",
            "pod_basis",
            "significant_svdvals",
            "energy_capture",
            "projection_error",
            "minimal_projection_error",
            "reproject_discrete",
            "reproject_continuous",
            "xdot_uniform",
            "xdot_nonuniform",
            "xdot",
          ]
