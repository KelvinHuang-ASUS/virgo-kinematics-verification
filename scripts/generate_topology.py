#!/usr/bin/env python3
"""
Kinematic Tree Topology Generator

Compiles Xacro macro files into complete URDFs and renders the 
corresponding kinematic TF tree topology to PDF using urdf_to_graphviz.
"""

import os
import subprocess
import sys
from pathlib import Path


def generate_topology(xacro_path: Path, output_dir: Path):
    if not xacro_path.exists():
        print(f"[-] Error: Target file '{xacro_path}' does not exist.")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)
    base_name = xacro_path.name.replace(".urdf.xacro", "").replace(".xacro", "").replace(".urdf", "")
    
    urdf_path = output_dir / f"{base_name}_compiled.urdf"
    pdf_base = output_dir / f"{base_name}_topology"

    print(f"[+] Compiling Xacro macro: {xacro_path} -> {urdf_path}")
    subprocess.run(["xacro", str(xacro_path), "-o", str(urdf_path)], check=True)

    print(f"[+] Generating kinematic TF tree PDF: {pdf_base}.pdf")
    subprocess.run(["urdf_to_graphviz", str(urdf_path), str(pdf_base)], check=True)
    
    print(f"[✓] Verification pipeline complete. Outputs generated in: {output_dir}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_topology.py <path_to_xacro_or_urdf> [output_dir]")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    target_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("output")
    generate_topology(input_file, target_dir)
