# Single Source of Truth (SSoT) for UAV Geometry and Inertia
This repository provides a Single Source of Truth (SSoT) for the UAV geometry. This geometry is defined through unambiguous Coordinate Reference Systems (CRS). Those CRS in turn are defined using the URDF (Unified Robot Description Format), the de-facto standard for defining the geometry of a robot (established by ROS). 
1. **The names for the URDF links serve as an API contract for CRS**: When referring to a CRS (e.g. when specifying coordinates) - whether in a design document, CAD file, or in source code - the link names defined in this URDF must be used to ensure consistency across all representations of the UAV.
1. The geometry and inertia properties defined in the URDF are used as the **source of truth for all downstream applications**, including:
    - Simulation: The URDF is used to create accurate simulations of the UAV, which are essential for testing and development.
   - Navigation and localization: The CRS are essential for navigation and localization tasks, allowing the UAV to understand its position and orientation in space.
   - Guidance and control: The CRS are also crucial for guidance and control algorithms, enabling the UAV to execute maneuvers and maintain stability.
   - Payload management: The CRS are also crucial for managing payloads, ensuring that they are correctly positioned and oriented relative to the UAV.


## URDF Structure and Components
The URDF files in this repository define:
- The components of the UAV, such as the main body, rotors, gimbals, and payloads.
- The physical properties of these components, including their dimensions, masses, and inertias.
- The connections between these components, including the joints and their types (e.g., fixed, revolute).

The main elements of a URDF files are links and joints. Links represent the physical components of the UAV, while joints define how these components are connected and can move relative to each other. Each link defines a coordinate frame, and the joints specify how these frames are related to each other. The name of a link therefore defines as the name of the corresponding CRS, which is used as the API contract for referring to that CRS in all other representations of the UAV geometry.

The URDF also includes visual and collision properties for each link, which are important for simulation and visualization purposes.

## Modular URDF for UAVs with Payloads
This repository contains a modular URDF (Unified Robot Description Format) for UAVs (Unmanned Aerial Vehicles) with payloads. The URDF is designed to be flexible and easily customizable, allowing users to create their own UAV configurations by including different components such as gimbals, cameras, and other payloads.

The URDF is structured using Xacro (XML Macros), which allows for the reuse of common xml snippets and simplifies the process of creating new UAV configurations. The main components included in this URDF are:
- **./xacro/orion_common.xacro**: This file contains common macros and definitions that are used across different UAV components, such as the definition of the PCB links and sensor frames.
- **./xacro/orion_components.xacro**: This file defines various components that can be included in a UAV, such as sensor PCBs, flight controller PCBs, and GNSS modules.
- **./xacro/orion_drone.xacro**: This file defines the base structure of the UAV, including the main body and rotors.
- **./xacro/orion_gimbal.xacro**: This file defines a gimbal component that can be attached to the UAV for mounting cameras or other payloads.

To create a new UAV configuration, users can include the desired components in a new Xacro file and specify the necessary parameters. For example, the `orion_with_gimbal.urdf.xacro` file demonstrates how to include both the drone and gimbal components, connect them via a URDF joint, and create a complete UAV configuration with a mounted gimbal. Users can further customize the UAV by adding additional components or modifying existing ones as needed.

## Usage
1. Install dependencies withing a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Generate the URDF file from the Xacro file:
   ```bash
   xacro orion_with_gimbal.urdf.xacro -o orion_with_gimbal.urdf
   ```
3. Optionally, in order to extract a topological tree from the generated URDF:
   ```bash
   urdf_to_graphviz orion_with_gimbal.urdf orion_with_gimbal_crs.pdf
   ```
   This requires the `urdf_to_graphviz` tool, which can be installed via apt:
   ```bash
   sudo apt install liburdfdom-tools graphviz
   ```

## Todo
### Inertia Tensors
1. `<inertial><origin ...>` defines the inertial frame of the link relative to the link frame.
1. The inertia matrix `(ixx, ixy, ...)` is expressed about that inertial frame origin and axes.

Hence, make sure the `<inertial><origin>` matches the frame in which your inertia tensor values are defined, not necessarily the link frame itself. You do not have to force the link frame itself to be at COM. You have two valid choices:
1. Put link frame where convenient for kinematics/joints, and set `<inertial><origin>` to the COM offset.
1. Put link frame at COM, and use `<inertial><origin xyz="0 0 0" rpy="0 0 0">`.

Best practice for stable dynamics:
1. Set `<inertial><origin>` at COM.
1. Align inertial axes with principal axes if possible. Then inertia tensor is mostly diagonal (`ixy`, `ixz`, `iyz` near zero). If not aligned, nonzero cross terms are expected and must be correct.
