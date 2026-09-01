# Experiment 03: CAD Coordinate Alignment & Vendor Kinematic Chain

## Objective
Establish a production-grade kinematic baseline based on vendor-provided AP242 STEP solid geometry and precise transformation matrices (`CAD_Model_ER_260820`). This sandbox ensures exact alignment between CAD datum coordinate systems and ROS 2 URDF frame conventions.

---

## Reference Specifications & Geometry

- **3D Geometry**: [`cad_specs/ASUS-ER-EL-AS(0901).STEP`](cad_specs/ASUS-ER-EL-AS(0901).STEP) (AP242 format with embedded Datum Coordinate Systems)
- **Transformation Specs**: [`cad_specs/multiply the chain 0901.xlsx`](cad_specs/multiply%20the%20chain%200901.xlsx) (Sheet: `CAD_Model_ER_260820`)

---

## Kinematic Topology Chain (10 Transform Nodes)

The kinematic chain follows a 10-node hierarchical transformation structure from the mount base down to individual payload sensors:

```
ISP BOX
  └── Suspend
        └── Roll (Motor Axis)
              └── Yaw (Motor Axis)
                    └── Pitch (Motor Axis)
                          └── Payload
                                ├── IMU
                                ├── Narrow Camera
                                ├── Tele Camera
                                └── Wide Camera
```

### Node List & Responsibilities
1. **`isp_box_link`**: Mount base / ISP box reference frame.
2. **`suspend_link`**: Vibration dampening suspension frame.
3. **`roll_link`**: Gimbal Roll axis rotation link.
4. **`yaw_link`**: Gimbal Yaw axis rotation link.
5. **`pitch_link`**: Gimbal Pitch axis rotation link.
6. **`payload_link`**: Payload carrier bracket link holding sensor packages.
7. **`imu_link`**: Inertial Measurement Unit sensor frame.
8. **`narrow_cam_link`**: Narrow Field of View (NFOV) camera frame.
9. **`tele_cam_link`**: Telephoto camera frame.
10. **`wide_cam_link`**: Wide Field of View (WFOV) camera frame.

---

## ER_260820 Exact Transformation Matrix Constants

The 9 coordinate transformations connecting the 10 nodes are defined in [`xacro/virgo_cad_transforms.xacro`](xacro/virgo_cad_transforms.xacro) based on exact matrix conversions:

| Joint / Transform Node | Parent Link | Child Link | Translation `xyz` (meters) | Rotation `rpy` (radians) |
| :--- | :--- | :--- | :--- | :--- |
| **`isp_box_to_suspend`** | `isp_box_link` | `suspend_link` | `0.064306 -0.000001 0.021546` | `0.0 0.0 0.0` |
| **`suspend_to_roll`** | `suspend_link` | `roll_link` | `-0.070790 0.0 0.029217` | `0.0 1.178098 0.0` |
| **`roll_to_yaw`** | `roll_link` | `yaw_link` | `-0.039807 0.0 0.034129` | `0.0 0.750491 0.0` |
| **`yaw_to_pitch`** | `yaw_link` | `pitch_link` | `0.0 0.054600 0.078100` | `1.570796 1.570796 0.0` |
| **`pitch_to_payload`** | `pitch_link` | `payload_link` | `-0.000069 -0.000666 0.060957` | `-1.570796 0.0 -2.783801` |
| **`payload_to_imu`** | `payload_link` | `imu_link` | `-0.018398 0.022833 0.023084` | `3.141593 1.570796 0.0` |
| **`payload_to_narrow`** | `payload_link` | `narrow_cam_link` | `-0.025633 0.016500 -0.013660` | `-1.570796 0.0 -1.570796` |
| **`payload_to_tele`** | `payload_link` | `tele_cam_link` | `-0.025633 -0.016500 -0.013660` | `-1.570796 0.0 -1.570796` |
| **`payload_to_wide`** | `payload_link` | `wide_cam_link` | `0.017012 -0.000740 0.014340` | `-1.570796 0.0 -1.570796` |

---

## Compiled Verification Artifacts

Automated pipeline runs (`generate_topology.py` and `render_joint_graph.py`) generate the following verification artifacts in [`output/03_cad_coordinate_alignment/`](../../output/03_cad_coordinate_alignment/):

- **Compiled URDF Model**: [`../../output/03_cad_coordinate_alignment/virgo_gimbal_compiled.urdf`](../../output/03_cad_coordinate_alignment/virgo_gimbal_compiled.urdf)
- **Kinematic TF Tree Topology Artifacts**:
  - Graphviz DOT descriptor: [`../../output/03_cad_coordinate_alignment/virgo_gimbal_topology.gv`](../../output/03_cad_coordinate_alignment/virgo_gimbal_topology.gv)
  - PDF vector tree graph: [`../../output/03_cad_coordinate_alignment/virgo_gimbal_topology.pdf`](../../output/03_cad_coordinate_alignment/virgo_gimbal_topology.pdf)
  - PNG image preview: [`../../output/03_cad_coordinate_alignment/virgo_gimbal_topology.png`](../../output/03_cad_coordinate_alignment/virgo_gimbal_topology.png)
- **Joint & Link Connection Graph Artifacts**:
  - Graphviz DOT descriptor: [`../../output/03_cad_coordinate_alignment/virgo_gimbal_joint_graph.gv`](../../output/03_cad_coordinate_alignment/virgo_gimbal_joint_graph.gv)
  - PDF vector joint graph: [`../../output/03_cad_coordinate_alignment/virgo_gimbal_joint_graph.pdf`](../../output/03_cad_coordinate_alignment/virgo_gimbal_joint_graph.pdf)
  - PNG image preview: [`../../output/03_cad_coordinate_alignment/virgo_gimbal_joint_graph.png`](../../output/03_cad_coordinate_alignment/virgo_gimbal_joint_graph.png)

---

## External Inspection & Verification Procedure

To inspect and verify embedded Datum Coordinate Systems (CS) directly against vendor 3D models:

```bash
/mnt/Ubuntu_Data/Virgo_Gimbal/cad_assistant_1.6.0_2021-10-05_lin64.appimage cad_specs/ASUS-ER-EL-AS(0901).STEP
```

### Inspection Steps:
1. Open CAD Assistant using the executable path above.
2. Load the STEP file `cad_specs/ASUS-ER-EL-AS(0901).STEP`.
3. In the left panel, enable visibility for **Datum Coordinate Systems**.
4. Verify local origin positions $(x, y, z)$ in meters and orientation vectors against the parameters specified in `cad_specs/multiply the chain 0901.xlsx` (Sheet: `CAD_Model_ER_260820`).
