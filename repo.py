import json
import os
from typing import List, Optional

from models import Student
from data_structures.stack import Stack
from data_structures.priority_queue import PriorityQueue

class StudentRepository:
    def __init__(self, file_path: str = "students.json"):
        self.file_path = file_path
        self.students: List[Student] = []
        self.deleted_stack = Stack()
        self.priority_queue = PriorityQueue()
        self.load()

    # ---------- Persistence (الحفظ والتحميل) ----------
    def load(self) -> None:
        if not os.path.exists(self.file_path):
            return
        
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.students = [Student.from_dict(d) for d in json.load(f)]
                self._rebuild_priority_queue()
        except Exception:
            self.students = []
            self.deleted_stack.clear()
            self.priority_queue.clear()

    def save(self) -> None:
        # اختصرنا هنا: الحفظ العادي هو نفسه التصدير بس للملف الأساسي
        self.export_to_file(self.file_path)

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
        # لو لقينا طالب بنفس الـ ID (يعني get_by_id مرجعتش None) يبقى فيه مشكلة
        if self.get_by_id(s.id):
            raise ValueError("Student with this ID already exists.")

        self.students.append(s)
        self.priority_queue.push(s.grade, s)

    def delete(self, student_id: str) -> None:
        student = self.get_by_id(student_id)
        if student:
            self.deleted_stack.push(student)
            self.students.remove(student) # دالة remove أسهل من إعادة بناء القائمة
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

        # تحديث البيانات دفعة واحدة
        s.name, s.age, s.grade = name, age, grade
        self._rebuild_priority_queue()

    def get_all(self) -> List[Student]:
        return list(self.students)

    def get_by_id(self, student_id: str) -> Optional[Student]:
        # السطر السحري: هات أول واحد يقابلك بالـ ID ده، ولو مفيش رجع None
        return next((s for s in self.students if s.id == student_id), None)

    # ---------- Search & Sort ----------
    def search(self, query: str) -> Optional[Student]:
        q = query.lower()
        # هات أول طالب الـ ID أو الاسم بتاعه فيه كلمة البحث
        return next((s for s in self.students if q in s.id.lower() or q in s.name.lower()), None)

    def sort(self, mode: str) -> None:
        # خريطة الترتيب بدل دوشة الـ if والـ elif
        sort_map = {
            "name_asc":   (lambda s: s.name.lower(), False),
            "name_desc":  (lambda s: s.name.lower(), True),
            "age_asc":    (lambda s: s.age, False),
            "age_desc":   (lambda s: s.age, True),
            "grade_asc":  (lambda s: s.grade, False),
            "grade_desc": (lambda s: s.grade, True),
        }
        
        if mode in sort_map:
            key_func, reverse_val = sort_map[mode]
            self.students.sort(key=key_func, reverse=reverse_val)

    # ---------- Priority Queue ----------
    def get_top_student(self) -> Optional[Student]:
        return self.priority_queue.peek()