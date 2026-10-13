import streamlit as st
import pandas as pd

# Tiêu đề ứng dụng
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# 1. Khởi tạo dữ liệu cho 10 sinh viên
data = {
    'Ho_va_ten': [
        'An', 'Bình', 'Chi', 'Dũng','Hà','Lan',
        'Minh', 'Nam', 'Phúc', 'Trang'
    ],
    'Chuyen_can': [8, 9, 7, 10, 8, 6, 9, 7, 8, 10],
    'Giua_ky': [7,8, 6, 9, 7, 5, 8, 6, 7,9],
    'Cuoi_ky': [9, 8, 7, 10, 6, 7, 9, 8, 7, 10]
}

# 2. Tạo DataFrame từ dữ liệu
df = pd.DataFrame(data)

# 3. Tính điểm tổng kết (20% Chuyên cần + 30% Giữa kỳ + 50% Cuối kỳ) và làm tròn 2 chữ số
df['Tong_ket'] = (0.2 * df['Chuyen_can'] + 0.3 * df['Giua_ky'] + 0.5 * df['Cuoi_ky']).round(2)

# 4. Định nghĩa hàm xếp loại sinh viên dựa trên điểm tổng kết
def phan_loai(diem):
    if diem >= 8.5:
        return 'Giỏi'
    elif diem >= 7.0:
        return 'Khá'
    elif diem >= 5.0:
        return 'Trung bình'
    else:
        return 'Yếu'

# 5. Tạo thêm cột Xep_loai bằng cách áp dụng hàm phan_loai vào cột Tong_ket
df['Xep_loai'] = df['Tong_ket'].apply(phan_loai)

# 6. Hiển thị bảng dữ liệu sinh viên lên web
st.subheader("📋 Bảng danh sách điểm sinh viên")
st.dataframe(df, use_container_width=True)

# 7. Thống kê chung
st.subheader("📊 Kết quả thống kê")

# Tính điểm tổng kết trung bình của lớp
diem_tb_lop = df['Tong_ket'].mean()
st.write(f"- **Điểm tổng kết trung bình của lớp:** {diem_tb_lop:.2f}")

# Tìm sinh viên có điểm tổng kết cao nhất
sv_cao_nhat = df[df['Tong_ket'] == df['Tong_ket'].max()]
for index, row in sv_cao_nhat.iterrows():
    st.write(f"- **Sinh viên có điểm tổng kết cao nhất:** {row['Ho_va_ten']} ({row['Tong_ket']} điểm)")

# Tìm sinh viên có điểm tổng kết thấp nhất
sv_thap_nhat = df[df['Tong_ket'] == df['Tong_ket'].min()]
for index, row in sv_thap_nhat.iterrows():
    st.write(f"- **Sinh viên có điểm tổng kết thấp nhất:** {row['Ho_va_ten']} ({row['Tong_ket']} điểm)")

# Đếm số sinh viên đạt (điểm tổng kết >= 5)
so_sv_dat = df[df['Tong_ket'] >= 5.0].shape[0]
st.write(f"- **Số sinh viên đạt (Tổng kết >= 5):** {so_sv_dat} sinh viên")

# 8. Tra cứu chi tiết từng sinh viên (Selectbox)
st.subheader("🔍 Tra cứu chi tiết sinh viên")
selected_name = st.selectbox("Chọn tên sinh viên để xem:", df['Ho_va_ten'].tolist())
sv_info = df[df['Ho_va_ten'] == selected_name].iloc[0]

st.info(f"""
- **Họ tên:** {sv_info['Ho_va_ten']}
- **Điểm Chuyên cần:** {sv_info['Chuyen_can']}
- **Điểm Giữa kỳ:** {sv_info['Giua_ky']}
- **Điểm Cuối kỳ:** {sv_info['Cuoi_ky']}
- **Điểm Tổng kết:** {sv_info['Tong_ket']}
- **Xếp loại:** {sv_info['Xep_loai']}
""")

# 9. Biểu đồ cột điểm tổng kết
st.subheader("📈 Biểu đồ điểm tổng kết của 10 sinh viên")
chart_data = df.set_index('Ho_va_ten')['Tong_ket']
st.bar_chart(chart_data)
# 10. Chân trang (Footer) thông tin cá nhân
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: small; color: gray;'>Họ tên: [Dương Huỳnh Khánh Đạt] – MSSV: [040208011265]</p>", unsafe_allow_html=True)
