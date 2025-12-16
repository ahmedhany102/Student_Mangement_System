import heapq

class PriorityQueue:
    def __init__(self):
        self.heap = []

    def push(self, priority, item):
        # negative priority → Max Heap
        heapq.heappush(self.heap, (-priority, item))

    def pop(self):
        if self.is_empty():
            return None
        return heapq.heappop(self.heap)[1]

    def peek(self):
        if self.is_empty():
            return None
        return self.heap[0][1]

    def is_empty(self):
        return len(self.heap) == 0

    def clear(self):
        self.heap.clear()
