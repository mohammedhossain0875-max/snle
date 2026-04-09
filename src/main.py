"""
main.py — Smart Network Logistics Engine (SNLE)
COMP 251 Capstone Project

Entry point: python src/main.py
"""

import os
import sys

# Allow sibling imports when running as  python src/main.py
sys.path.insert(0, os.path.dirname(__file__))

from graph import Graph
from heap import MaxHeap
from hashmap import HashMap
from trie import Trie
from utils import load_network


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_HERE = os.path.dirname(__file__)
_DATA_FILE = os.path.join(_HERE, "..", "data", "network.txt")


# ---------------------------------------------------------------------------
# Initialisation
# ---------------------------------------------------------------------------

def initialise(filepath: str):
    """Load the network file and build all data structures."""
    nodes, edges, packages = load_network(filepath)

    # --- Graph -----------------------------------------------------------
    graph = Graph()
    graph.build_from_edges(nodes, edges)

    # --- Priority Dispatch Queue (MaxHeap) --------------------------------
    dispatch_queue = MaxHeap()
    for pkg in packages:
        dispatch_queue.enqueue(pkg)

    # --- Depot HashMap ---------------------------------------------------
    depot_map = HashMap()
    for node in nodes:
        # Store the node's adjacency list size as a simple metadata value
        depot_map.insert(node, node)

    # --- Trie for autocomplete -------------------------------------------
    trie = Trie()
    for node in nodes:
        trie.insert(node)

    return graph, dispatch_queue, depot_map, trie, nodes


# ---------------------------------------------------------------------------
# Menu handlers
# ---------------------------------------------------------------------------

def show_network_summary(graph: Graph) -> None:
    print("\n--- Network Summary ---")
    graph.display_summary()


def find_shortest_path(graph: Graph) -> None:
    print("\n--- Find Shortest Path ---")
    nodes = graph.nodes()
    print("  Available nodes:", ", ".join(nodes))

    source = input("  Enter source node: ").strip()
    target = input("  Enter target node: ").strip()

    if source not in nodes:
        print(f"  [!] Node '{source}' not found in graph.")
        return
    if target not in nodes:
        print(f"  [!] Node '{target}' not found in graph.")
        return

    path, distance = graph.shortest_path(source, target)

    if not path:
        print(f"  No path exists from '{source}' to '{target}'.")
    else:
        print(f"  Shortest path : {' -> '.join(path)}")
        print(f"  Total distance: {distance}")


def detect_cycles(graph: Graph) -> None:
    print("\n--- Cycle Detection (DFS / WHITE-GRAY-BLACK) ---")
    has_cycle, cycle = graph.detect_cycles()
    if has_cycle:
        print("  [!] Cycle detected!")
        print(f"  Cycle path: {' -> '.join(cycle)}")
    else:
        print("  No cycles detected. The graph is a DAG.")


def dispatch_package(dispatch_queue: MaxHeap) -> None:
    print("\n--- Priority Dispatch ---")
    if dispatch_queue.is_empty():
        print("  Dispatch queue is empty. No packages to dispatch.")
        return

    print(f"  Packages remaining: {len(dispatch_queue)}")
    pkg = dispatch_queue.dequeue()
    print(f"  Dispatched: {pkg}")
    print(f"  Remaining in queue: {len(dispatch_queue)}")


def search_depot(depot_map: HashMap) -> None:
    print("\n--- Depot Search ---")
    name = input("  Enter depot name to search: ").strip()
    result = depot_map.search(name)
    if result is not None:
        print(f"  Found: '{name}' is registered in the network.")
    else:
        print(f"  '{name}' was not found in the depot registry.")


def autocomplete_depot(trie: Trie) -> None:
    print("\n--- Depot Autocomplete ---")
    prefix = input("  Enter prefix to autocomplete: ").strip()
    matches = trie.autocomplete(prefix)
    if matches:
        print(f"  Matches for '{prefix}':")
        for m in matches:
            print(f"    - {m}")
    else:
        print(f"  No depots found with prefix '{prefix}'.")


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

MENU = """\
===== Smart Network Logistics Engine =====
1. Display Network Summary
2. Find Shortest Path
3. Detect Cycles
4. Dispatch Highest-Priority Package
5. Search Depot by Name
6. Autocomplete Depot Name
7. Exit
=========================================="""


def main() -> None:
    print("Loading network data...", end=" ", flush=True)
    try:
        graph, dispatch_queue, depot_map, trie, nodes = initialise(_DATA_FILE)
    except FileNotFoundError as exc:
        print(f"\n[ERROR] {exc}")
        sys.exit(1)
    except ValueError as exc:
        print(f"\n[ERROR] Malformed data file — {exc}")
        sys.exit(1)
    print("done.\n")

    handlers = {
        "1": lambda: show_network_summary(graph),
        "2": lambda: find_shortest_path(graph),
        "3": lambda: detect_cycles(graph),
        "4": lambda: dispatch_package(dispatch_queue),
        "5": lambda: search_depot(depot_map),
        "6": lambda: autocomplete_depot(trie),
    }

    while True:
        print(MENU)
        choice = input("Select an option: ").strip()

        if choice == "7":
            print("Goodbye.")
            break

        handler = handlers.get(choice)
        if handler:
            handler()
        else:
            print("  Invalid choice. Please enter a number between 1 and 7.")

        input("\n  Press Enter to continue...")


if __name__ == "__main__":
    main()
