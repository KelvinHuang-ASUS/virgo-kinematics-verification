#!/usr/bin/env python3
"""
Interactive 3D URDF Coordinate Frame Inspector

Parses a URDF or Xacro kinematic model, calculates forward kinematics for all links
in zero configuration, and renders an interactive 3D Plotly view displaying:
  - Persistent link origin text labels
  - RGB 3D coordinate frames for every link (Red=X, Green=Y, Blue=Z)
  - Inter-frame kinematic joint linkages
  - Optical camera pointing direction vectors

Output: Standalone HTML page with embedded interactive Plotly inspection tool.
"""

import argparse
import math
import os
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import plotly.graph_objects as go


def rpy_to_rotation_matrix(roll: float, pitch: float, yaw: float) -> np.ndarray:
    """
    Convert roll, pitch, yaw angles (radians) to a 3x3 rotation matrix.
    Follows standard ROS/URDF extrinsic fixed-axis convention:
    R = Rz(yaw) * Ry(pitch) * Rx(roll)
    """
    cr, sr = np.cos(roll), np.sin(roll)
    cp, sp = np.cos(pitch), np.sin(pitch)
    cy, sy = np.cos(yaw), np.sin(yaw)

    rx = np.array([[1.0, 0.0, 0.0],
                   [0.0, cr, -sr],
                   [0.0, sr, cr]])

    ry = np.array([[cp, 0.0, sp],
                   [0.0, 1.0, 0.0],
                   [-sp, 0.0, cp]])

    rz = np.array([[cy, -sy, 0.0],
                   [sy, cy, 0.0],
                   [0.0, 0.0, 1.0]])

    return rz @ ry @ rx


def parse_urdf_tree(urdf_path: Path):
    """
    Parses URDF XML structure to extract link names and joint transformations.
    Returns:
        links: list of link names
        joints: list of dict containing joint properties (name, type, parent, child, xyz, rpy)
    """
    tree = ET.parse(str(urdf_path))
    root = tree.getroot()

    links = []
    for link_elem in root.findall("link"):
        link_name = link_elem.attrib.get("name")
        if link_name:
            links.append(link_name)

    joints = []
    for joint_elem in root.findall("joint"):
        j_name = joint_elem.attrib.get("name")
        j_type = joint_elem.attrib.get("type", "fixed")
        parent_elem = joint_elem.find("parent")
        child_elem = joint_elem.find("child")

        if j_name and parent_elem is not None and child_elem is not None:
            parent_link = parent_elem.attrib.get("link")
            child_link = child_elem.attrib.get("link")
            
            origin_elem = joint_elem.find("origin")
            xyz = [0.0, 0.0, 0.0]
            rpy = [0.0, 0.0, 0.0]

            if origin_elem is not None:
                if "xyz" in origin_elem.attrib:
                    xyz = [float(v) for v in origin_elem.attrib["xyz"].split()]
                if "rpy" in origin_elem.attrib:
                    rpy = [float(v) for v in origin_elem.attrib["rpy"].split()]

            joints.append({
                "name": j_name,
                "type": j_type,
                "parent": parent_link,
                "child": child_link,
                "xyz": xyz,
                "rpy": rpy
            })

    return links, joints


def compute_forward_kinematics(links: list, joints: list):
    """
    Computes world-frame origin position and rotation matrix for all links.
    """
    child_to_joint = {j["child"]: j for j in joints}
    child_links = set(child_to_joint.keys())
    root_links = [l for l in links if l not in child_links]

    link_poses = {}

    # Initialize root links at world origin
    for root_link in root_links:
        link_poses[root_link] = {
            "pos": np.array([0.0, 0.0, 0.0]),
            "rot": np.eye(3),
            "parent_joint": None,
            "rpy_rel": [0.0, 0.0, 0.0],
            "xyz_rel": [0.0, 0.0, 0.0]
        }

    # BFS / DFS traversal down the kinematic tree
    queue = list(root_links)
    visited = set(root_links)

    while queue:
        curr_link = queue.pop(0)
        curr_pos = link_poses[curr_link]["pos"]
        curr_rot = link_poses[curr_link]["rot"]

        # Find outgoing joints where current link is parent
        outgoing_joints = [j for j in joints if j["parent"] == curr_link]
        for j in outgoing_joints:
            child = j["child"]
            if child in visited:
                continue

            rel_xyz = np.array(j["xyz"])
            rel_rot = rpy_to_rotation_matrix(*j["rpy"])

            world_pos = curr_pos + curr_rot @ rel_xyz
            world_rot = curr_rot @ rel_rot

            link_poses[child] = {
                "pos": world_pos,
                "rot": world_rot,
                "parent_joint": j["name"],
                "rpy_rel": j["rpy"],
                "xyz_rel": j["xyz"]
            }
            visited.add(child)
            queue.append(child)

    return link_poses, child_to_joint


