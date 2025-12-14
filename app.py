import customtkinter as ctk
from ui_login import LoginWindow
from ui_dashboard import Dashboard


def open_dashboard():
    # new main window for dashboard
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = Dashboard()
    app.mainloop()


def main():
    # first show login
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    login = LoginWindow(on_success=open_dashboard)
    login.mainloop()


if __name__ == "__main__":
    main()
