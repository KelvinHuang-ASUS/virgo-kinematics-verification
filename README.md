# Virgo Kinematics Verification

## Overview
This repository manages the kinematics architecture, URDF/Xacro models, and TF tree topology verification pipeline for the gimbal system.

## Environment & Toolchain Status
- **Host OS**: Ubuntu 26.04 LTS (x86_64)
- **Core CLI Tools**:
  - `liburdfdom-tools` (provides `check_urdf`, `urdf_to_graphviz`) — *Verified*
  - `graphviz` (DOT rendering engine for PDF generation) — *Verified*
  - `python3-venv` & `python3-pip` — *Configured*

## Next Steps
1. Set up dedicated Python virtual environment (`venv`).
2. Configure dependencies in `requirements.txt` (`xacro`).
3. Implement automated topology generation script (`generate_topology.py`).
