import json
import os
from typing import List, Optional

from models import Student
from data_structures.stack import Stack
from data_structures.priority_queue import PriorityQueue


class StudentRepository:
    def __init__(self, file_path: str = "students.json"):
        self.file_path = file_path

        # Main Data Structure (Dynamic Array)
        self.students: List[Student] = []

        # Stack for Undo Delete (LIFO)
        self.deleted_stack = Stack()

        # Priority Queue for Top Student
        self.priority_queue = PriorityQueue()

        self.load()

    # ---------- Persistence ----------
    def load(self) -> None:
        if not os.path.exists(self.file_path):
            self.students = []
            self.deleted_stack.clear()
            self.priority_queue.clear()
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.students = [Student.from_dict(d) for d in data]
                self._rebuild_priority_queue()
        except Exception:
            self.students = []
            self.deleted_stack.clear()
            self.priority_queue.clear()

    def save(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in self.students], f, indent=2)

    def export_to_file(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in self.students], f, indent=2)

    # ---------- Internal Helpers ----------
    def _rebuild_priority_queue(self) -> None:
        self.priority_queue.clear()
        for s in self.students:
            self.priority_queue.push(s.grade, s)

    # ---------- CRUD Operations ----------
    def add(self, s: Student) -> None:
        if any(x.id == s.id for x in self.students):
            raise ValueError("Student with this ID already exists.")

        self.students.append(s)
        self.priority_queue.push(s.grade, s)

    def delete(self, student_id: str) -> None:
        student = self.get_by_id(student_id)
        if student:
            # push deleted student into Stack (Undo)
            self.deleted_stack.push(student)

        self.students = [x for x in self.students if x.id != student_id]
        self._rebuild_priority_queue()

    def undo_delete(self) -> Optional[Student]:
        student = self.deleted_stack.pop()
        if student:
            self.students.append(student)
            self._rebuild_priority_queue()
            return student
        return None

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

    # ---------- Search & Sort ----------
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
        return self.priority_queue.peek()
