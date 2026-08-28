# Experiment 02: Joint Limits & Dynamics

## Overview
This experiment extends the baseline inertia model from Experiment 01 (`experiments/01_inertia_macros_setup/`) by introducing physical joint mechanical range limits (`revolute` joints) and dynamic parameters (viscous damping and static friction) for the **Virgo 3-Axis Gimbal System**.

By defining realistic angular bounds and joint dynamics, this model provides accurate physical boundaries required for controller design, trajectory optimization, and simulation in ROS 2 / Gazebo environment.

---

## Directory Structure
```
experiments/02_joint_limits_and_dynamics/
├── virgo_gimbal.urdf.xacro      # Top-level Xacro entrypoint
├── README.md                    # Technical documentation & joint limit specs
└── xacro/
    ├── inertia_macros.xacro     # Closed-form geometric inertia calculation macros
    ├── virgo_common.xacro       # Materials, sensor frame, and camera macros
    └── virgo_gimbal.xacro       # 3-axis gimbal URDF model with revolute limits & dynamics
```

---

## 3-Axis Joint Specifications & Dynamics

| Joint Name | Axis Name | Joint Type | Lower Limit (Rad / Deg) | Upper Limit (Rad / Deg) | Max Effort (N·m) | Max Velocity (rad/s) | Damping (N·m·s/rad) | Friction (N·m) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `j_gimbal_motor_3` | Yaw ($Z$-axis) | `revolute` | $-2.79253\text{ rad } (-160^\circ)$ | $+2.79253\text{ rad } (+160^\circ)$ | $1.5\text{ N}\cdot\text{m}$ | $6.28\text{ rad/s}$ | $0.05$ | $0.01$ |
| `j_gimbal_motor_2` | Roll ($X$-axis) | `revolute` | $-0.78540\text{ rad } (-45^\circ)$ | $+0.78540\text{ rad } (+45^\circ)$ | $1.2\text{ N}\cdot\text{m}$ | $6.28\text{ rad/s}$ | $0.05$ | $0.01$ |
| `j_gimbal_motor_1` | Pitch ($Y$-axis) | `revolute` | $-1.57080\text{ rad } (-90^\circ)$ | $+0.78540\text{ rad } (+45^\circ)$ | $1.2\text{ N}\cdot\text{m}$ | $6.28\text{ rad/s}$ | $0.05$ | $0.01$ |

### Joint Limit Details
1. **Yaw Joint (`j_gimbal_motor_3`)**: Range $\pm 160^\circ$ around the vertical $Z$-axis, providing wide search coverage while avoiding cable twisting.
2. **Roll Joint (`j_gimbal_motor_2`)**: Range $\pm 45^\circ$ around the longitudinal roll axis for horizon stabilization and bank angle compensation.
3. **Pitch Joint (`j_gimbal_motor_1`)**: Asymmetric range from $-90^\circ$ (pointing straight down / nadir view) to $+45^\circ$ (looking upward / skyward view).

---

## Verification Pipeline

To expand Xacro templates into compiled URDF XML, render the kinematic TF tree topology, and generate custom joint structure diagrams:

```bash
python3 scripts/generate_topology.py experiments/02_joint_limits_and_dynamics/virgo_gimbal.urdf.xacro output/02_joint_limits_and_dynamics
python3 scripts/render_joint_graph.py experiments/02_joint_limits_and_dynamics/virgo_gimbal.urdf.xacro output/02_joint_limits_and_dynamics
```

### Verification Artifacts Generated
- `output/02_joint_limits_and_dynamics/virgo_gimbal_compiled.urdf`: Compiled XML URDF containing expanded `<limit>` and `<dynamics>` blocks for all 3 motor joints.
- `output/02_joint_limits_and_dynamics/virgo_gimbal_topology.pdf`: Vector PDF graph of the kinematic TF frame hierarchy.
- `output/02_joint_limits_and_dynamics/virgo_gimbal_joint_graph.gv`: Custom Graphviz DOT joint structure descriptor.
- `output/02_joint_limits_and_dynamics/virgo_gimbal_joint_graph.png`: Rendered PNG diagram of the kinematic joint structure.


