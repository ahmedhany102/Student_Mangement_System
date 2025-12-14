import customtkinter as ctk
from tkinter import messagebox


class LoginWindow(ctk.CTk):
    def __init__(self, on_success):
        super().__init__()
        self.on_success = on_success

        self.title("Admin Login")
        self.geometry("360x260")
        self.resizable(False, False)

        # main frame
        frame = ctk.CTkFrame(self, corner_radius=15)
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        title = ctk.CTkLabel(frame, text="Admin Login",
                             font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=(15, 10))

        self.username_entry = ctk.CTkEntry(frame, placeholder_text="Username")
        self.username_entry.pack(pady=8, padx=20, fill="x")

        self.password_entry = ctk.CTkEntry(frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=8, padx=20, fill="x")

        login_btn = ctk.CTkButton(frame, text="Login", command=self._handle_login)
        login_btn.pack(pady=(15, 5))

        self.bind("<Return>", lambda e: self._handle_login())

    def _handle_login(self):
        user = self.username_entry.get().strip()
        pwd = self.password_entry.get().strip()

        # simple fixed admin credentials
        if user == "admin" and pwd == "12345":
            self.destroy()
            self.on_success()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
