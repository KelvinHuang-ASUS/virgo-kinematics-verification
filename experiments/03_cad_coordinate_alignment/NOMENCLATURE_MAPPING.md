# Experiment 03: Nomenclature & Frame Mapping Specification

This document defines the cross-reference mapping between vendor CAD designations (`CAD_Model_ER_260820` / STEP models) and the Virgo Gimbal system internal standard nomenclature for all links and joints.

---

## 1. Complete Nomenclature Mapping Table

### A. Link Naming Mapping

| Vendor CAD Name (`CAD_Model_ER_260820`) | Legacy / Exp03 Draft Name | Internal Standard Link Name | Functional Role & Visual Description |
| :--- | :--- | :--- | :--- |
| **`ISP_BOX`** | `isp_box_link` | **`gimbal_mnt_link`** | Main ISP box mounting bracket (Kinematic Base Link). |
| **`SUSPENSION_PLATE`** | `suspend_link` | **`gimbal_susp_link`** | Vibration isolation dampening plate assembly. |
| **`ROLL_HOUSING`** | `roll_link` | **`gimbal_motor_3_link`** | Outer Roll axis motor housing and assembly (Motor 3). |
| **`YAW_HOUSING`** | `yaw_link` | **`gimbal_motor_2_link`** | Middle Yaw axis motor housing and arm (Motor 2). |
| **`PITCH_HOUSING`** | `pitch_link` | **`gimbal_motor_1_link`** | Inner Pitch axis motor housing and shaft (Motor 1). |
| **`PAYLOAD_BRACKET`** | `payload_link` | **`gimbal_payload_link`** | Sensor carrier plate holding optical & IMU payloads. |
| **`IMU_MODULE`** | `imu_link` | **`imu_1_frame`** | Internal Inertial Measurement Unit reference frame. |
| **`CAM_NARROW_ASSY`** | `narrow_cam_link` | **`cam_narrow_link`** | Narrow Field-of-View (NFOV) optical camera frame. |
| **`CAM_TELE_ASSY`** | `tele_cam_link` | **`cam_tele_link`** | Telephoto long-range camera reference frame. |
| **`CAM_WIDE_ASSY`** | `wide_cam_link` | **`cam_wide_link`** | Wide Field-of-View (WFOV) camera reference frame. |
| **`CAM_NARROW_CV`** | N/A | **`cam_narrow_cv_frame`** | OpenCV optical reference frame for Narrow camera ($Z$-axis forward optical axis, $X$-axis right, $Y$-axis down). |
| **`CAM_TELE_CV`** | N/A | **`cam_tele_cv_frame`** | OpenCV optical reference frame for Telephoto camera ($Z$-axis forward optical axis, $X$-axis right, $Y$-axis down). |
| **`CAM_WIDE_CV`** | N/A | **`cam_wide_cv_frame`** | OpenCV optical reference frame for Wide camera ($Z$-axis forward optical axis, $X$-axis right, $Y$-axis down). |

### B. Joint Naming & Kinematic DoF Mapping

