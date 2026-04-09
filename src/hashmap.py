"""
hashmap.py — Custom hash map with open addressing (linear probing).

Supports: insert, search, delete.
Automatically resizes (doubles capacity) when load factor exceeds 0.7.
"""

_DELETED = object()   # sentinel for deleted slots


class HashMap:
    """
    Hash map using open addressing with linear probing.

    Keys must be hashable (strings are the primary use-case here).
    Values may be any object.
    """

    _INITIAL_CAPACITY = 16
    _LOAD_FACTOR_THRESHOLD = 0.7

    def __init__(self):
        self._capacity: int = self._INITIAL_CAPACITY
        self._size: int = 0                          # live entries
        self._buckets: list = [None] * self._capacity

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def insert(self, key: str, value) -> None:
        """Insert or update key→value. Resizes if load factor > 0.7."""
        if self._load_factor() > self._LOAD_FACTOR_THRESHOLD:
            self._resize()

        idx = self._probe(key)
        if self._buckets[idx] is None or self._buckets[idx] is _DELETED:
            self._size += 1
        self._buckets[idx] = (key, value)

    def search(self, key: str):
        """Return the value associated with *key*, or None if not found."""
        idx = self._find(key)
        if idx is None:
            return None
        return self._buckets[idx][1]

    def delete(self, key: str) -> bool:
        """
        Remove *key* from the map.
        Returns True on success, False if key was not present.
        """
        idx = self._find(key)
        if idx is None:
            return False
        self._buckets[idx] = _DELETED
        self._size -= 1
        return True

    def keys(self) -> list:
        """Return all live keys."""
        return [b[0] for b in self._buckets if b is not None and b is not _DELETED]

    def items(self) -> list:
        """Return all live (key, value) pairs."""
        return [b for b in self._buckets if b is not None and b is not _DELETED]

    def __len__(self) -> int:
        return self._size

    def __contains__(self, key: str) -> bool:
        return self._find(key) is not None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _hash(self, key: str) -> int:
        """Polynomial rolling hash mapped into current capacity."""
        h = 0
        for ch in key:
            h = (h * 31 + ord(ch)) % self._capacity
        return h

    def _probe(self, key: str) -> int:
        """
        Return the index where *key* should be written.
        Stops at the first empty slot, deleted slot, or existing slot with
        the same key (for updates).
        """
        idx = self._hash(key)
        first_deleted = None
        for _ in range(self._capacity):
            slot = self._buckets[idx]
            if slot is None:
                return first_deleted if first_deleted is not None else idx
            if slot is _DELETED:
                if first_deleted is None:
                    first_deleted = idx
            elif slot[0] == key:
                return idx
            idx = (idx + 1) % self._capacity
        return first_deleted  # map is full (shouldn't happen with resize)

    def _find(self, key: str):
        """
        Return the index of a live slot containing *key*, or None.
        """
        idx = self._hash(key)
        for _ in range(self._capacity):
            slot = self._buckets[idx]
            if slot is None:
                return None
            if slot is not _DELETED and slot[0] == key:
                return idx
            idx = (idx + 1) % self._capacity
        return None

    def _load_factor(self) -> float:
        return self._size / self._capacity

    def _resize(self) -> None:
        """Double capacity and rehash all live entries."""
        old_buckets = self._buckets
        self._capacity *= 2
        self._size = 0
        self._buckets = [None] * self._capacity
        for slot in old_buckets:
            if slot is not None and slot is not _DELETED:
                self.insert(slot[0], slot[1])
