"""Interactive demo: tweak a refractive-index field and ray parameters live."""
import numpy as np
from raytracer.refractive_index import RefractiveIndexField
from raytracer.ray import integrate_ray
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


def main():
    fig = plt.figure(figsize=(12, 8))
    fig.patch.set_facecolor('black')
    plt.subplots_adjust(left=0.06, right=0.98, top=0.95, bottom=0.32)

    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')

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

    # Slider layout: 4 rows x 5 columns spanning the bottom of the figure.
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
        {"name": "origin_y", "label": "Origin Y", "min": -4.0, "max": 0.0, "init": -3.0},
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

        xs = np.linspace(-sliders["x_span"].val, sliders["x_span"].val, int(sliders["x_count"].val))
        zs = np.linspace(-sliders["z_span"].val, sliders["z_span"].val, int(sliders["z_count"].val))
        origin_y = sliders["origin_y"].val
        direction = np.array([sliders["dir_x"].val, sliders["dir_y"].val, sliders["dir_z"].val])
        sensor_y = sliders["sensor_y"].val

        def sensor_plane(pos):
            return pos[1] >= sensor_y

        for x in xs:
            for z in zs:
                traj = integrate_ray(
                    np.array([x, origin_y, z]),
                    direction,
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

    # Initial draw
    update_scene()

    ax.set_xlim(bounds[0])
    ax.set_ylim(bounds[1])
    ax.set_zlim(bounds[2])
    for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
        axis.label.set_color('white')
        axis.set_tick_params(colors='white')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Ray paths through a Gaussian refractive-index bump', color='white')
    plt.show()


if __name__ == '__main__':
    main()
