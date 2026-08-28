# Experiment 01: Inertia Macros & Setup

## Overview
This experimental workspace provides an isolated environment for tuning, verifying, and validating physical inertia parameters, center-of-mass (COM) offsets, and coordinate reference frames for the **Virgo 3-Axis Gimbal Payload Assembly**.

By maintaining this standalone experiment workspace, all model iterations and parameter tuning operate independently without mutating the baseline model located at `src/urdf/orion-urdf-model/`.

---

## Directory Structure
```
experiments/01_inertia_macros_setup/
├── virgo_gimbal.urdf.xacro      # Top-level Xacro entrypoint
├── README.md                    # Technical documentation & usage instructions
└── xacro/
    ├── inertia_macros.xacro     # Closed-form geometric inertia calculation macros
    ├── virgo_common.xacro       # Materials, sensor frame, and camera macros
    └── virgo_gimbal.xacro       # 3-axis gimbal URDF model with full inertial properties
```

---

## Technical Features & Mathematics

### 1. Geometric Inertia Macros (`xacro/inertia_macros.xacro`)
Standard closed-form inertia tensor formulas for rigid geometric bodies:
- **Rectangular Solid (Box)**:
  $$I_{xx} = \frac{1}{12} m (y^2 + z^2), \quad I_{yy} = \frac{1}{12} m (x^2 + z^2), \quad I_{zz} = \frac{1}{12} m (x^2 + y^2)$$
- **Solid Cylinder (aligned along Z axis)**:
  $$I_{xx} = I_{yy} = \frac{1}{12} m (3r^2 + h^2), \quad I_{zz} = \frac{1}{2} m r^2$$
- **Solid Sphere**:
  $$I_{xx} = I_{yy} = I_{zz} = \frac{2}{5} m r^2$$

### 2. Complete Link Inertial Definitions
All 8 physical links in `virgo_gimbal.xacro` (`gimbal_base_link`, `gimbal_mnt_link`, `gimbal_susp_link`, `gimbal_motor_3_link`, `gimbal_motor_2_link`, `gimbal_motor_1_link`, `gimbal_amba_bd_link`, `lrf_gimbal_frame`) as well as camera payload links feature explicit `<inertial>` definitions. All inertia matrices are verified to be strictly positive-definite.

### 3. Coordinate Frame Integrity
- **Camera Optical Frame (`_link`)**: Follows standard CAD/robotics convention ($X$: Forward / Optical axis, $Y$: Right, $Z$: Down).
- **Computer Vision Frame (`_cv_frame`)**: Follows OpenCV convention ($Z$: Depth / Optical axis, $X$: Right, $Y$: Down). Axis rotation matrix joint mapping: $\text{rpy} = (-90^\circ, 0^\circ, -90^\circ)$.
- **Laser Range Finder Frame (`lrf_gimbal_frame`)**: Range beam emitted along $+X$ axis.

---

## Verification Pipeline

To expand Xacro templates into compiled URDF XML, render the kinematic TF tree topology, and generate custom joint structure diagrams:

```bash
python3 scripts/generate_topology.py experiments/01_inertia_macros_setup/virgo_gimbal.urdf.xacro output/01_inertia_macros_setup
python3 scripts/render_joint_graph.py experiments/01_inertia_macros_setup/virgo_gimbal.urdf.xacro output/01_inertia_macros_setup
```

### Verification Artifacts Generated
- `output/01_inertia_macros_setup/virgo_gimbal_compiled.urdf`: Compiled XML URDF containing all expanded `<inertial>` elements.
- `output/01_inertia_macros_setup/virgo_gimbal_topology.pdf`: Vector PDF graph of the kinematic TF frame hierarchy.
- `output/01_inertia_macros_setup/virgo_gimbal_joint_graph.gv`: Custom Graphviz DOT joint structure descriptor.
- `output/01_inertia_macros_setup/virgo_gimbal_joint_graph.png`: Rendered PNG diagram of the kinematic joint structure.


