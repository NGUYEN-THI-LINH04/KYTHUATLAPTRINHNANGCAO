from openpyxl import Workbook

FILE_PATH = "data/students.txt"


# ================== TÍNH ĐIỂM ==================
def tinh_diem(gk1, gk2, cc, thi):
    diem_thanh_phan = round((gk1 + gk2 + cc) / 3, 2)
    tong = round(diem_thanh_phan * 0.4 + thi * 0.6, 2)

    if tong >= 8.5:
        he4, chu = 4.0, "A"
    elif tong >= 7.0:
        he4, chu = 3.0, "B"
    elif tong >= 5.5:
        he4, chu = 2.0, "C"
    elif tong >= 4.0:
        he4, chu = 1.0, "D"
    else:
        he4, chu = 0.0, "F"

    return diem_thanh_phan, tong, he4, chu


# ================== ĐỌC FILE ==================
def get_all_students():
    students = []
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            for line in f:
                data = line.strip().split(";")
                if len(data) == 11:
                    students.append(data)
    except FileNotFoundError:
        pass
    return students


# ================== GHI THÊM SINH VIÊN ==================
def write_student(msv, ten, subject, gk1, gk2, cc, thi):
    gk1, gk2, cc, thi = map(float, [gk1, gk2, cc, thi])
    diem_tp, tong, he4, chu = tinh_diem(gk1, gk2, cc, thi)

    with open(FILE_PATH, "a", encoding="utf-8") as f:
        f.write(
            f"{msv};{ten};{subject};{gk1};{gk2};{cc};"
            f"{diem_tp};{thi};{tong};{he4};{chu}\n"
        )


# ================== XUẤT EXCEL ==================
def export_excel(filename="diem.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws.title = "Danh sách sinh viên"

    ws.append([
        "Mã SV", "Họ tên", "Môn học",
        "GK1", "GK2", "CC",
        "Điểm TP", "Thi", "Tổng",
        "Hệ 4", "Điểm chữ"
    ])

    for sv in get_all_students():
        ws.append(sv)

    wb.save(filename)


# ================== THỐNG KÊ ==================
def get_stats():
    students = get_all_students()
    if not students:
        return 0, 0, 0

    totals = [float(sv[8]) for sv in students]
    return len(students), round(sum(totals) / len(totals), 2), max(totals)
