# Virgo Gimbal Kinematics & Topology Verification Pipeline

This repository hosts the kinematics architecture, URDF/Xacro models, and TF tree topology verification pipeline for the **Virgo Gimbal System**.

The entire compilation and rendering workflow is powered by the **ROS 2 native robotics toolchain**, ensuring strict coordinate frame integrity and structural compliance.

---

## Technical Documentation
- **Architecture & Setup Guide**: [docs/TOOLCHAIN_AND_PIPELINE_GUIDE.md](docs/TOOLCHAIN_AND_PIPELINE_GUIDE.md) - Comprehensive reference detailing toolchain roles, installation steps, and pipeline orchestration.

---

## 1. Modular Extraction Architecture
- **Target Entrypoint**: `src/urdf/orion-urdf-model/orion_gimbal.urdf.xacro`
- **Mechanism**: Evaluates the standalone gimbal macro defined in `xacro/orion_gimbal.xacro` without instantiating the entire UAV assembly.
- **Root Frame**: `gimbal_mnt_frame_child` serves as the root link isolating the suspension, 3-axis motor chain, and sensor payloads.

---

## 2. ROS 2 Toolchain Conversion Pipeline
1. **xacro**: Expands macro templates into standard URDF XML.
2. **liburdfdom-tools (urdf_to_graphviz)**: Validates TF DOM and generates DOT graph descriptor.
3. **graphviz (dot)**: Compiles DOT descriptor into vector PDF tree.

---

## 3. Verification Artifacts & Visual Proof
### A. Compiled URDF & 3D Kinematic Visual Preview
![3D Kinematic Model Preview](docs/images/01_urdf_3d_preview.png)

### B. Graphviz DOT Topological Source Code
![Graphviz DOT Preview](docs/images/02_graphviz_dot_source.png)

### C. Generated Kinematic TF Tree Topology (PDF)
![Kinematic TF Tree](docs/images/03_tf_tree_topology_pdf.png)

---

## 4. Quick Start & Reproduction
1. Activate virtual environment: `source .venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Execute automated pipeline: `python3 scripts/generate_topology.py src/urdf/orion-urdf-model/orion_gimbal.urdf.xacro output`