| Vendor Datum Transform Pair | Legacy / Exp03 Draft Joint Name | Internal Standard Joint Name | Joint Type | Motion Axis / DoF |
| :--- | :--- | :--- | :--- | :--- |
| **`ISP_BOX` $\rightarrow$ `SUSPENSION`** | `isp_box_to_suspend` | **`gimbal_mnt_to_susp_joint`** | Fixed | Rigid connection ($0$ DoF) |
| **`SUSPENSION` $\rightarrow$ `ROLL_AXIS`** | `suspend_to_roll` | **`gimbal_susp_to_motor3_joint`** | Revolute | Roll axis rotation ($X$-axis, $\pm 45^\circ$) |
| **`ROLL_AXIS` $\rightarrow$ `YAW_AXIS`** | `roll_to_yaw` | **`gimbal_motor3_to_motor2_joint`** | Revolute | Yaw axis rotation ($Z$-axis, $\pm 160^\circ$) |
| **`YAW_AXIS` $\rightarrow$ `PITCH_AXIS`** | `yaw_to_pitch` | **`gimbal_motor2_to_motor1_joint`** | Revolute | Pitch axis rotation ($Y$-axis, $-90^\circ / +45^\circ$) |
| **`PITCH_AXIS` $\rightarrow$ `PAYLOAD`** | `pitch_to_payload` | **`gimbal_motor1_to_payload_joint`** | Fixed | Rigid connection ($0$ DoF) |
| **`PAYLOAD` $\rightarrow$ `IMU`** | `payload_to_imu` | **`gimbal_payload_to_imu_joint`** | Fixed | Sensor alignment ($0$ DoF) |
| **`PAYLOAD` $\rightarrow$ `NARROW_CAM`** | `payload_to_narrow` | **`gimbal_payload_to_narrow_joint`** | Fixed | Optical alignment ($0$ DoF) |
| **`PAYLOAD` $\rightarrow$ `TELE_CAM`** | `payload_to_tele` | **`gimbal_payload_to_tele_joint`** | Fixed | Optical alignment ($0$ DoF) |
| **`PAYLOAD` $\rightarrow$ `WIDE_CAM`** | `payload_to_wide` | **`gimbal_payload_to_wide_joint`** | Fixed | Optical alignment ($0$ DoF) |
| **`NARROW_CAM` $\rightarrow$ `NARROW_CV`** | N/A | **`cam_narrow_cv_j`** | Fixed | Optical frame convention rotation ($0$ DoF) |
| **`TELE_CAM` $\rightarrow$ `TELE_CV`** | N/A | **`cam_tele_cv_j`** | Fixed | Optical frame convention rotation ($0$ DoF) |
| **`WIDE_CAM` $\rightarrow$ `WIDE_CV`** | N/A | **`cam_wide_cv_j`** | Fixed | Optical frame convention rotation ($0$ DoF) |

---

## 2. Revision History & Alias Tracking

### Version 1.0.0 (Raw Vendor Draft Alignment)
- **Initial State**: Links and joints were named using generic vendor descriptors (`isp_box_link`, `suspend_link`, `roll_link`, `yaw_link`, `pitch_link`, `payload_link`, etc.).
- **Baseline Files Preserved**: Generated outputs from this initial draft were backed up in [`output/03_cad_coordinate_alignment/`](../../output/03_cad_coordinate_alignment/) as:
  - `virgo_gimbal_raw_compiled.urdf`
  - `virgo_gimbal_raw_topology.pdf` / `.png` / `.gv`
  - `virgo_gimbal_raw_joint_graph.pdf` / `.png` / `.gv`

### Version 1.1.0 (Internal Standard Mapping Refactoring)
- **Rationale**: Aligned all link identifiers and joint tags with the production system naming standards (`gimbal_mnt_link`, `gimbal_susp_link`, `gimbal_motor_3_link` for Roll, `gimbal_motor_2_link` for Yaw, `gimbal_motor_1_link` for Pitch, `gimbal_payload_link`, `imu_1_frame`, `cam_narrow_link`, `cam_tele_link`, `cam_wide_link`).
- **Kinematic Integrity**: The transformation parameters ($x, y, z$ translations and $r, p, y$ rotations) remain identical to the vendor `CAD_Model_ER_260820` specification sheet while enforcing consistent naming across ROS 2 TF topics and internal verification tools.

### Version 1.2.0 (OpenCV Camera Optical Frame Architecture Optimization)
- **Rationale**: Extended camera links (`cam_narrow_link`, `cam_tele_link`, `cam_wide_link`) with standardized OpenCV camera optical reference frames (`cam_narrow_cv_frame`, `cam_tele_cv_frame`, `cam_wide_cv_frame`) and fixed joints (`cam_narrow_cv_j`, `cam_tele_cv_j`, `cam_wide_cv_j`).
- **Coordinate System Alignment**: Formally bridged ROS REP-103 robot body frame conventions ($X$-axis forward, $Y$-axis left, $Z$-axis up) with standard optical frame conventions ($Z$-axis forward optical axis, $X$-axis right, $Y$-axis down) using static transform $rpy = (-1.570796, 0.0, -1.570796)$.