def build_3d_interactive_figure(links: list, joints: list, link_poses: dict, axis_length: float = 0.025) -> go.Figure:
    """
    Constructs an interactive 3D Plotly visualization of URDF coordinate frames.
    Styled in Clean White Presentation Theme.
    """
    fig = go.Figure()

    # Define virtual algorithm optical frames to filter out from 3D visualization (rendered in Graphviz topology DOT)
    exclude_links = {"cam_narrow_cv_frame", "cam_tele_cv_frame", "cam_wide_cv_frame"}

    # 1. Add kinematic structure joint lines (parent origin -> child origin)
    joint_lines_x, joint_lines_y, joint_lines_z = [], [], []
    for j in joints:
        if j["child"] in exclude_links or j["parent"] in exclude_links:
            continue
        parent_pos = link_poses[j["parent"]]["pos"]
        child_pos = link_poses[j["child"]]["pos"]
        joint_lines_x.extend([parent_pos[0], child_pos[0], None])
        joint_lines_y.extend([parent_pos[1], child_pos[1], None])
        joint_lines_z.extend([parent_pos[2], child_pos[2], None])

    fig.add_trace(go.Scatter3d(
        x=joint_lines_x,
        y=joint_lines_y,
        z=joint_lines_z,
        mode="lines",
        name="Kinematic Joint Linkage",
        line=dict(color="#64748B", width=3, dash="solid"),
        hoverinfo="none",
        showlegend=True
    ))

    # 2. Prepare coordinate axes vectors for each link (excluding intermediate camera body links)
    # Track legend additions to prevent duplicate entries
    legend_added = {"X": False, "Y": False, "Z": False}

    for link_name in links:
        if link_name in exclude_links or link_name not in link_poses:
            continue

        pos = link_poses[link_name]["pos"]
        rot = link_poses[link_name]["rot"]

        x_axis_end = pos + axis_length * rot[:, 0]
        y_axis_end = pos + axis_length * rot[:, 1]
        z_axis_end = pos + axis_length * rot[:, 2]

        # X-Axis (Red)
        fig.add_trace(go.Scatter3d(
            x=[pos[0], x_axis_end[0]],
            y=[pos[1], x_axis_end[1]],
            z=[pos[2], x_axis_end[2]],
            mode="lines",
            name="X Axis (Red)",
            legendgroup="X_Axis",
            showlegend=not legend_added["X"],
            line=dict(color="#EF4444", width=6),
            hoverinfo="text",
            hovertext=f"<b>{link_name}</b><br>X Axis (Red)<br>Start: ({pos[0]:.4f}, {pos[1]:.4f}, {pos[2]:.4f})<br>End: ({x_axis_end[0]:.4f}, {x_axis_end[1]:.4f}, {x_axis_end[2]:.4f})"
        ))
        legend_added["X"] = True

        # Y-Axis (Green)
        fig.add_trace(go.Scatter3d(
            x=[pos[0], y_axis_end[0]],
            y=[pos[1], y_axis_end[1]],
            z=[pos[2], y_axis_end[2]],
            mode="lines",
            name="Y Axis (Green)",
            legendgroup="Y_Axis",
            showlegend=not legend_added["Y"],
            line=dict(color="#10B981", width=6),
            hoverinfo="text",
            hovertext=f"<b>{link_name}</b><br>Y Axis (Green)<br>Start: ({pos[0]:.4f}, {pos[1]:.4f}, {pos[2]:.4f})<br>End: ({y_axis_end[0]:.4f}, {y_axis_end[1]:.4f}, {y_axis_end[2]:.4f})"
        ))
        legend_added["Y"] = True

        # Z-Axis (Blue)
        fig.add_trace(go.Scatter3d(
            x=[pos[0], z_axis_end[0]],
            y=[pos[1], z_axis_end[1]],
            z=[pos[2], z_axis_end[2]],
            mode="lines",
            name="Z Axis (Blue)",
            legendgroup="Z_Axis",
            showlegend=not legend_added["Z"],
            line=dict(color="#3B82F6", width=6),
            hoverinfo="text",
            hovertext=f"<b>{link_name}</b><br>Z Axis (Blue)<br>Start: ({pos[0]:.4f}, {pos[1]:.4f}, {pos[2]:.4f})<br>End: ({z_axis_end[0]:.4f}, {z_axis_end[1]:.4f}, {z_axis_end[2]:.4f})"
        ))
        legend_added["Z"] = True

    # 3. Add link origin markers with persistent labels including world (X, Y, Z) coordinates
    origin_x, origin_y, origin_z = [], [], []
    origin_labels = []
    hover_texts = []

    for link_name in links:
        if link_name in exclude_links or link_name not in link_poses:
            continue
        p_info = link_poses[link_name]
        pos = p_info["pos"]
        origin_x.append(pos[0])
        origin_y.append(pos[1])
        origin_z.append(pos[2])
        origin_labels.append(f"<b>{link_name}</b><br>({pos[0]:.4f}, {pos[1]:.4f}, {pos[2]:.4f})")

        j_info = f"Parent Joint: {p_info['parent_joint']}" if p_info['parent_joint'] else "Root Base Link"
        rpy_deg = [math.degrees(val) for val in p_info["rpy_rel"]]
        htext = (
            f"<b>Link: {link_name}</b><br>"
            f"{j_info}<br>"
            f"World Position (x,y,z): ({pos[0]:.4f}, {pos[1]:.4f}, {pos[2]:.4f}) m<br>"
            f"Relative Translation: ({p_info['xyz_rel'][0]:.4f}, {p_info['xyz_rel'][1]:.4f}, {p_info['xyz_rel'][2]:.4f}) m<br>"
            f"Relative RPY: ({p_info['rpy_rel'][0]:.4f}, {p_info['rpy_rel'][1]:.4f}, {p_info['rpy_rel'][2]:.4f}) rad "
            f"({rpy_deg[0]:.1f}°, {rpy_deg[1]:.1f}°, {rpy_deg[2]:.1f}°)"
        )
        hover_texts.append(htext)

    fig.add_trace(go.Scatter3d(
        x=origin_x,
        y=origin_y,
        z=origin_z,
        mode="markers+text",
        name="Link Origins & Labels",
        marker=dict(size=7, color="#D97706", symbol="circle", opacity=0.95),
        text=origin_labels,
        textposition="top center",
        textfont=dict(size=10, color="#0F172A", family="Inter, sans-serif"),
        hoverinfo="text",
        hovertext=hover_texts,
        showlegend=True
    ))

    # 4. Configure professional Clean White Presentation layout and 3D scene controls
    fig.update_layout(
        title=dict(
            text="VIRGO Gimbal Kinematic Chain — Interactive 3D Frame Inspector<br>"
                 "<sup>RGB Axes Definition: Red = X, Green = Y, Blue = Z | CAD Model Alignment ER_260820</sup>",
            font=dict(size=18, color="#0F172A", family="Inter, sans-serif"),
            x=0.02,
            y=0.96
        ),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        template="plotly_white",
        scene=dict(
            xaxis=dict(
                title=dict(text="X (meters)", font=dict(color="#334155")),
                tickfont=dict(color="#334155"),
                backgroundcolor="#F8FAFC",
                gridcolor="#E2E8F0",
                showbackground=True,
                zerolinecolor="#94A3B8"
            ),
            yaxis=dict(
                title=dict(text="Y (meters)", font=dict(color="#334155")),
                tickfont=dict(color="#334155"),
                backgroundcolor="#F8FAFC",
                gridcolor="#E2E8F0",
                showbackground=True,
                zerolinecolor="#94A3B8"
            ),
            zaxis=dict(
                title=dict(text="Z (meters)", font=dict(color="#334155")),
                tickfont=dict(color="#334155"),
                backgroundcolor="#F8FAFC",
                gridcolor="#E2E8F0",
                showbackground=True,
                zerolinecolor="#94A3B8"
            ),
            aspectmode="data",  # 1:1:1 physical aspect ratio
            camera=dict(
                eye=dict(x=-1.8, y=-1.8, z=1.0),
                up=dict(x=0, y=0, z=1)
            )
        ),
        legend=dict(
            font=dict(color="#334155", size=12),
            bgcolor="rgba(255, 255, 255, 0.9)",
            bordercolor="#CBD5E1",
            borderwidth=1,
            x=0.01,
            y=0.85
        ),
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                active=0,
                x=0.98,
                y=0.98,
                xanchor="right",
                yanchor="top",
                bgcolor="#F8FAFC",
                bordercolor="#CBD5E1",
                borderwidth=1,
                font=dict(color="#0F172A", size=12, family="Inter, sans-serif"),
                buttons=[
                    dict(
                        label="Mechanical View (Z Up)",
                        method="relayout",
                        args=[{
                            "scene.camera": dict(
                                eye=dict(x=-1.8, y=-1.8, z=1.0),
                                up=dict(x=0, y=0, z=1)
                            )
                        }]
                    ),
                    dict(
                        label="Robotics View (Z Down)",
                        method="relayout",
                        args=[{
                            "scene.camera": dict(
                                eye=dict(x=-1.8, y=1.8, z=-1.0),
                                up=dict(x=0, y=0, z=-1)
                            )
                        }]
                    )
                ]
            )
        ],
        margin=dict(l=20, r=20, b=20, t=80)
    )

    return fig


