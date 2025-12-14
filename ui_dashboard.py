import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from repo import StudentRepository
from models import Student


class StudentForm(ctk.CTkToplevel):
    def __init__(self, master, repo: StudentRepository, student: Student | None = None):
        super().__init__(master)
        self.repo = repo
        self.student = student
        self.result = None

        self.title("Student Form")
        self.geometry("360x300")
        self.resizable(False, False)

        frame = ctk.CTkFrame(self, corner_radius=15)
        frame.pack(expand=True, fill="both", padx=15, pady=15)

        title_text = "Add Student" if student is None else "Edit Student"
        ctk.CTkLabel(
            frame,
            text=title_text,
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(10, 15))

        self.id_entry = ctk.CTkEntry(frame, placeholder_text="Student ID")
        self.id_entry.pack(pady=5, padx=20, fill="x")

        self.name_entry = ctk.CTkEntry(frame, placeholder_text="Name")
        self.name_entry.pack(pady=5, padx=20, fill="x")

        self.age_entry = ctk.CTkEntry(frame, placeholder_text="Age")
        self.age_entry.pack(pady=5, padx=20, fill="x")

        self.grade_entry = ctk.CTkEntry(frame, placeholder_text="Grade")
        self.grade_entry.pack(pady=5, padx=20, fill="x")

        ctk.CTkButton(frame, text="Save", command=self._save).pack(pady=(15, 10))

        # ✅ PRE-FILL DATA WHEN EDITING
        if self.student is not None:
            self.id_entry.insert(0, self.student.id)
            self.id_entry.configure(state="disabled")
            self.name_entry.insert(0, self.student.name)
            self.age_entry.insert(0, str(self.student.age))
            self.grade_entry.insert(0, str(self.student.grade))

    def _save(self):
        sid = self.id_entry.get().strip()
        name = self.name_entry.get().strip()
        age_text = self.age_entry.get().strip()
        grade_text = self.grade_entry.get().strip()

        if not sid or not name or not age_text or not grade_text:
            messagebox.showwarning("Validation", "Please fill all fields.")
            return

        try:
            age = int(age_text)
            grade = int(grade_text)
        except ValueError:
            messagebox.showwarning("Validation", "Age and Grade must be integers.")
            return

        self.result = (sid, name, age, grade)
        self.destroy()


class SortDialog(ctk.CTkToplevel):
    def __init__(self, master, callback):
        super().__init__(master)
        self.callback = callback
        self.title("Sort Options")
        self.geometry("280x260")
        self.resizable(False, False)

        frame = ctk.CTkFrame(self, corner_radius=15)
        frame.pack(expand=True, fill="both", padx=15, pady=15)

        ctk.CTkLabel(
            frame,
            text="Choose sort mode",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(10, 15))

        def add_button(text, mode):
            ctk.CTkButton(
                frame,
                text=text,
                command=lambda m=mode: self._select(m)
            ).pack(pady=5, padx=20, fill="x")

        add_button("Name A → Z", "name_asc")
        add_button("Name Z → A", "name_desc")
        add_button("Age Low → High", "age_asc")
        add_button("Age High → Low", "age_desc")
        add_button("Grade Low → High", "grade_asc")
        add_button("Grade High → Low", "grade_desc")

    def _select(self, mode: str):
        self.callback(mode)
        self.destroy()


class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Student Management Dashboard")
        self.geometry("980x560")
        self.minsize(900, 520)

        self.repo = StudentRepository()

        # ---- Dark TreeView ----
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background="#1b1b1b",
            foreground="white",
            rowheight=30,
            fieldbackground="#1b1b1b",
            borderwidth=0
        )
        style.map(
            "Treeview",
            background=[("selected", "#0e639c")],
            foreground=[("selected", "white")]
        )

        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True)

        left = ctk.CTkFrame(main_frame)
        left.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)

        right = ctk.CTkFrame(main_frame, corner_radius=15)
        right.pack(side="right", fill="y", padx=(5, 10), pady=10)

        ctk.CTkLabel(
            left,
            text="Student Management System",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=10)

        table_frame = ctk.CTkFrame(left)
        table_frame.pack(fill="both", expand=True, padx=10)

        columns = ("id", "name", "age", "grade")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col.upper())

        self.tree.pack(fill="both", expand=True)

        # ---- Controls ----
        ctk.CTkLabel(
            right,
            text="Controls",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=10)

        ctk.CTkButton(right, text="Add Student",
                      command=self.add_student).pack(pady=5, padx=15, fill="x")

        ctk.CTkButton(right, text="Edit Student",
                      command=self.edit_student).pack(pady=5, padx=15, fill="x")

        ctk.CTkButton(
            right,
            text="Delete Student",
            fg_color="#d63031",
            hover_color="#b02426",
            command=self.delete_student
        ).pack(pady=5, padx=15, fill="x")

        # ✅ Stack button
        ctk.CTkButton(
            right,
            text="Undo Delete",
            fg_color="#0984e3",
            hover_color="#0770c2",
            command=self.undo_delete
        ).pack(pady=5, padx=15, fill="x")

        ctk.CTkButton(right, text="Sort...",
                      command=self.open_sort_dialog).pack(pady=5, padx=15, fill="x")

        ctk.CTkButton(
            right,
            text="Top Student",
            fg_color="#6c5ce7",
            hover_color="#5a4bdc",
            command=self.show_top_student
        ).pack(pady=5, padx=15, fill="x")

        ctk.CTkButton(right, text="Save",
                      command=self.save_data).pack(pady=5, padx=15, fill="x")

        ctk.CTkButton(right, text="Export JSON",
                      command=self.export_data).pack(pady=5, padx=15, fill="x")

        self.refresh_table()

    # -------- Actions --------
    def refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for s in self.repo.get_all():
            self.tree.insert("", "end", values=(s.id, s.name, s.age, s.grade))

    def add_student(self):
        d = StudentForm(self, self.repo)
        self.wait_window(d)
        if d.result:
            self.repo.add(Student(*d.result))
            self.refresh_table()

    def edit_student(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Edit", "Please select a student first.")
            return

        values = self.tree.item(sel[0], "values")
        sid = values[0]

        student = self.repo.get_by_id(sid)
        if not student:
            messagebox.showerror("Error", "Student not found.")
            return

        d = StudentForm(self, self.repo, student)
        self.wait_window(d)

        if d.result:
            _, name, age, grade = d.result
            self.repo.update(sid, name, age, grade)
            self.refresh_table()

    def delete_student(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Delete", "Please select a student first.")
            return

        sid = self.tree.item(sel[0], "values")[0]
        self.repo.delete(sid)

        self.tree.selection_remove(sel)
        self.refresh_table()

    def undo_delete(self):
        student = self.repo.undo_delete()
        if not student:
            messagebox.showinfo("Undo Delete", "Nothing to undo.")
            return
        self.refresh_table()
        messagebox.showinfo("Undo Delete", f"Restored: {student.name}")

    def open_sort_dialog(self):
        SortDialog(self, lambda m: (self.repo.sort(m), self.refresh_table()))

    def show_top_student(self):
        s = self.repo.get_top_student()
        if not s:
            messagebox.showinfo("Top Student", "No students available.")
            return
        messagebox.showinfo(
            "Top Student",
            f"ID: {s.id}\nName: {s.name}\nAge: {s.age}\nGrade: {s.grade}"
        )

    def save_data(self):
        self.repo.save()
        messagebox.showinfo("Saved", "Data saved.")

    def export_data(self):
        path = filedialog.asksaveasfilename(defaultextension=".json")
        if path:
            self.repo.export_to_file(path)
