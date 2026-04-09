# Smart Network Logistics Engine (SNLE)
**COMP 251 – Data Structures & Algorithms | Capstone Project**

A command-line Python application that models a city courier delivery network
as a weighted directed graph.  Every data structure used is implemented from
scratch — no external libraries are required.

---

## Project Structure

```
snle/
├── src/
│   ├── main.py       # CLI entry point & menu
│   ├── graph.py      # Weighted directed graph, Dijkstra, cycle detection
│   ├── heap.py       # MinHeap (Dijkstra) + MaxHeap (priority dispatch)
│   ├── hashmap.py    # Open-addressing hash map (linear probing)
│   ├── trie.py       # Trie for depot autocomplete
│   └── utils.py      # Network file parser
├── data/
│   └── network.txt   # Input: nodes, edges, packages
├── README.md
└── requirements.txt
```

---

## How to Run

```bash
cd snle
python src/main.py
```

Python 3.10 or later is recommended (uses `list[str]` type hints).

---

## Data File Format (`data/network.txt`)

```
NODES
DepotA DepotB DepotC WarehouseX ZoneNorth ZoneSouth

EDGES
DepotA DepotB 4
DepotA WarehouseX 2
...

PACKAGES
PKG001 8 ZoneNorth 2.5
...
```

- **NODES** — space-separated depot/zone names  
- **EDGES** — `<src> <dst> <weight>` (directed, integer weight)  
- **PACKAGES** — `<id> <priority 1-10> <destination> <weight_kg>`

---

## Features & Algorithms

| Menu | Feature | Algorithm / DS |
|------|---------|----------------|
| 1 | Display Network Summary | Adjacency list traversal |
| 2 | Find Shortest Path | Dijkstra's algorithm (custom MinHeap) |
| 3 | Detect Cycles | DFS — WHITE / GRAY / BLACK node colouring |
| 4 | Dispatch Highest-Priority Package | Custom MaxHeap (priority queue) |
| 5 | Search Depot by Name | Custom HashMap (open addressing, load-factor resize) |
| 6 | Autocomplete Depot Name | Trie prefix search |

### Graph (`graph.py`)
Adjacency list stored as `dict[str, list[(neighbour, weight)]]`.

### Dijkstra's Algorithm (`graph.py` + `heap.py`)
Uses a custom **MinHeap** that stores `(distance, node)` tuples.
Lazy-deletion handles stale entries — nodes are skipped once fully settled.

### Cycle Detection (`graph.py`)
Iterative DFS with three colours:
- **WHITE** — not yet visited  
- **GRAY** — currently on the DFS stack (active path)  
- **BLACK** — fully explored  

A back edge (WHITE → GRAY) proves a directed cycle exists.

### Priority Dispatch Queue (`heap.py`)
**MaxHeap** of `Package` objects ordered by `priority` (1–10).
Provides `enqueue`, `dequeue`, `peek`, `is_empty`.

### Custom Hash Map (`hashmap.py`)
Open addressing with **linear probing**.
- Polynomial rolling hash  
- Lazy deletion via a `_DELETED` sentinel  
- Automatic resize (capacity × 2) when load factor > 0.7

### Trie (`trie.py`)
Character-level trie supporting exact `search`, `starts_with`, and
`autocomplete` (returns all words sharing a given prefix).

---

## No External Dependencies

`requirements.txt` is included for completeness but lists no packages.
The project runs on the Python standard library alone.