def render_3d_interactive(input_path: Path, output_target: Path):
    if not input_path.exists():
        print(f"[-] Error: Input path '{input_path}' does not exist.")
        sys.exit(1)

    # Output directory and filename resolution
    if input_path.suffix == ".xacro":
        temp_urdf = output_target / f"{input_path.stem.replace('.urdf', '')}_compiled.urdf" if output_target.is_dir() else input_path.with_suffix(".urdf")
        print(f"[+] Compiling Xacro to temporary URDF: {input_path} -> {temp_urdf}")
        subprocess.run(["xacro", str(input_path), "-o", str(temp_urdf)], check=True)
        urdf_file = temp_urdf
    else:
        urdf_file = input_path

    base_name = input_path.name.replace(".urdf.xacro", "").replace(".xacro", "").replace(".urdf", "").replace("_compiled", "")

    if output_target.suffix == ".html":
        output_html = output_target
        output_html.parent.mkdir(parents=True, exist_ok=True)
    else:
        output_target.mkdir(parents=True, exist_ok=True)
        output_html = output_target / f"{base_name}_interactive_3d.html"

    print(f"[+] Parsing URDF model: {urdf_file}")
    links, joints = parse_urdf_tree(urdf_file)

    print(f"[+] Computing zero-configuration forward kinematics for {len(links)} links and {len(joints)} joints...")
    link_poses, _ = compute_forward_kinematics(links, joints)

    print("[+] Building 3D Plotly coordinate frame visualization...")
    fig = build_3d_interactive_figure(links, joints, link_poses)

    print(f"[+] Exporting interactive HTML inspector: {output_html}")
    fig.write_html(str(output_html), include_plotlyjs="cdn", full_html=True)

    print(f"[✓] 3D coordinate frame rendering complete. File saved to: {output_html}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render interactive 3D Plotly coordinate frame inspector from URDF/Xacro.")
    parser.add_argument("input_path", type=Path, help="Path to input .urdf or .xacro file")
    parser.add_argument("output_path", type=Path, nargs="?", default=Path("output/03_cad_coordinate_alignment"),
                        help="Output HTML file path or output directory")

    args = parser.parse_args()
    render_3d_interactive(args.input_path, args.output_path)
