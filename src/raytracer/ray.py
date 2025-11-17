import numpy as np


def _normalize(v):
    v = np.asarray(v, dtype=float)
    n = np.linalg.norm(v)
    if n == 0:
        raise ValueError("zero-length vector")
    return v / n


def integrate_ray(r0, dir0, field, ds=0.01, steps=1000):
    """Integrate a ray through a continuous refractive-index field.

    We use the first-order system with state [r, p] where p = n(r) * dr/ds.

    Equations:
      dr/ds = p / n(r)
      dp/ds = grad_n(r)

    Parameters
    ----------
    r0 : array-like (3,)   initial position
    dir0: array-like (3,)  initial direction (need not be unit length)
    field: RefractiveIndexField instance with n(x) and grad_n(x)
    ds: float step-size in path-length s
    steps: int number of steps

    Returns
    -------
    traj : ndarray shape (steps+1, 3) positions along ray
    """
    r = np.asarray(r0, dtype=float)
    u0 = _normalize(dir0)
    n0 = field.n(r)
    p = n0 * u0

    traj = np.zeros((steps + 1, 3), dtype=float)
    traj[0] = r.copy()

    # state = [r_x, r_y, r_z, p_x, p_y, p_z]
    state = np.empty(6, dtype=float)
    state[0:3] = r
    state[3:6] = p

    def deriv(sstate):
        r = sstate[0:3]
        p = sstate[3:6]
        n = field.n(r)
        drds = p / n
        dpds = field.grad_n(r)
        return np.concatenate([drds, dpds])

    for i in range(1, steps + 1):
        k1 = deriv(state)
        k2 = deriv(state + 0.5 * ds * k1)
        k3 = deriv(state + 0.5 * ds * k2)
        k4 = deriv(state + ds * k3)
        state = state + (ds / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        traj[i] = state[0:3]

    return traj
