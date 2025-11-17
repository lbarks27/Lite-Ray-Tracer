import numpy as np

class RefractiveIndexField:
    """A simple continuous refractive-index field.

    n(x) = n0 + linear_grad . x + sum_i A_i * exp(-||x-c_i||^2/(2*sigma_i^2))

    Methods
    -------
    n(x): returns scalar refractive index at point x (array-like length 3)
    grad_n(x): returns gradient vector of n at x
    """
    def __init__(self, n0=1.0, gaussians=None, linear_grad=None):
        self.n0 = float(n0)
        self.gaussians = gaussians or []
        if linear_grad is None:
            self.linear_grad = np.zeros(3, dtype=float)
        else:
            self.linear_grad = np.asarray(linear_grad, dtype=float)

    def n(self, x):
        x = np.asarray(x, dtype=float)
        val = self.n0 + float(np.dot(self.linear_grad, x))
        for g in self.gaussians:
            A = float(g.get('amplitude', 0.0))
            c = np.asarray(g.get('center', np.zeros(3)), dtype=float)
            sigma = float(g.get('sigma', 1.0))
            r2 = np.sum((x - c) ** 2)
            val += A * np.exp(-r2 / (2.0 * sigma * sigma))
        return float(val)

    def grad_n(self, x):
        x = np.asarray(x, dtype=float)
        grad = np.array(self.linear_grad, dtype=float)
        for g in self.gaussians:
            A = float(g.get('amplitude', 0.0))
            c = np.asarray(g.get('center', np.zeros(3)), dtype=float)
            sigma = float(g.get('sigma', 1.0))
            diff = x - c
            exp_term = np.exp(-np.sum(diff * diff) / (2.0 * sigma * sigma))
            # derivative of A * exp(-|x-c|^2/(2 sigma^2)) = A * exp(...) * (-(x-c)/sigma^2)
            grad += A * exp_term * (-(diff) / (sigma * sigma))
        return grad
