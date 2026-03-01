import tkinter as tk
from tkinter import messagebox

from services.auth_service import check_login
from ui.gui import start_app

def start_login():
    root = tk.Tk()
    root.title("Đăng nhập hệ thống")
    root.geometry("350x220")
    root.resizable(False, False)

    tk.Label(root, text="ĐĂNG NHẬP",
             font=("Segoe UI", 14, "bold")).pack(pady=10)

    frame = tk.Frame(root)
    frame.pack(pady=10)

    tk.Label(frame, text="Tên đăng nhập:").grid(row=0, column=0, sticky="w")
    entry_user = tk.Entry(frame, width=25)
    entry_user.grid(row=0, column=1, pady=5)

    tk.Label(frame, text="Mật khẩu:").grid(row=1, column=0, sticky="w")
    entry_pass = tk.Entry(frame, width=25, show="*")
    entry_pass.grid(row=1, column=1, pady=5)

    def login():
        user = entry_user.get().strip()
        pw = entry_pass.get().strip()

        if not user or not pw:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đủ")
            return

        info = check_login(user, pw)
        if info:
            messagebox.showinfo(
                "Thành công",
                f"Xin chào {info['username']} ({info['role']})"
            )
            root.destroy()
            start_app()   # 👉 mở giao diện quản lý điểm
        else:
            messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu")

    tk.Button(root, text="Đăng nhập",
              width=20,
              bg="#0d6efd",
              fg="white",
              command=login).pack(pady=10)

    root.mainloop()
