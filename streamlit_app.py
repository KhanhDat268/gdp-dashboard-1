import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Cấu hình trang Streamlit
st.set_page_config(page_title="Quản lý điểm sinh viên", layout="wide")

# 1. Hiển thị tiêu đề
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# Khởi tạo dữ liệu 10 sinh viên
data = {
    "MSSV": ["SV001", "SV002", "SV003", "SV004", "SV005", "SV006", "SV007", "SV008", "SV009", "SV010"],
    "Họ tên": ["An", "Bình", "Chi", "Dũng", "Hà", "Lan", "Minh", "Nam", "Phúc", "Trang"],
    "Chuyên cần": [8, 9, 7, 10, 8, 6, 9, 7, 8, 10],
    "Giữa kỳ": [7, 8, 6, 9, 7, 5, 8, 6, 7, 9],
    "Cuối kỳ": [9, 8, 7, 10, 6, 7, 9, 8, 7, 10]
}

df = pd.DataFrame(data)

# Tính điểm Tổng kết
df["Tổng kết"] = (0.2 * df["Chuyên cần"] + 0.3 * df["Giữa kỳ"] + 0.5 * df["Cuối kỳ"]).round(2)

# Hàm xếp loại
def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    else:
        return "Yếu"

df["Xếp loại"] = df["Tổng kết"].apply(xep_loai)

# 2. Hiển thị bảng điểm của 10 sinh viên
st.subheader("📋 Bảng điểm sinh viên")
st.dataframe(df[["Họ tên", "Chuyên cần", "Giữa kỳ", "Cuối kỳ", "Tổng kết", "Xếp loại"]], use_container_width=True)

st.markdown("---")

# Các tính toán thống kê
diem_tb = df["Tổng kết"].mean()
diem_cao_nhat = df["Tổng kết"].max()
sv_cao_nhat = df[df["Tổng kết"] == diem_cao_nhat]

diem_thap_nhat = df["Tổng kết"].min()
sv_thap_nhat = df[df["Tổng kết"] == diem_thap_nhat]

so_sv_dat = (df["Tổng kết"] >= 5).sum()

# 3, 4, 5. Hiển thị các thông tin thống kê
st.subheader("📊 Thống kê chung")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Điểm trung bình của lớp", value=f"{diem_tb:.2f}")

with col2:
    st.metric(label="Số sinh viên đạt (>= 5.0)", value=f"{so_sv_dat} / {len(df)}")

with col3:
    d_cao = ", ".join(f"{row['Họ tên']} ({row['Tổng kết']})" for _, row in sv_cao_nhat.iterrows())
    st.markdown(f"**Sinh viên điểm cao nhất:**\n{d_cao}")

with col4:
    d_thap = ", ".join(f"{row['Họ tên']} ({row['Tổng kết']})" for _, row in sv_thap_nhat.iterrows())
    st.markdown(f"**Sinh viên điểm thấp nhất:**\n{d_thap}")

st.markdown("---")

# 6 & 7. Danh sách sổ xuống (Selectbox) và hiển thị chi tiết sinh viên
st.subheader("🔍 Tra cứu thông tin sinh viên")
danh_sach_sv = df["Họ tên"].tolist()
sv_duoc_chon = st.selectbox("Chọn một sinh viên:", danh_sach_sv)

# Hiển thị thông tin sinh viên được chọn
thong_tin_sv = df[df["Họ tên"] == sv_duoc_chon].iloc[0]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Chuyên cần", thong_tin_sv["Chuyên cần"])
c2.metric("Giữa kỳ", thong_tin_sv["Giữa kỳ"])
c3.metric("Cuối kỳ", thong_tin_sv["Cuối kỳ"])
c4.metric("Điểm tổng kết", thong_tin_sv["Tổng kết"])
c5.metric("Xếp loại", thong_tin_sv["Xếp loại"])

st.markdown("---")

# 8. Hiển thị biểu đồ cột điểm tổng kết
st.subheader("📈 Biểu đồ cột điểm tổng kết của 10 sinh viên")
fig, ax = plt.subplots(figsize=(10, 4))
bars = ax.bar(df["Họ tên"], df["Tổng kết"], color="#4C72B0")

# Thêm điểm số lên trên từng cột
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 0.1, f"{yval:.2f}", ha='center', va='bottom', fontsize=9)

ax.set_title("ĐIỂM TỔNG KẾT CỦA 10 SINH VIÊN", fontsize=12, fontweight='bold')
ax.set_xlabel("Họ tên sinh viên")
ax.set_ylabel("Điểm tổng kết")
ax.set_ylim(0, 10.5)
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)

# 9. Hiển thị Họ tên và MSSV ở cuối trang với kích thước chữ nhỏ
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 12px; color: gray; text-align: center;'>Người tạo ứng dụng: Nguyễn Văn A - MSSV: 12345678</p>", unsafe_allow_html=True)
