"""Interactive demo: tweak a refractive-index field and ray parameters live."""
import time
import numpy as np
from raytracer.refractive_index import RefractiveIndexField
from raytracer.ray import ray
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def _normalize(v):
    v = np.asarray(v, dtype=float)
    n = np.linalg.norm(v)
    if n == 0:
        raise ValueError("zero-length vector")
    return v / n

def _orthonormal_basis(axis):
    axis = _normalize(axis)
    if abs(axis[0]) < 0.9:
        helper = np.array([1.0, 0.0, 0.0])
    else:
        helper = np.array([0.0, 1.0, 0.0])
    u = np.cross(axis, helper)
    u_norm = np.linalg.norm(u)
    if u_norm == 0:
        helper = np.array([0.0, 0.0, 1.0])
        u = np.cross(axis, helper)
        u_norm = np.linalg.norm(u)
    u /= u_norm
    v = np.cross(axis, u)
    return axis, u, v


def main():
    fig = plt.figure(figsize=(12, 8))
    fig.patch.set_facecolor('black')
    plt.subplots_adjust(left=0.06, right=0.98, top=0.95, bottom=0.32)

    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')
    ax.grid(False)

    bounds = np.array([[-2.5, 2.5], [-4.0, 2.0], [-2.0, 2.0]])

    # Visualize the refractive-index field as a semi-transparent scatter cloud
    grid_x = np.linspace(bounds[0][0], bounds[0][1], 12)
    grid_y = np.linspace(bounds[1][0], bounds[1][1], 12)
    grid_z = np.linspace(bounds[2][0], bounds[2][1], 12)
    gx, gy, gz = np.meshgrid(grid_x, grid_y, grid_z)
    sample_points = np.stack([gx.ravel(), gy.ravel(), gz.ravel()], axis=-1)

    def new_field_from_sliders(slider_map):
        return RefractiveIndexField(
            n0=slider_map["n0"].val,
            gaussians=[
                {
                    "amplitude": slider_map["amplitude"].val,
                    "center": np.array(
                        [slider_map["center_x"].val, slider_map["center_y"].val, slider_map["center_z"].val]
                    ),
                    "sigma": slider_map["sigma"].val,
                }
            ],
            linear_grad=np.array(
                [slider_map["grad_x"].val, slider_map["grad_y"].val, slider_map["grad_z"].val]
            ),
        )

    # Slider layout: 6 rows x 5 columns spanning the bottom of the figure.
    ray_mode_names = ["Grid", "Cone", "Sphere"]
    slider_specs = [
        {"name": "n0", "label": "n0", "min": 0.8, "max": 2.0, "init": 1.0},
        {"name": "amplitude", "label": "Gaussian A", "min": -30.0, "max": 30.0, "init": -20.0},
        {"name": "sigma", "label": "Sigma", "min": 0.5, "max": 5.0, "init": 2.6},
        {"name": "center_x", "label": "Center X", "min": -2.5, "max": 2.5, "init": 1.0},
        {"name": "center_y", "label": "Center Y", "min": -4.0, "max": 2.0, "init": 0.0},
        {"name": "center_z", "label": "Center Z", "min": -2.0, "max": 2.0, "init": 0.0},
        {"name": "grad_x", "label": "Grad X", "min": -15.0, "max": 15.0, "init": 0.0},
        {"name": "grad_y", "label": "Grad Y", "min": -15.0, "max": 15.0, "init": 10.0},
        {"name": "grad_z", "label": "Grad Z", "min": -15.0, "max": 15.0, "init": 0.0},
        {"name": "sensor_y", "label": "Sensor Y", "min": -1.0, "max": 3.0, "init": 1.5},
        {"name": "dir_x", "label": "Dir X", "min": -2.0, "max": 2.0, "init": 0.0},
        {"name": "dir_y", "label": "Dir Y", "min": 0.2, "max": 3.0, "init": 1.0},
        {"name": "dir_z", "label": "Dir Z", "min": -2.0, "max": 2.0, "init": 2.0},
        {"name": "ray_mode", "label": "Ray Mode", "min": 0, "max": 2, "init": 0, "step": 1},
        {"name": "cone_angle", "label": "Cone Angle", "min": 5.0, "max": 90.0, "init": 25.0},
        {"name": "origin_x", "label": "Origin X", "min": -2.5, "max": 2.5, "init": 0.0},
        {"name": "origin_y", "label": "Origin Y", "min": -4.0, "max": 2.0, "init": -3.0},
        {"name": "origin_z", "label": "Origin Z", "min": -2.0, "max": 2.0, "init": 0.0},
        {"name": "origin_move", "label": "Origin Move", "min": 0, "max": 1, "init": 0, "step": 1},
        {"name": "move_radius", "label": "Move Radius", "min": 0.0, "max": 2.0, "init": 0.6},
        {"name": "move_rate", "label": "Move Hz", "min": 0.0, "max": 1.0, "init": 0.2},
        {"name": "x_span", "label": "X Span", "min": 0.5, "max": 3.0, "init": 1.5},
        {"name": "z_span", "label": "Z Span", "min": 0.5, "max": 2.5, "init": 1.0},
        {"name": "x_count", "label": "# X Rays", "min": 2, "max": 9, "init": 5, "step": 1},
        {"name": "z_count", "label": "# Z Rays", "min": 2, "max": 7, "init": 3, "step": 1},
        {"name": "ds", "label": "ds", "min": 0.005, "max": 0.08, "init": 0.02},
        {"name": "steps", "label": "Steps", "min": 50, "max": 1200, "init": 600, "step": 10},
    ]
    sliders = {}
    cols = 5
    slider_width = 0.1
    slider_height = 0.022
    x_gap = 0.1
    y_gap = 0.055
    x_start = 0.06
    y_start = 0.28
    axcolor = "#1a1a1a"
    for i, spec in enumerate(slider_specs):
        row = i // cols
        col = i % cols
        left = x_start + col * (slider_width + x_gap)
        bottom = y_start - row * y_gap
        ax_slider = fig.add_axes([left, bottom, slider_width, slider_height], facecolor=axcolor)
        sliders[spec["name"]] = Slider(
            ax=ax_slider,
            label=spec["label"],
            valmin=spec["min"],
            valmax=spec["max"],
            valinit=spec["init"],
            valstep=spec.get("step", None),
            color="#ff8c00",
        )
        sliders[spec["name"]].label.set_color('white')
        sliders[spec["name"]].valtext.set_color('white')

    field = new_field_from_sliders(sliders)
    n_values = np.array([field.n(p) for p in sample_points])
    scatter = ax.scatter(
        sample_points[:, 0],
        sample_points[:, 1],
        sample_points[:, 2],
        c=n_values,
        cmap='plasma',
        alpha=0.55,
        s=15,
        linewidths=0,
    )
    cbar = fig.colorbar(scatter, ax=ax, shrink=0.7, pad=0.1)
    cbar.ax.tick_params(colors='white')
    cbar.set_label('Refractive index', color='white')
    ray_lines = []
    start_time = time.perf_counter()

    def animated_origin(base_origin, moving):
        if not moving:
            return base_origin
        radius = sliders["move_radius"].val
        rate = sliders["move_rate"].val
        phase = 2.0 * np.pi * rate * (time.perf_counter() - start_time)
        offset = np.array([radius * np.cos(phase), 0.0, radius * np.sin(phase)])
        return base_origin + offset

    def update_scene(_=None):
        # Update field and scatter colors
        new_field = new_field_from_sliders(sliders)
        n_vals = np.array([new_field.n(p) for p in sample_points])
        scatter.set_array(n_vals)
        scatter.set_clim(np.min(n_vals), np.max(n_vals))
        cbar.update_normal(scatter)

        # Redraw rays
        for line in ray_lines:
            line.remove()
        ray_lines.clear()

        x_span = sliders["x_span"].val
        z_span = sliders["z_span"].val
        x_count = int(sliders["x_count"].val)
        z_count = int(sliders["z_count"].val)
        base_origin = np.array([sliders["origin_x"].val, sliders["origin_y"].val, sliders["origin_z"].val])
        direction = np.array([sliders["dir_x"].val, sliders["dir_y"].val, sliders["dir_z"].val])
        sensor_y = sliders["sensor_y"].val
        ray_mode = ray_mode_names[int(sliders["ray_mode"].val)]
        origin_move = int(sliders["origin_move"].val)
        origin = animated_origin(base_origin, origin_move)
        sliders["ray_mode"].valtext.set_text(ray_mode)
        sliders["origin_move"].valtext.set_text("On" if origin_move else "Off")

        def ray_pairs():
            if ray_mode == "Grid":
                xs = np.linspace(-x_span, x_span, x_count) + origin[0]
                zs = np.linspace(-z_span, z_span, z_count) + origin[2]
                for x in xs:
                    for z in zs:
                        yield np.array([x, origin[1], z]), direction
                return

            if ray_mode == "Cone":
                theta_max = np.deg2rad(sliders["cone_angle"].val)
            else:
                theta_max = np.pi

            axis, u, v = _orthonormal_basis(direction)
            thetas = np.linspace(0.0, theta_max, z_count)
            phis = np.linspace(0.0, 2.0 * np.pi, x_count, endpoint=False)
            for theta in thetas:
                sin_t = np.sin(theta)
                cos_t = np.cos(theta)
                for phi in phis:
                    dir_vec = cos_t * axis + sin_t * (np.cos(phi) * u + np.sin(phi) * v)
                    yield origin, dir_vec

        ax.set_title(
            f"Ray paths through a Gaussian refractive-index bump (mode: {ray_mode})",
            color='white',
        )

        def sensor_plane(pos):
            return pos[1] >= sensor_y

        for ray_origin, ray_dir in ray_pairs():
            traj = ray(
                ray_origin,
                ray_dir,
                new_field,
                ds=sliders["ds"].val,
                steps=int(sliders["steps"].val),
                adaptive=True,
                domain_bounds=bounds,
                surfaces=[sensor_plane],
            )
            line, = ax.plot(traj[:, 0], traj[:, 1], traj[:, 2], linewidth=0.9, color='snow')
            ray_lines.append(line)
        fig.canvas.draw_idle()

    for s in sliders.values():
        s.on_changed(update_scene)

    def animation_tick():
        if int(sliders["origin_move"].val) == 0:
            return
        update_scene()

    timer = fig.canvas.new_timer(interval=120)
    timer.add_callback(animation_tick)
    timer.start()

    ax.set_xlim(bounds[0])
    ax.set_ylim(bounds[1])
    ax.set_zlim(bounds[2])
    for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
        axis.set_pane_color((0, 0, 0, 0))
        axis.line.set_color((0, 0, 0, 0))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_zlabel('')
    for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
        axis.set_tick_params(colors='white')

    # Initial draw
    update_scene()
    plt.show()


if __name__ == '__main__':
    main()
