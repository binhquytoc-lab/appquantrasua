import streamlit as st
from datetime import datetime
import pandas as pd
import io


# ============================================================
# CẤU HÌNH TRANG
# ============================================================

st.set_page_config(
    page_title="Trà Sữa - Tính Bill",
    page_icon="🧋",
    layout="wide"
)


# ============================================================
# CSS GIAO DIỆN
# ============================================================

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.title {
    text-align: center;
    font-size: 38px;
    font-weight: bold;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #666;
    font-size: 18px;
    margin-bottom: 25px;
}

.bill-box {
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #ddd;
    background-color: #fafafa;
}

.total-box {
    padding: 20px;
    border-radius: 15px;
    background-color: #f5f5f5;
    text-align: right;
}

.big-total {
    font-size: 30px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# DỮ LIỆU MENU
# ============================================================

MENU = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa trân châu": 35000,
    "Trà sữa matcha": 38000,
    "Trà sữa socola": 38000,
    "Trà sữa khoai môn": 38000,
    "Trà sữa dâu": 38000,
    "Trà đào": 30000,
    "Trà vải": 30000,
    "Trà chanh": 25000,
    "Trà tắc": 25000,
    "Matcha đá xay": 45000,
    "Cacao đá xay": 45000,
}

TOPPINGS = {
    "Không topping": 0,
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch trái cây": 5000,
    "Thạch phô mai": 7000,
    "Pudding trứng": 7000,
    "Kem cheese": 10000,
    "Hạt thủy tinh": 6000,
}

SIZES = {
    "M": 0,
    "L": 5000,
    "XL": 10000,
}

SUGAR_LEVELS = [
    "100% đường",
    "70% đường",
    "50% đường",
    "30% đường",
    "0% đường",
]

ICE_LEVELS = [
    "100% đá",
    "70% đá",
    "50% đá",
    "30% đá",
    "0% đá",
]


# ============================================================
# KHỞI TẠO SESSION STATE
# ============================================================

if "cart" not in st.session_state:
    st.session_state.cart = []

if "invoice" not in st.session_state:
    st.session_state.invoice = None

if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""


# ============================================================
# HÀM ĐỊNH DẠNG TIỀN
# ============================================================

def format_money(value):
    return f"{int(value):,}".replace(",", ".") + " VNĐ"


# ============================================================
# HÀM TÍNH GIÁ MỘT MÓN
# ============================================================

def calculate_item_price(drink, size, topping):
    base_price = MENU[drink]
    size_price = SIZES[size]
    topping_price = TOPPINGS[topping]

    total = base_price + size_price + topping_price

    return total


# ============================================================
# TIÊU ĐỀ
# ============================================================

st.markdown(
    '<div class="title">🧋 TRÀ SỮA BILL</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Hệ thống tính tiền và xuất hóa đơn quán trà sữa</div>',
    unsafe_allow_html=True
)


# ============================================================
# THÔNG TIN KHÁCH HÀNG
# ============================================================

st.subheader("👤 Thông tin khách hàng")

customer_name = st.text_input(
    "Tên khách hàng",
    value=st.session_state.customer_name,
    placeholder="Ví dụ: Nguyễn Văn An"
)

st.session_state.customer_name = customer_name


# ============================================================
# CHIA 2 CỘT
# ============================================================

col1, col2 = st.columns([1.1, 0.9])


# ============================================================
# CỘT TRÁI - CHỌN MÓN
# ============================================================

