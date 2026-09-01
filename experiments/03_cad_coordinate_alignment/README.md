# Experiment 03: CAD Coordinate Alignment & Vendor Kinematic Chain

## Objective
Establish a production-grade kinematic baseline based on vendor-provided AP242 STEP solid geometry and precise transformation matrices (`CAD_Model_ER_260820`), fully mapped to internal standard nomenclature (`NOMENCLATURE_MAPPING.md`). This sandbox ensures exact alignment between CAD datum coordinate systems and ROS 2 URDF frame conventions.

---

## Reference Specifications & Nomenclature

- **3D Geometry**: [`cad_specs/ASUS-ER-EL-AS(0901).STEP`](cad_specs/ASUS-ER-EL-AS(0901).STEP) (AP242 format with embedded Datum Coordinate Systems)
- **Transformation Specs**: [`cad_specs/multiply the chain 0901.xlsx`](cad_specs/multiply%20the%20chain%200901.xlsx) (Sheet: `CAD_Model_ER_260820`)
- **Nomenclature Mapping**: [`NOMENCLATURE_MAPPING.md`](NOMENCLATURE_MAPPING.md) (Cross-reference mapping table between vendor CAD names and internal system standard frames)

---

## Kinematic Topology Chain (10 Internal Standard Nodes)

The kinematic chain follows a 10-node hierarchical transformation structure from the mount base down to individual payload sensors using internal system standard nomenclature:

```
gimbal_mnt_link
  └── gimbal_susp_link
        └── gimbal_motor_3_link (Roll Motor Axis)
              └── gimbal_motor_2_link (Yaw Motor Axis)
                    └── gimbal_motor_1_link (Pitch Motor Axis)
                          └── gimbal_payload_link
                                ├── imu_1_frame
                                ├── cam_narrow_link
                                ├── cam_tele_link
                                └── cam_wide_link
```

### Node List & Responsibilities
1. **`gimbal_mnt_link`**: Mount base / ISP box reference frame (Kinematic Root Base).
2. **`gimbal_susp_link`**: Vibration dampening suspension frame.
3. **`gimbal_motor_3_link`**: Gimbal Roll axis motor link (Motor 3).
4. **`gimbal_motor_2_link`**: Gimbal Yaw axis motor link (Motor 2).
5. **`gimbal_motor_1_link`**: Gimbal Pitch axis motor link (Motor 1).
6. **`gimbal_payload_link`**: Sensor payload carrier bracket link.
7. **`imu_1_frame`**: Inertial Measurement Unit reference frame.
8. **`cam_narrow_link`**: Narrow Field of View (NFOV) camera frame.
9. **`cam_tele_link`**: Telephoto camera reference frame.
10. **`cam_wide_link`**: Wide Field of View (WFOV) camera reference frame.

---

## ER_260820 Exact Transformation Matrix Constants

The 9 coordinate transformations connecting the 10 nodes are defined in [`xacro/virgo_cad_transforms.xacro`](xacro/virgo_cad_transforms.xacro) based on exact matrix conversions, mapped to internal standard joint names in [`xacro/virgo_gimbal.xacro`](xacro/virgo_gimbal.xacro):

| Internal Standard Joint Name | Parent Link | Child Link | Translation `xyz` (meters) | Rotation `rpy` (radians) |
| :--- | :--- | :--- | :--- | :--- |
| **`gimbal_mnt_to_susp_joint`** | `gimbal_mnt_link` | `gimbal_susp_link` | `0.064306 -0.000001 0.021546` | `0.0 0.0 0.0` |
| **`gimbal_susp_to_motor3_joint`** | `gimbal_susp_link` | `gimbal_motor_3_link` | `-0.070790 0.0 0.029217` | `0.0 1.178098 0.0` |
| **`gimbal_motor3_to_motor2_joint`** | `gimbal_motor_3_link` | `gimbal_motor_2_link` | `-0.039807 0.0 0.034129` | `0.0 0.750491 0.0` |
| **`gimbal_motor2_to_motor1_joint`** | `gimbal_motor_2_link` | `gimbal_motor_1_link` | `0.0 0.054600 0.078100` | `1.570796 1.570796 0.0` |
| **`gimbal_motor1_to_payload_joint`** | `gimbal_motor_1_link` | `gimbal_payload_link` | `-0.000069 -0.000666 0.060957` | `-1.570796 0.0 -2.783801` |
| **`gimbal_payload_to_imu_joint`** | `gimbal_payload_link` | `imu_1_frame` | `-0.018398 0.022833 0.023084` | `3.141593 1.570796 0.0` |
| **`gimbal_payload_to_narrow_joint`** | `gimbal_payload_link` | `cam_narrow_link` | `-0.025633 0.016500 -0.013660` | `-1.570796 0.0 -1.570796` |
| **`gimbal_payload_to_tele_joint`** | `gimbal_payload_link` | `cam_tele_link` | `-0.025633 -0.016500 -0.013660` | `-1.570796 0.0 -1.570796` |
| **`gimbal_payload_to_wide_joint`** | `gimbal_payload_link` | `cam_wide_link` | `0.017012 -0.000740 0.014340` | `-1.570796 0.0 -1.570796` |

