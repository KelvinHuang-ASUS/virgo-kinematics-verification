#!/usr/bin/env python3
"""
Custom Kinematic Joint Graph Renderer

Parses URDF/Xacro files to generate custom Graphviz kinematic joint structure diagrams.
Root links are styled as yellow rounded boxes, standard links as slate rounded boxes,
fixed joints as dark gray dashed arrows, and revolute/continuous joints as bold blue arrows.
"""

import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def render_joint_graph(input_path: Path, output_dir: Path):
    if not input_path.exists():
        print(f"[-] Error: Target file '{input_path}' does not exist.")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)
    base_name = input_path.name.replace(".urdf.xacro", "").replace(".xacro", "").replace(".urdf", "")

    # Compile Xacro if necessary
    if input_path.name.endswith(".xacro"):
        urdf_path = output_dir / f"{base_name}_compiled.urdf"
        print(f"[+] Compiling Xacro macro: {input_path} -> {urdf_path}")
        subprocess.run(["xacro", str(input_path), "-o", str(urdf_path)], check=True)
    else:
        urdf_path = input_path

    # Parse URDF XML
    tree = ET.parse(str(urdf_path))
    root = tree.getroot()

    links = []
    for link_elem in root.findall("link"):
        link_name = link_elem.attrib.get("name")
        if link_name:
            links.append(link_name)

    joints = []
    child_links_set = set()
    for joint_elem in root.findall("joint"):
        joint_name = joint_elem.attrib.get("name")
        joint_type = joint_elem.attrib.get("type", "fixed")
        parent_elem = joint_elem.find("parent")
        child_elem = joint_elem.find("child")

        if joint_name and parent_elem is not None and child_elem is not None:
            parent_link = parent_elem.attrib.get("link")
            child_link = child_elem.attrib.get("link")
            if parent_link and child_link:
                joints.append({
                    "name": joint_name,
                    "type": joint_type,
                    "parent": parent_link,
                    "child": child_link
                })
                child_links_set.add(child_link)

    # Determine Root Link
    root_links = [l for l in links if l not in child_links_set]

    # Build DOT string
    dot_lines = [
        'digraph G {',
        '  rankdir=TB;',
        '  node [fontname="Helvetica", fontsize=10, shape=box, style="filled,rounded"];',
        '  edge [fontname="Helvetica", fontsize=9];',
        ''
    ]

    # Format Node declarations
    for link in links:
        if link in root_links:
            dot_lines.append(f'  "{link}" [fillcolor="#FEF3C7", color="#D97706", label="{link}"];')
        else:
            dot_lines.append(f'  "{link}" [fillcolor="#F8FAFC", color="#334155", label="{link}"];')

    dot_lines.append('')

    # Format Edge declarations
    for j in joints:
        parent = j["parent"]
        child = j["child"]
        jname = j["name"]
        jtype = j["type"]

        if jtype == "fixed":
            edge_attr = 'style="dashed", color="#475569"'
        elif jtype in ("revolute", "continuous"):
            edge_attr = 'color="#0284C7", style="bold"'
        else:
            edge_attr = 'color="#334155"'

        dot_lines.append(f'  "{parent}" -> "{child}" [label="{jname}\\n[{jtype}]", {edge_attr}];')

    dot_lines.append('}')
    dot_content = '\n'.join(dot_lines) + '\n'

    gv_path = output_dir / f"{base_name}_joint_graph.gv"
    png_path = output_dir / f"{base_name}_joint_graph.png"

    print(f"[+] Writing Graphviz DOT: {gv_path}")
    gv_path.write_text(dot_content, encoding="utf-8")

    print(f"[+] Rendering custom joint graph PNG: {png_path}")
    subprocess.run(["dot", "-Tpng", str(gv_path), "-o", str(png_path)], check=True)

    print(f"[✓] Joint graph rendering complete. Outputs generated in: {output_dir}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python render_joint_graph.py <path_to_xacro_or_urdf> [output_dir]")
        sys.exit(1)

    target_input = Path(sys.argv[1])
    target_output = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("output")
    render_joint_graph(target_input, target_output)