with col1:

    st.subheader("🧋 Thêm món")

    drink = st.selectbox(
        "Loại trà sữa / đồ uống",
        list(MENU.keys())
    )

    size = st.selectbox(
        "Size",
        list(SIZES.keys())
    )

    topping = st.selectbox(
        "Topping",
        list(TOPPINGS.keys())
    )

    sugar = st.select_slider(
        "Mức độ đường",
        options=SUGAR_LEVELS,
        value="100% đường"
    )

    ice = st.select_slider(
        "Mức độ đá",
        options=ICE_LEVELS,
        value="100% đá"
    )

    quantity = st.number_input(
        "Số lượng",
        min_value=1,
        max_value=20,
        value=1,
        step=1
    )

    # Tính giá
    unit_price = calculate_item_price(
        drink,
        size,
        topping
    )

    item_total = unit_price * quantity

    st.info(
        f"Đơn giá: **{format_money(unit_price)}**\n\n"
        f"Thành tiền: **{format_money(item_total)}**"
    )

    if st.button(
        "➕ THÊM MÓN VÀO HÓA ĐƠN",
        use_container_width=True,
        type="primary"
    ):

        item = {
            "Tên món": drink,
            "Size": size,
            "Topping": topping,
            "Đường": sugar,
            "Đá": ice,
            "Số lượng": quantity,
            "Đơn giá": unit_price,
            "Thành tiền": item_total
        }

        st.session_state.cart.append(item)

        st.success(
            f"Đã thêm {quantity} x {drink} vào hóa đơn!"
        )


# ============================================================
# CỘT PHẢI - GIỎ HÀNG
# ============================================================

