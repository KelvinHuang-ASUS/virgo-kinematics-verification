# Virgo Kinematics Verification

## Overview
This repository manages the kinematics architecture, URDF/Xacro models, and TF tree topology verification pipeline.

## Environment & Toolchain Status
- **Host OS**: Ubuntu 26.04 LTS (x86_64)
- **Core CLI Tools**:
  - liburdfdom-tools (provides check_urdf, urdf_to_graphviz) - Verified
  - graphviz (DOT rendering engine for PDF generation) - Verified
  - python3-venv & python3-pip - Configured
- **Python Environment**:
  - Dedicated virtual environment configured (.venv/)
  - Dependencies tracked in requirements.txt (xacro >= 2.0.0, pyyaml) - Verified

## Setup Instructions
1. Activate virtual environment: source .venv/bin/activate
2. Install dependencies: pip install -r requirements.txt

## Next Steps
1. Implement automated topology generation script (scripts/generate_topology.py).
2. Add gimbal Xacro/URDF model source files.
3. Validate TF tree topology and output PDF diagram.
