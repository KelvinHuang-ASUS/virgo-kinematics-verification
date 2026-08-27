# ROS 2 Toolchain Installation & Pipeline Architecture Guide

This document details the toolchain, installation, and verification steps for the **Virgo Gimbal Kinematics Verification System**.

## 1. Toolchain Overview & Roles
- **xacro**: Evaluates XML macros, math parameters, and imports into a single unified URDF.
- **liburdfdom-tools (urdf_to_graphviz)**: Parses URDF links/joints hierarchy into DOT graph format (.gv).
- **graphviz (dot engine)**: Renders DOT descriptor into vector PDF tree.
- **generate_topology.py**: Python orchestrator combining xacro and urdf_to_graphviz in a single command.

## 2. Installation Procedures
1. System utilities: sudo apt update && sudo apt install -y liburdfdom-tools graphviz python3-pip python3-venv
2. Virtual environment: python3 -m venv .venv && source .venv/bin/activate
3. Python dependencies: pip install -r requirements.txt

## 3. Toolchain Verification Checklist
- Verify parser CLI: urdf_to_graphviz 2>&1 | head -n 2
- Verify Graphviz engine: dot -V
- Verify Python Xacro: python3 -c 'import xacro; print(xacro.__file__)'

## 4. Execution Workflow
Run the automated pipeline script:
python3 scripts/generate_topology.py src/urdf/orion-urdf-model/orion_gimbal.urdf.xacro output