with col2:

    st.subheader("🛒 Giỏ hàng")

    if len(st.session_state.cart) == 0:

        st.info(
            "Chưa có món nào.\n\n"
            "Hãy chọn món bên trái và bấm "
            "**THÊM MÓN VÀO HÓA ĐƠN**."
        )

    else:

        total_bill = 0

        for i, item in enumerate(st.session_state.cart):

            st.markdown(
                f"### {i + 1}. {item['Tên món']}"
            )

            st.write(
                f"Size: **{item['Size']}** | "
                f"Topping: **{item['Topping']}**"
            )

            st.write(
                f"Đường: **{item['Đường']}** | "
                f"Đá: **{item['Đá']}**"
            )

            st.write(
                f"Số lượng: **{item['Số lượng']}**"
            )

            st.write(
                f"Thành tiền: **{format_money(item['Thành tiền'])}**"
            )

            # Nút xóa món
            if st.button(
                f"🗑️ Xóa món {i + 1}",
                key=f"delete_{i}"
            ):
                st.session_state.cart.pop(i)
                st.rerun()

            st.divider()

            total_bill += item["Thành tiền"]

        st.markdown(
            f"""
            <div class="total-box">
                <div>TỔNG CỘNG</div>
                <div class="big-total">
                    {format_money(total_bill)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# THANH TOÁN
# ============================================================

st.divider()

st.subheader("💳 Thanh toán")

if len(st.session_state.cart) == 0:

    st.warning("Vui lòng thêm ít nhất một món trước khi thanh toán.")

else:

    total_bill = sum(
        item["Thành tiền"]
        for item in st.session_state.cart
    )

    payment_col1, payment_col2 = st.columns(2)

    with payment_col1:

        payment_method = st.selectbox(
            "Phương thức thanh toán",
            [
                "Tiền mặt",
                "Chuyển khoản",
                "Ví điện tử"
            ]
        )

    with payment_col2:

        discount = st.number_input(
            "Giảm giá (VNĐ)",
            min_value=0,
            max_value=int(total_bill),
            value=0,
            step=5000
        )

    final_total = total_bill - discount

    st.markdown(
        f"""
        <div class="total-box">
            <div>TẠM TÍNH</div>
            <h3>{format_money(total_bill)}</h3>

            <div>GIẢM GIÁ</div>
            <h3>- {format_money(discount)}</h3>

            <hr>

            <div>TỔNG THANH TOÁN</div>
            <div class="big-total">
                {format_money(final_total)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if st.button(
        "💰 THANH TOÁN & TẠO HÓA ĐƠN",
        use_container_width=True,
        type="primary"
    ):

        invoice_time = datetime.now()

        st.session_state.invoice = {
            "customer_name": customer_name
            if customer_name.strip()
            else "Khách lẻ",

            "items": st.session_state.cart.copy(),

            "subtotal": total_bill,

            "discount": discount,

            "total": final_total,

            "payment_method": payment_method,

            "time": invoice_time.strftime(
                "%d/%m/%Y %H:%M:%S"
            ),

            "invoice_number": invoice_time.strftime(
                "%Y%m%d%H%M%S"
            )
        }

        st.success("Thanh toán thành công!")

        st.balloons()


# ============================================================
# HIỂN THỊ HÓA ĐƠN
# ============================================================

if st.session_state.invoice is not None:

    invoice = st.session_state.invoice

    st.divider()

    st.subheader("🧾 HÓA ĐƠN THANH TOÁN")

    st.markdown(
        f"""
        <div class="bill-box">

        <h2 style="text-align:center;">
        🧋 TRÀ SỮA BILL
        </h2>

        <p style="text-align:center;">
        HÓA ĐƠN THANH TOÁN
        </p>

        <hr>

        <p>
        <b>Mã hóa đơn:</b> {invoice['invoice_number']}
        </p>

        <p>
        <b>Khách hàng:</b> {invoice['customer_name']}
        </p>

        <p>
        <b>Thời gian:</b> {invoice['time']}
        </p>

        <p>
        <b>Thanh toán:</b> {invoice['payment_method']}
        </p>

        <hr>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # BẢNG CHI TIẾT HÓA ĐƠN
    # ========================================================

    invoice_rows = []

    for i, item in enumerate(invoice["items"]):

        invoice_rows.append({
            "STT": i + 1,
            "Tên món": item["Tên món"],
            "Size": item["Size"],
            "Topping": item["Topping"],
            "Đường": item["Đường"],
            "Đá": item["Đá"],
            "SL": item["Số lượng"],
            "Đơn giá": format_money(item["Đơn giá"]),
            "Thành tiền": format_money(item["Thành tiền"])
        })

    invoice_df = pd.DataFrame(invoice_rows)

    st.dataframe(
        invoice_df,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # TỔNG TIỀN
    # ========================================================

    st.markdown(
        f"""
        <div class="total-box">

        <p>
        Tạm tính:
        <b>{format_money(invoice['subtotal'])}</b>
        </p>

        <p>
        Giảm giá:
        <b>- {format_money(invoice['discount'])}</b>
        </p>

        <hr>

        <div>
        TỔNG THANH TOÁN
        </div>

        <div class="big-total">
        {format_money(invoice['total'])}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # XUẤT EXCEL
    # ========================================================

    st.subheader("📥 Xuất hóa đơn")

    export_data = []

    for item in invoice["items"]:

        export_data.append({
            "Mã hóa đơn": invoice["invoice_number"],
            "Khách hàng": invoice["customer_name"],
            "Thời gian": invoice["time"],
            "Tên món": item["Tên món"],
            "Size": item["Size"],
            "Topping": item["Topping"],
            "Đường": item["Đường"],
            "Đá": item["Đá"],
            "Số lượng": item["Số lượng"],
            "Đơn giá": item["Đơn giá"],
            "Thành tiền": item["Thành tiền"],
            "Phương thức thanh toán": invoice["payment_method"]
        })

    export_df = pd.DataFrame(export_data)


    # ========================================================
    # XUẤT CSV
    # ========================================================

    csv_data = export_df.to_csv(
        index=False,
        encoding="utf-8-sig"
    )

    col_export1, col_export2 = st.columns(2)

    with col_export1:

        st.download_button(
            label="📄 TẢI HÓA ĐƠN CSV",
            data=csv_data,
            file_name=f"hoa_don_{invoice['invoice_number']}.csv",
            mime="text/csv",
            use_container_width=True
        )


    # ========================================================
    # XUẤT EXCEL
    # ========================================================

    with col_export2:

        excel_buffer = io.BytesIO()

        with pd.ExcelWriter(
            excel_buffer,
            engine="openpyxl"
        ) as writer:

            export_df.to_excel(
                writer,
                index=False,
                sheet_name="Hoa Don"
            )

        st.download_button(
            label="📊 TẢI HÓA ĐƠN EXCEL",
            data=excel_buffer.getvalue(),
            file_name=f"hoa_don_{invoice['invoice_number']}.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            ),
            use_container_width=True
        )


# ============================================================
# NÚT TẠO HÓA ĐƠN MỚI
# ============================================================

if st.session_state.invoice is not None:

    st.write("")

    if st.button(
        "🆕 TẠO HÓA ĐƠN MỚI",
        use_container_width=True
    ):

        st.session_state.cart = []
        st.session_state.invoice = None
        st.session_state.customer_name = ""

        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🧋 Trà Sữa Bill | Hệ thống tính tiền hóa đơn"
)
