"""
heap.py — Custom MinHeap and MaxHeap implementations.

MinHeap: used by Dijkstra's algorithm; stores (distance, node) tuples.
MaxHeap: used as the Priority Dispatch Queue; stores Package objects
         ordered by priority (highest first).
"""


class Package:
    """Represents a delivery package in the dispatch queue."""

    def __init__(self, package_id: str, priority: int, destination: str, weight_kg: float):
        self.package_id = package_id
        self.priority = priority        
        self.destination = destination
        self.weight_kg = weight_kg

    def __repr__(self):
        return (
            f"Package(id={self.package_id}, priority={self.priority}, "
            f"dest={self.destination}, weight={self.weight_kg}kg)"
        )




class MinHeap:
    """
    Binary min-heap storing (key, value) tuples.
    The heap property is maintained on *key* (the first element).
    Typical use: (distance, node_name).
    """

    def __init__(self):
        self._data: list = []

  

    def push(self, item: tuple) -> None:
        """Insert an item and restore heap order."""
        self._data.append(item)
        self._sift_up(len(self._data) - 1)

    def pop(self) -> tuple:
        """Remove and return the item with the smallest key."""
        if self.is_empty():
            raise IndexError("pop from empty MinHeap")
        self._swap(0, len(self._data) - 1)
        minimum = self._data.pop()
        if self._data:
            self._sift_down(0)
        return minimum

    def peek(self) -> tuple:
        """Return the item with the smallest key without removing it."""
        if self.is_empty():
            raise IndexError("peek at empty MinHeap")
        return self._data[0]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def __len__(self) -> int:
        return len(self._data)

  
    def _sift_up(self, idx: int) -> None:
        while idx > 0:
            parent = (idx - 1) // 2
            if self._data[idx][0] < self._data[parent][0]:
                self._swap(idx, parent)
                idx = parent
            else:
                break

    def _sift_down(self, idx: int) -> None:
        n = len(self._data)
        while True:
            smallest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2

            if left < n and self._data[left][0] < self._data[smallest][0]:
                smallest = left
            if right < n and self._data[right][0] < self._data[smallest][0]:
                smallest = right

            if smallest != idx:
                self._swap(idx, smallest)
                idx = smallest
            else:
                break

    def _swap(self, i: int, j: int) -> None:
        self._data[i], self._data[j] = self._data[j], self._data[i]




class MaxHeap:
    """
    Binary max-heap storing Package objects ordered by priority (descending).
    Provides enqueue / dequeue / peek / is_empty.
    """

    def __init__(self):
        self._data: list[Package] = []

    
    def enqueue(self, package: Package) -> None:
        """Add a package and restore heap order."""
        self._data.append(package)
        self._sift_up(len(self._data) - 1)

    def dequeue(self) -> Package:
        """Remove and return the highest-priority package."""
        if self.is_empty():
            raise IndexError("dequeue from empty MaxHeap")
        self._swap(0, len(self._data) - 1)
        top = self._data.pop()
        if self._data:
            self._sift_down(0)
        return top

    def peek(self) -> Package:
        """Return the highest-priority package without removing it."""
        if self.is_empty():
            raise IndexError("peek at empty MaxHeap")
        return self._data[0]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def __len__(self) -> int:
        return len(self._data)

  

    def _sift_up(self, idx: int) -> None:
        while idx > 0:
            parent = (idx - 1) // 2
            if self._data[idx].priority > self._data[parent].priority:
                self._swap(idx, parent)
                idx = parent
            else:
                break

    def _sift_down(self, idx: int) -> None:
        n = len(self._data)
        while True:
            largest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2

            if left < n and self._data[left].priority > self._data[largest].priority:
                largest = left
            if right < n and self._data[right].priority > self._data[largest].priority:
                largest = right

            if largest != idx:
                self._swap(idx, largest)
                idx = largest
            else:
                break

    def _swap(self, i: int, j: int) -> None:
        self._data[i], self._data[j] = self._data[j], self._data[i]
