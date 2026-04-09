"""
trie.py — Trie data structure for depot-name prefix search / autocomplete.

Supports: insert, search (exact), starts_with (prefix), autocomplete.
"""


class _TrieNode:
    __slots__ = ("children", "is_end")

    def __init__(self):
        self.children: dict[str, "_TrieNode"] = {}
        self.is_end: bool = False


class Trie:
    """
    Character-level trie over depot name strings.

    All lookups are case-sensitive to match the network file exactly.
    """

    def __init__(self):
        self._root = _TrieNode()

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def insert(self, word: str) -> None:
        """Insert *word* into the trie."""
        node = self._root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = _TrieNode()
            node = node.children[ch]
        node.is_end = True

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def search(self, word: str) -> bool:
        """Return True iff *word* was inserted exactly."""
        node = self._find_node(word)
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> bool:
        """Return True iff any inserted word begins with *prefix*."""
        return self._find_node(prefix) is not None

    def autocomplete(self, prefix: str) -> list[str]:
        """
        Return a sorted list of all inserted words that begin with *prefix*.
        Returns an empty list when no match exists.
        """
        node = self._find_node(prefix)
        if node is None:
            return []
        results: list[str] = []
        self._collect(node, list(prefix), results)
        return sorted(results)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _find_node(self, prefix: str):
        """Walk down the trie following *prefix*; return final node or None."""
        node = self._root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def _collect(self, node: _TrieNode, path: list, results: list) -> None:
        """DFS from *node*, appending complete words to *results*."""
        if node.is_end:
            results.append("".join(path))
        for ch, child in node.children.items():
            path.append(ch)
            self._collect(child, path, results)
            path.pop()
