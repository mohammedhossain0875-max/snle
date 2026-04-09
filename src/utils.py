"""
utils.py — Network file parser.

Reads data/network.txt and returns structured data consumed by the rest
of the application.

File format
-----------
NODES
<space-separated node names>

EDGES
<src> <dst> <weight>
...

PACKAGES
<pkg_id> <priority> <destination> <weight_kg>
...
"""

import os
from heap import Package


def load_network(filepath: str) -> tuple[list[str], list[tuple], list[Package]]:
    """
    Parse *filepath* and return (nodes, edges, packages).

    nodes    : list of node name strings
    edges    : list of (src, dst, weight) tuples  (weight is int)
    packages : list of Package objects
    """
    nodes: list[str] = []
    edges: list[tuple] = []
    packages: list[Package] = []

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Network file not found: {filepath}")

    section = None
    with open(filepath, "r") as fh:
        for raw_line in fh:
            line = raw_line.strip()
            if not line:
                continue

            if line == "NODES":
                section = "NODES"
                continue
            if line == "EDGES":
                section = "EDGES"
                continue
            if line == "PACKAGES":
                section = "PACKAGES"
                continue

            if section == "NODES":
                nodes.extend(line.split())

            elif section == "EDGES":
                parts = line.split()
                if len(parts) != 3:
                    raise ValueError(f"Malformed edge line: {line!r}")
                src, dst, weight = parts[0], parts[1], int(parts[2])
                edges.append((src, dst, weight))

            elif section == "PACKAGES":
                parts = line.split()
                if len(parts) != 4:
                    raise ValueError(f"Malformed package line: {line!r}")
                pkg_id, priority, destination, weight_kg = (
                    parts[0], int(parts[1]), parts[2], float(parts[3])
                )
                packages.append(Package(pkg_id, priority, destination, weight_kg))

    return nodes, edges, packages
