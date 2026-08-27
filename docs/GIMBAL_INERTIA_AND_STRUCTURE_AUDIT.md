# Gimbal Subsystem Physical Inertia and Kinematic Structure Audit Report

## 1. Overview & Objective
This document presents the structural, kinematic, and physical inertia audit for the **Virgo Gimbal Subsystem**. The objective is to establish an inventory of all links defined within the URDF/Xacro representation, analyze current `<inertial>` parameters, evaluate mass and center of mass (COM) offsets, and identify compliance gaps prior to dynamic simulation and control pipeline integration.

---

## 2. File Associations & Architectural Scope
The scope of this audit is strictly isolated to the standalone Gimbal Subsystem (`orion_gimbal`). The primary source files involved in this architecture are:

- **Target Entrypoint**: [`src/urdf/orion-urdf-model/orion_gimbal.urdf.xacro`](../src/urdf/orion-urdf-model/orion_gimbal.urdf.xacro)
- **Gimbal Macro Definition**: [`src/urdf/orion-urdf-model/xacro/orion_gimbal.xacro`](../src/urdf/orion-urdf-model/xacro/orion_gimbal.xacro)
- **Common Utility & Sensor Macros**: [`src/urdf/orion-urdf-model/xacro/orion_common.xacro`](../src/urdf/orion-urdf-model/xacro/orion_common.xacro)
- **Compiled URDF Artifact**: [`output/orion_gimbal_compiled.urdf`](../output/orion_gimbal_compiled.urdf)

---

## 3. Gimbal Subsystem 13-Link Audit Matrix

The Gimbal Subsystem comprises **13 link nodes** (8 physical structural links/PCBs, 4 camera links, 4 virtual CV frames, 1 LRF sensor frame, and 1 root anchor frame).

| Link Identifier | Visual Geometry / Link Type | Visual Origin Offset (`xyz`, `rpy`) | Current `<inertial>` Status | Physical Compliance & Risk Assessment |
| :--- | :--- | :--- | :--- | :--- |
| **`gimbal_mnt_frame_child`** | Virtual Anchor Root | None | Missing (Intentional) | **Compliant**: Pure kinematic root frame; zero mass expected. |
| **`gimbal_mnt_link`** | Box (`0.06 0.08 0.06` m) | `xyz="0.03 0 0"` | **Missing** | ❌ **Non-compliant**: Missing mass & inertia tensor. Visual COM offset requires `<origin>`. |
| **`gimbal_base_link`** | Box (`0.05 0.05 0.01` m) | `xyz="0 0 0.005"` | **Missing** | ❌ **Non-compliant**: Missing mass & inertia tensor. Visual COM offset requires `<origin>`. |
| **`gimbal_susp_link`** | Box (`0.04 0.04 0.01` m) | `xyz="0 0 -0.005"` | **Missing** | ❌ **Non-compliant**: Missing mass & inertia tensor. Visual COM offset requires `<origin>`. |
| **`gimbal_motor_3_link`** (Yaw Axis) | Cylinder (`r=0.015 h=0.02` m) | `xyz="0 0 0"` | **Missing** | ❌ **Non-compliant**: Missing mass & inertia tensor for rotational motor link. |
| **`gimbal_motor_2_link`** (Roll/Pitch Axis) | Cylinder + Composite Arm Box | Composite (`0.01 -0.02 -0.025`, `0.785 0 0`) | **Missing** | ❌ **Non-compliant**: Missing composite COM origin and inertia tensor for asymmetric arm. |
| **`gimbal_motor_1_link`** (Pitch/Yaw Axis) | Cylinder + Composite Arm Box | Composite (`-0.025 0.01 -0.015`, `0 -0.785 0`) | **Missing** | ❌ **Non-compliant**: Missing composite COM origin and inertia tensor for asymmetric arm. |
| **`gimbal_amba_bd_link`** (Amba PCB) | Box (`0.05 0.07 0.002` m) | `xyz="0 0 0"` | **Missing** | ❌ **Non-compliant**: Missing thin-plate PCB mass & inertia tensor. |
| **`cam_wide_link`** | Cylinder (`r=0.008 h=0.01` m) | `xyz="0.005 0 0" rpy="0 1.5708 0"` | **Missing** | ❌ **Non-compliant**: Lens visual offset present; missing camera mass & inertia tensor. |
| **`cam_narrow_link`** | Cylinder (`r=0.005 h=0.01` m) | `xyz="0.005 0 0" rpy="0 1.5708 0"` | **Missing** | ❌ **Non-compliant**: Lens visual offset present; missing camera mass & inertia tensor. |
| **`cam_tele_link`** | Cylinder (`r=0.012 h=0.02` m) | `xyz="0.005 0 0" rpy="0 1.5708 0"` | **Missing** | ❌ **Non-compliant**: Lens visual offset present; missing camera mass & inertia tensor. |
| **`cam_thermal_link`** | Cylinder (`r=0.006 h=0.01` m) | `xyz="0.005 0 0" rpy="0 1.5708 0"` | **Missing** | ❌ **Non-compliant**: Lens visual offset present; missing camera mass & inertia tensor. |
| **`cam_*_cv_frame`** (x4) | Virtual Computer Vision Frame | None | Missing (Intentional) | **Compliant**: Pure optical coordinate frame; zero mass expected. |
| **`lrf_gimbal_frame`** | Box (`0.01 0.01 0.01` m) | `xyz="0.005 0 0"` | **Missing** | ❌ **Non-compliant**: Missing laser range finder sensor mass & inertia tensor. |

---

## 4. Key Findings & Physical Dynamics Risk Analysis

1. **Total Absence of Physical Inertia Tags**:
   All 8 physical structural links and 5 payload links completely lack `<inertial>` tags. While the model compiles cleanly via ROS 2 `xacro` and exports valid Graphviz kinematic topology diagrams (`.pdf`/`.gv`), it is currently unviable for physics engines (e.g., Gazebo, Isaac Sim, MuJoCo) or PX4 inertia-based control dynamics.

2. **COM Offset Mismatches**:
   Several links (e.g., `gimbal_mnt_link`, `gimbal_base_link`, `gimbal_susp_link`, and camera links) define non-zero visual origin offsets. The `<inertial><origin>` tags must be explicitly aligned with the physical Center of Mass (COM) rather than defaulted to zero.

3. **Composite Geometry Inertia Calculation**:
   Motor links `gimbal_motor_2_link` and `gimbal_motor_1_link` consist of multi-geometry visual elements (cylindrical actuators attached to angled structural bracket boxes). The inertial parameters for these links require composite body calculations using the Parallel Axis Theorem.

---

## 5. Planned Remediation Steps
1. **Modular Inertia Macro Architecture**: Design modular Xacro macros in `orion_common.xacro` for standard geometric primitives (box, cylinder, point mass).
2. **Inertia Tensor Calculation & Positive-Definiteness Enforcement**: Calculate standard masses based on material densities and geometry dimensions, ensuring all inertia tensors satisfy positive-definiteness ($I_{xx}, I_{yy}, I_{zz} > 0$) and physical triangle inequalities ($I_{xx} + I_{yy} > I_{zz}$).
3. **Coordinate Reference System (CRS) Verification**: Verify optical axis and computer vision depth frame rotations across all camera optical links.
4. **Pipeline Re-verification**: Execute `generate_topology.py` to confirm compile integrity and output topology generation.
