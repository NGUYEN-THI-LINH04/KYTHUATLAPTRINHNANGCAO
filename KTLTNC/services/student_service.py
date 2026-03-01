from data.file_handler import (
    get_all_students,
    write_student,
    export_excel,
    get_stats,
    FILE_PATH
)

import matplotlib.pyplot as plt


# ================== THÊM SINH VIÊN ==================
def add_student(msv, ten, subject, gk1, gk2, cc, thi):
    write_student(msv, ten, subject, gk1, gk2, cc, thi)


# ================== LẤY DANH SÁCH ==================
def get_students():
    return get_all_students()


# ================== XOÁ SINH VIÊN ==================
def delete_student(msv):
    students = get_all_students()
    new_list = [sv for sv in students if sv[0] != msv]

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        for sv in new_list:
            f.write(";".join(sv) + "\n")


# ================== SỬA SINH VIÊN ==================
def update_student(msv, ten, subject, gk1, gk2, cc, thi):
    students = get_all_students()
    updated = False

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        for sv in students:
            if sv[0] == msv:
                f.write(";".join([
                    msv, ten, subject,
                    str(gk1), str(gk2), str(cc), str(thi)
                ]) + "\n")
                updated = True
            else:
                f.write(";".join(sv) + "\n")

    return updated


# ================== XUẤT EXCEL ==================
def export_students_excel():
    export_excel("diem.xlsx")


# ================== THỐNG KÊ ==================
def get_statistics():
    return get_stats()


# ================== BIỂU ĐỒ THỐNG KÊ (CỬA SỔ RIÊNG) ==================
def show_grade_chart():
    students = get_all_students()
    if not students:
        return False

    thong_ke = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}

    for sv in students:
        diem_chu = sv[10]   # cột điểm chữ
        if diem_chu in thong_ke:
            thong_ke[diem_chu] += 1

    plt.figure(figsize=(6, 4))
    plt.bar(thong_ke.keys(), thong_ke.values())
    plt.title("Thống kê sinh viên theo điểm chữ")
    plt.xlabel("Điểm chữ")
    plt.ylabel("Số lượng sinh viên")
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show(block=False)

    return True


# ================== TÌM KIẾM SINH VIÊN ==================
def search_students(keyword, field="msv"):
    """
    field:
        - 'mssv'  : tìm theo mã sinh viên
        - 'hoten' : tìm theo họ tên
        - 'mon'   : tìm theo môn học
    """
    keyword = keyword.strip().lower()
    if not keyword:
        return get_all_students()

    students = get_all_students()
    result = []

    for sv in students:
        if field == "mssv" and keyword in sv[0].lower():
            result.append(sv)
        elif field == "hoten" and keyword in sv[1].lower():
            result.append(sv)
        elif field == "mon" and keyword in sv[2].lower():
            result.append(sv)

    return result


# ================== DỮ LIỆU BIỂU ĐỒ (NHÚNG TKINTER) ==================
def get_grade_chart_data():
    """
    Hàm này CHỈ TRẢ DỮ LIỆU
    Không vẽ, không ảnh hưởng các chức năng cũ
    """
    students = get_all_students()
    thong_ke = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}

    for sv in students:
        diem_chu = sv[10]
        if diem_chu in thong_ke:
            thong_ke[diem_chu] += 1

    return thong_ke

def search_students(keyword):
    students = get_students()
    result = []

    for sv in students:
        if keyword.lower() in sv["msv"].lower() or keyword.lower() in sv["ten"].lower():
            result.append(sv)

    # Sắp xếp theo điểm tổng từ cao xuống thấp
    result = sorted(result, key=lambda x: x["tong"], reverse=True)

    return result