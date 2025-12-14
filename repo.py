import json
import os
import heapq
from typing import List, Optional
from models import Student


class StudentRepository:
    def __init__(self, file_path: str = "students.json"):
        self.file_path = file_path

        # Main Data Structure (Dynamic Array)
        self.students: List[Student] = []

        # Priority Queue (Max-Heap by grade)
        self.priority_queue = []

        # Stack (Undo Delete)  <-- من المنهج
        self.deleted_stack: List[Student] = []

        self.load()  # auto-load on start

    # ---------- persistence ----------
    def load(self) -> None:
        if not os.path.exists(self.file_path):
            self.students = []
            self.priority_queue = []
            self.deleted_stack = []
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.students = [Student.from_dict(d) for d in data]
                self._rebuild_priority_queue()
        except Exception:
            self.students = []
            self.priority_queue = []
            self.deleted_stack = []

    def save(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in self.students], f, indent=2)

    def export_to_file(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in self.students], f, indent=2)

    # ---------- internal ----------
    def _rebuild_priority_queue(self) -> None:
        self.priority_queue = []
        for s in self.students:
            heapq.heappush(self.priority_queue, (-s.grade, s))

    # ---------- CRUD ----------
    def add(self, s: Student) -> None:
        if any(x.id == s.id for x in self.students):
            raise ValueError("Student with this ID already exists.")

        self.students.append(s)
        heapq.heappush(self.priority_queue, (-s.grade, s))

    def delete(self, student_id: str) -> None:
        student = self.get_by_id(student_id)
        if student:
            # PUSH into Stack
            self.deleted_stack.append(student)

        self.students = [x for x in self.students if x.id != student_id]
        self._rebuild_priority_queue()

    def undo_delete(self) -> Optional[Student]:
        if not self.deleted_stack:
            return None

        # POP from Stack
        student = self.deleted_stack.pop()
        self.students.append(student)
        self._rebuild_priority_queue()
        return student

    def update(self, student_id: str, name: str, age: int, grade: int) -> None:
        s = self.get_by_id(student_id)
        if not s:
            raise ValueError("Student not found.")

        s.name = name
        s.age = age
        s.grade = grade
        self._rebuild_priority_queue()

    def get_all(self) -> List[Student]:
        return list(self.students)

    def get_by_id(self, student_id: str) -> Optional[Student]:
        for s in self.students:
            if s.id == student_id:
                return s
        return None

    # ---------- search & sort ----------
    def search(self, query: str) -> Optional[Student]:
        q = query.lower()
        for s in self.students:
            if q in s.id.lower() or q in s.name.lower():
                return s
        return None

    def sort(self, mode: str) -> None:
        if mode == "name_asc":
            self.students.sort(key=lambda s: s.name.lower())
        elif mode == "name_desc":
            self.students.sort(key=lambda s: s.name.lower(), reverse=True)
        elif mode == "age_asc":
            self.students.sort(key=lambda s: s.age)
        elif mode == "age_desc":
            self.students.sort(key=lambda s: s.age, reverse=True)
        elif mode == "grade_asc":
            self.students.sort(key=lambda s: s.grade)
        elif mode == "grade_desc":
            self.students.sort(key=lambda s: s.grade, reverse=True)

    # ---------- Priority Queue ----------
    def get_top_student(self) -> Optional[Student]:
        if not self.priority_queue:
            return None
        return self.priority_queue[0][1]
