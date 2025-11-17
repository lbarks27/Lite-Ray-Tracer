import numpy as np
from raytracer.refractive_index import RefractiveIndexField
from raytracer.ray import integrate_ray


def test_straight_in_constant_field():
    # In a constant refractive index field (no gradients), rays must be straight lines.
    field = RefractiveIndexField(n0=1.33, gaussians=[], linear_grad=np.zeros(3))
    r0 = np.array([0.0, 0.0, 0.0])
    dir0 = np.array([0.3, 0.4, 0.5])
    ds = 0.05
    steps = 100
    traj = integrate_ray(r0, dir0, field, ds=ds, steps=steps)

    # Expected: r(s) = r0 + s * u (u normalized initial direction)
    u = dir0 / np.linalg.norm(dir0)
    s_values = np.linspace(0.0, steps * ds, steps + 1)
    expected = r0[np.newaxis, :] + np.outer(s_values, u)

    max_err = np.max(np.linalg.norm(traj - expected, axis=1))
    assert max_err < 1e-8