---

## Verification Artifacts & Baseline Comparison

Automated pipeline runs (`generate_topology.py` and `render_joint_graph.py`) produce output files in [`output/03_cad_coordinate_alignment/`](../../output/03_cad_coordinate_alignment/). Baseline files are preserved alongside the internal standard outputs for comparative validation:

### A. Internal Standard Artifacts (Latest Pipeline Generation)
- **Compiled URDF Model**: [`../../output/03_cad_coordinate_alignment/virgo_gimbal_compiled.urdf`](../../output/03_cad_coordinate_alignment/virgo_gimbal_compiled.urdf)
- **Kinematic TF Tree Topology**:
  - Graphviz DOT descriptor: [`../../output/03_cad_coordinate_alignment/virgo_gimbal_topology.gv`](../../output/03_cad_coordinate_alignment/virgo_gimbal_topology.gv)
  - PDF vector tree graph: [`../../output/03_cad_coordinate_alignment/virgo_gimbal_topology.pdf`](../../output/03_cad_coordinate_alignment/virgo_gimbal_topology.pdf)
  - PNG image preview: [`../../output/03_cad_coordinate_alignment/virgo_gimbal_topology.png`](../../output/03_cad_coordinate_alignment/virgo_gimbal_topology.png)
- **Joint & Link Connection Graph**:
  - Graphviz DOT descriptor: [`../../output/03_cad_coordinate_alignment/virgo_gimbal_joint_graph.gv`](../../output/03_cad_coordinate_alignment/virgo_gimbal_joint_graph.gv)
  - PDF vector joint graph: [`../../output/03_cad_coordinate_alignment/virgo_gimbal_joint_graph.pdf`](../../output/03_cad_coordinate_alignment/virgo_gimbal_joint_graph.pdf)
  - PNG image preview: [`../../output/03_cad_coordinate_alignment/virgo_gimbal_joint_graph.png`](../../output/03_cad_coordinate_alignment/virgo_gimbal_joint_graph.png)

### B. Raw Vendor Baseline Artifacts (Preserved Baseline Comparison)
- **Raw Compiled URDF Model**: [`../../output/03_cad_coordinate_alignment/virgo_gimbal_raw_compiled.urdf`](../../output/03_cad_coordinate_alignment/virgo_gimbal_raw_compiled.urdf)
- **Raw Kinematic TF Tree Topology**:
  - Graphviz DOT descriptor: [`../../output/03_cad_coordinate_alignment/virgo_gimbal_raw_topology.gv`](../../output/03_cad_coordinate_alignment/virgo_gimbal_raw_topology.gv)
  - PDF vector tree graph: [`../../output/03_cad_coordinate_alignment/virgo_gimbal_raw_topology.pdf`](../../output/03_cad_coordinate_alignment/virgo_gimbal_raw_topology.pdf)
  - PNG image preview: [`../../output/03_cad_coordinate_alignment/virgo_gimbal_raw_topology.png`](../../output/03_cad_coordinate_alignment/virgo_gimbal_raw_topology.png)
- **Raw Joint & Link Connection Graph**:
  - Graphviz DOT descriptor: [`../../output/03_cad_coordinate_alignment/virgo_gimbal_raw_joint_graph.gv`](../../output/03_cad_coordinate_alignment/virgo_gimbal_raw_joint_graph.gv)
  - PDF vector joint graph: [`../../output/03_cad_coordinate_alignment/virgo_gimbal_raw_joint_graph.pdf`](../../output/03_cad_coordinate_alignment/virgo_gimbal_raw_joint_graph.pdf)
  - PNG image preview: [`../../output/03_cad_coordinate_alignment/virgo_gimbal_raw_joint_graph.png`](../../output/03_cad_coordinate_alignment/virgo_gimbal_raw_joint_graph.png)

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
