import tkinter as tk
from tkinter import messagebox, ttk

from services.student_service import (
    add_student,
    get_students,
    delete_student,
    update_student,
    export_students_excel,
    get_grade_chart_data
)

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


def start_app():
    root = tk.Tk()
    root.title("Phần Mềm Quản Lý Điểm Sinh Viên")
    root.geometry("1150x580")
    root.resizable(False, False)
    root.configure(bg="#f4f6f8")

    # ================== STYLE ==================
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Treeview",
        background="white",
        foreground="black",
        rowheight=26,
        fieldbackground="white",
        font=("Segoe UI", 10)
    )

    style.configure(
        "Treeview.Heading",
        background="#0d6efd",
        foreground="white",
        font=("Segoe UI", 10, "bold")
    )

    style.map("Treeview", background=[("selected", "#cfe2ff")])

    # ================== FRAME TRÁI ==================
    frame_left = tk.Frame(root, padx=15, pady=15, bg="white")
    frame_left.pack(side=tk.LEFT, fill=tk.Y)

    def label_entry(text, row):
        tk.Label(frame_left, text=text, bg="white",
                 font=("Segoe UI", 10)).grid(row=row, column=0, sticky="w", pady=3)
        e = tk.Entry(frame_left, width=25, font=("Segoe UI", 10))
        e.grid(row=row, column=1, pady=3)
        return e

    entry_msv = label_entry("MSSV:", 0)
    entry_ten = label_entry("Họ và tên:", 1)

    # ===== MÔN HỌC =====
    tk.Label(frame_left, text="Môn học:", bg="white",
             font=("Segoe UI", 10)).grid(row=2, column=0, sticky="w", pady=3)

    ds_mon = [
        "Lập trình Python",
        "C/C++",
        "Cơ sở dữ liệu",
        "Cấu trúc dữ liệu",
        "Đại số tuyến tính",
        "+ Môn khác..."
    ]

    combo_mon = ttk.Combobox(
        frame_left, values=ds_mon,
        state="readonly", width=22, font=("Segoe UI", 10)
    )
    combo_mon.grid(row=2, column=1, pady=3)
    combo_mon.current(0)

    entry_mon_khac = tk.Entry(frame_left, width=25, font=("Segoe UI", 10))

    def xu_ly_chon_mon(event=None):
        if combo_mon.get() == "+ Môn khác...":
            combo_mon.grid_remove()
            entry_mon_khac.grid(row=2, column=1, pady=3)
            entry_mon_khac.focus()

    def luu_mon_moi(event=None):
        mon = entry_mon_khac.get().strip()
        if mon:
            ds = list(combo_mon["values"])
            if mon not in ds:
                ds.insert(-1, mon)
                combo_mon["values"] = ds
            combo_mon.set(mon)
        entry_mon_khac.grid_remove()
        combo_mon.grid(row=2, column=1, pady=3)

    combo_mon.bind("<<ComboboxSelected>>", xu_ly_chon_mon)
    entry_mon_khac.bind("<Return>", luu_mon_moi)
    entry_mon_khac.bind("<FocusOut>", luu_mon_moi)

    entry_gk1 = label_entry("GK1:", 3)
    entry_gk2 = label_entry("GK2:", 4)
    entry_cc = label_entry("CC:", 5)
    entry_thi = label_entry("Thi:", 6)

    # ================== FUNCTIONS ==================
    def clear_input():
        for e in (entry_msv, entry_ten, entry_gk1, entry_gk2, entry_cc, entry_thi):
            e.delete(0, tk.END)

    def hien_thi():
        tree.delete(*tree.get_children())
        for sv in get_students():
            tree.insert("", tk.END, values=(
                sv[0], sv[1], sv[2],
                sv[3], sv[4], sv[5],
                sv[6], sv[7], sv[8], sv[10]
            ))

    def them_sv():
        add_student(
            entry_msv.get(),
            entry_ten.get(),
            combo_mon.get(),
            entry_gk1.get(),
            entry_gk2.get(),
            entry_cc.get(),
            entry_thi.get()
        )
        hien_thi()
        clear_input()

    def sua_sv():
        ok = update_student(
            entry_msv.get(),
            entry_ten.get(),
            combo_mon.get(),
            entry_gk1.get(),
            entry_gk2.get(),
            entry_cc.get(),
            entry_thi.get()
        )
        if ok:
            hien_thi()
            messagebox.showinfo("OK", "Đã sửa sinh viên")
        else:
            messagebox.showwarning("Lỗi", "Không tìm thấy MSSV")

    def xoa_sv():
        delete_student(entry_msv.get())
        hien_thi()
        clear_input()

    def btn(text, cmd, row, color):
        tk.Button(
            frame_left, text=text, command=cmd,
            bg=color, fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat", width=20
        ).grid(row=row, columnspan=2, pady=4)

    btn("Thêm", them_sv, 7, "#198754")
    btn("Sửa", sua_sv, 8, "#0d6efd")
    btn("Xóa", xoa_sv, 9, "#dc3545")
    btn("Xuất Excel", export_students_excel, 10, "#20c997")

    # ================== FRAME PHẢI ==================
    frame_right = tk.Frame(root, bg="#f4f6f8")
    frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    frame_search = tk.Frame(frame_right, bg="#f4f6f8", pady=5)
    frame_search.pack(fill=tk.X)

    entry_search = tk.Entry(frame_search, width=30, font=("Segoe UI", 10))
    entry_search.pack(side=tk.LEFT, padx=5)

    combo_search = ttk.Combobox(
        frame_search,
        values=["Mã SV", "Họ tên", "Môn học"],
        state="readonly", width=12
    )
    combo_search.current(0)
    combo_search.pack(side=tk.LEFT, padx=5)

    def tim_kiem():
        keyword = entry_search.get().lower()
        idx = {"Mã SV": 0, "Họ tên": 1, "Môn học": 2}[combo_search.get()]
        tree.delete(*tree.get_children())
        for sv in get_students():
            if keyword in sv[idx].lower():
                tree.insert("", tk.END, values=(
                    sv[0], sv[1], sv[2],
                    sv[3], sv[4], sv[5],
                    sv[6], sv[7], sv[8], sv[10]
                ))

    tk.Button(frame_search, text="Tìm", command=tim_kiem,
              bg="#0d6efd", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(frame_search, text="Tất cả", command=hien_thi,
              bg="#6c757d", fg="white").pack(side=tk.LEFT)

    # ================== TABLE ==================
    frame_table = tk.Frame(frame_right)
    frame_table.pack(fill=tk.BOTH, expand=True)

    columns = ("mssv", "hoten", "mon", "gk1", "gk2", "cc", "tp", "thi", "tong", "tich")
    tree = ttk.Treeview(frame_table, columns=columns, show="headings")

    headings = [
        ("mssv", "MSSV"), ("hoten", "Họ và tên"), ("mon", "Môn"),
        ("gk1", "GK1"), ("gk2", "GK2"), ("cc", "CC"),
        ("tp", "TP"), ("thi", "Thi"), ("tong", "Tổng"), ("tich", "Tích")
    ]

    for col, text in headings:
        tree.heading(col, text=text)
        tree.column(col, width=90, anchor="center")

    tree.pack(fill=tk.BOTH, expand=True)

    def chon_dong(event):
        item = tree.focus()
        if not item:
            return
        v = tree.item(item, "values")
        clear_input()
        entry_msv.insert(0, v[0])
        entry_ten.insert(0, v[1])
        combo_mon.set(v[2])
        entry_gk1.insert(0, v[3])
        entry_gk2.insert(0, v[4])
        entry_cc.insert(0, v[5])
        entry_thi.insert(0, v[7])

    tree.bind("<<TreeviewSelect>>", chon_dong)

    # ================== BIỂU ĐỒ (CỬA SỔ RIÊNG) ==================
    def ve_bieu_do():
        data = get_grade_chart_data()

        if not data:
            messagebox.showwarning("Thông báo", "Không có dữ liệu để vẽ biểu đồ")
            return

        win = tk.Toplevel(root)
        win.title("Biểu đồ thống kê điểm chữ")
        win.geometry("500x400")
        win.resizable(False, False)

        fig, ax = plt.subplots(figsize=(5, 4))
        ax.bar(data.keys(), data.values())
        ax.set_title("Thống kê điểm chữ")
        ax.set_xlabel("Điểm chữ")
        ax.set_ylabel("Số sinh viên")

        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        plt.close(fig)

    btn("Biểu đồ", ve_bieu_do, 11, "#fd7e14")

    hien_thi()
    root.mainloop()


if __name__ == "__main__":
    start_app()
