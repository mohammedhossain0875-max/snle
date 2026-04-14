"""
graph.py — Weighted directed graph with adjacency-list representation.

Features
--------
* build_from_edges  — populate the graph from (src, dst, weight) tuples
* dijkstra          — single-source shortest paths via custom MinHeap
* detect_cycles     — DFS with WHITE / GRAY / BLACK node colouring
* display_summary   — human-readable dump of nodes and edges
"""

from heap import MinHeap



WHITE = 0  
GRAY  = 1   
BLACK = 2   


class Graph:
    """Weighted directed graph using an adjacency list (dict of lists)."""

    def __init__(self):
        self._adj: dict[str, list[tuple[str, int]]] = {}

  

    def add_node(self, name: str) -> None:
        """Ensure *name* exists in the adjacency list (no duplicate edges)."""
        if name not in self._adj:
            self._adj[name] = []

    def add_edge(self, src: str, dst: str, weight: int) -> None:
        """Add a directed edge src → dst with the given weight."""
        self.add_node(src)
        self.add_node(dst)
        self._adj[src].append((dst, weight))

    def build_from_edges(self, nodes: list[str], edges: list[tuple]) -> None:
        """
        Populate the graph from pre-parsed data.

        nodes : list of node name strings (guarantees isolated nodes appear)
        edges : list of (src, dst, weight) tuples
        """
        for n in nodes:
            self.add_node(n)
        for src, dst, weight in edges:
            self.add_edge(src, dst, weight)


    def nodes(self) -> list[str]:
        return list(self._adj.keys())

    def neighbours(self, node: str) -> list[tuple[str, int]]:
        return self._adj.get(node, [])

   
    def dijkstra(self, source: str) -> tuple[dict, dict]:
        """
        Compute shortest distances from *source* to every reachable node.

        Returns
        -------
        dist : dict mapping node → shortest distance (inf if unreachable)
        prev : dict mapping node → predecessor on shortest path
        """
        if source not in self._adj:
            raise ValueError(f"Node '{source}' not in graph.")

        INF = float("inf")
        dist: dict[str, float] = {n: INF for n in self._adj}
        prev: dict[str, str | None] = {n: None for n in self._adj}
        dist[source] = 0

        heap = MinHeap()
        heap.push((0, source))

        visited: set[str] = set()

        while not heap.is_empty():
            d, u = heap.pop()

            if u in visited:
                continue
            visited.add(u)

            for v, w in self._adj[u]:
                if v in visited:
                    continue
                new_dist = d + w
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    prev[v] = u
                    heap.push((new_dist, v))

        return dist, prev

    def shortest_path(self, source: str, target: str) -> tuple[list[str], float]:
        """
        Return (path, total_distance) for the shortest route from
        *source* to *target*.  path is [] and distance is inf if
        unreachable.
        """
        dist, prev = self.dijkstra(source)

        if dist[target] == float("inf"):
            return [], float("inf")

      
        path: list[str] = []
        node: str | None = target
        while node is not None:
            path.append(node)
            node = prev[node]
        path.reverse()
        return path, dist[target]


    def detect_cycles(self) -> tuple[bool, list[str]]:
        """
        Detect whether the graph contains any directed cycle.

        Returns
        -------
        (has_cycle, cycle_path)

        has_cycle  : True if at least one cycle was found
        cycle_path : list of nodes forming one cycle (empty if none)
        """
        colour: dict[str, int] = {n: WHITE for n in self._adj}
        parent: dict[str, str | None] = {n: None for n in self._adj}
        cycle_info: list = []  

        def dfs(u: str) -> bool:
            colour[u] = GRAY
            for v, _ in self._adj[u]:
                if colour[v] == GRAY:
                   
                    cycle: list[str] = [v, u]
                    node = u
                    while parent[node] != v and parent[node] is not None:
                        node = parent[node]
                        cycle.append(node)
                    cycle.append(v)
                    cycle.reverse()
                    cycle_info.append(cycle)
                    return True
                if colour[v] == WHITE:
                    parent[v] = u
                    if dfs(v):
                        return True
            colour[u] = BLACK
            return False

        for node in self._adj:
            if colour[node] == WHITE:
                if dfs(node):
                    return True, cycle_info[0]

        return False, []

   

    def display_summary(self) -> None:
        """Print a formatted summary of nodes and adjacency list."""
        print(f"\n  Nodes ({len(self._adj)}):")
        for node in self._adj:
            print(f"    - {node}")

        total_edges = sum(len(v) for v in self._adj.values())
        print(f"\n  Edges ({total_edges}):")
        for src, neighbours in self._adj.items():
            for dst, w in neighbours:
                print(f"    {src} -> {dst}  (weight: {w})")
