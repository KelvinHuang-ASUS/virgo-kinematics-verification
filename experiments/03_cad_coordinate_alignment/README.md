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
