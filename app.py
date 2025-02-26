import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="High-End Japanese Hotel - Pricing Calculator",
    page_icon="warakulogo.png",
    layout="centered"
)

# ---------- CUSTOM CSS (Optional) ----------
custom_css = """
<style>
body {
    background: url("https://images.unsplash.com/photo-1586500051230-836e79a2b353?ixlib=rb-4.0.3&auto=format&fit=crop&w=2067&q=80");
    background-size: cover;
    background-position: center;
    color: #fff;
    font-family: 'Noto Sans JP', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background-color: rgba(0,0,0,0.4) !important;
    padding: 2rem;
    border-radius: 1rem;
}

h1, h2, h3, h4 {
    font-family: 'Noto Serif JP', serif;
    font-weight: 500;
    color: #fffae6;
    text-shadow: 1px 1px 2px #000;
}

label {
    font-size: 1.1rem;
    color: #fffae6;
}

.stButton button {
    background-color: #6B2E5F !important;
    border: none;
    color: #ffffff;
    padding: 0.6rem 1.2rem;
    font-size: 1rem;
    border-radius: 8px;
    cursor: pointer;
}
.stButton button:hover {
    background-color: #8f437c !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------- HELPER FUNCTIONS ----------
def parse_price(input_str):
    """
    Convert a free-text yen input (e.g., '¥30,000' or '30000') to a float.
    Returns 0.0 if parsing fails.
    """
    cleaned = input_str.replace("¥", "").replace(",", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return 0.0

def parse_discount(input_str):
    """
    Parse a discount input (e.g., '10%' or '¥2000').
    Returns (is_percent, value).
      - is_percent = True if it's a '%' discount.
      - value = numeric discount amount (float).
    """
    inp = input_str.strip()
    if inp.endswith("%"):
        # Percentage discount
        try:
            val = float(inp[:-1])  # remove '%' and convert
            return (True, val)
        except ValueError:
            return (False, 0.0)
    else:
        # Assume currency discount
        cleaned = inp.replace("¥", "").replace(",", "").strip()
        try:
            val = float(cleaned)
            return (False, val)
        except ValueError:
            return (False, 0.0)

def apply_discount(base_price, discount_str):
    """
    Applies discount to base_price based on discount_str.
    If discount is percentage, base_price * (1 - discount%).
    If discount is absolute yen, base_price - discount.
    Returns final price (>= 0).
    """
    (is_percent, val) = parse_discount(discount_str)
    if is_percent:
        discounted_price = base_price - (base_price * (val / 100.0))
    else:
        discounted_price = base_price - val

    return max(discounted_price, 0)


# ---------- TITLE ----------
st.title("和楽 料金計算システム")
st.markdown("**すべて税込でご入力ください。** 大人・子供の人数と、それぞれが希望する食事オプション・追加料金を入力します。")

# ====================
# 1) ROOM PRICING
# ====================
# ---------- ADULT INPUTS ----------
st.subheader("1. 大人料金")
col1, col2 = st.columns(2)
with col1:
    adult_base_str = st.text_input("大人1名あたりの基本料金 (税込)", value="0")
with col2:
    adult_discount_str = st.text_input("大人向け割引 (例: '10%' or '¥2000')", value="0")

num_adults = st.number_input("大人の人数", min_value=0, value=0)

# ---------- CHILD INPUTS ----------
st.subheader("2. 子供料金")
col3, col4 = st.columns(2)
with col3:
    child_base_str = st.text_input("子供1名あたりの基本料金 (税込)", value="0")
with col4:
    child_discount_str = st.text_input("子供向け割引 (例: '5%' or '¥1000')", value="0")

num_children = st.number_input("子供の人数", min_value=0, value=0)

# ====================
# 2) MEALS
# ====================
# ---------- MEALS: ADULTS ----------
st.subheader("3. 食事オプション（大人）")
with st.expander("大人用の食事詳細を入力する"):
    colA1, colA2 = st.columns(2)
    with colA1:
        adult_breakfast_str = st.text_input("朝食料金（大人1名あたり・税込）", value="0")
        adults_breakfast_count = st.number_input("朝食を希望する大人の人数", min_value=0, value=0)
    with colA2:
        adult_dinner_str = st.text_input("夕食料金（大人1名あたり・税込）", value="0")
        adults_dinner_count = st.number_input("夕食を希望する大人の人数", min_value=0, value=0)

# ---------- MEALS: CHILDREN ----------
st.subheader("4. 食事オプション（子供）")
with st.expander("子供用の食事詳細を入力する"):
    colC1, colC2 = st.columns(2)
    with colC1:
        child_breakfast_str = st.text_input("朝食料金（子供1名あたり・税込）", value="0")
        children_breakfast_count = st.number_input("朝食を希望する子供の人数", min_value=0, value=0)
    with colC2:
        child_dinner_str = st.text_input("夕食料金（子供1名あたり・税込）", value="0")
        children_dinner_count = st.number_input("夕食を希望する子供の人数", min_value=0, value=0)


# ====================
# 3) ADDITIONAL CHARGES
# ====================
st.subheader("5. 追加料金 (Extra Charges)")

# ---------- ADULT ADDITIONAL CHARGES ----------
with st.expander("大人向けの追加料金"):
    st.markdown("下記に大人用の追加料金を入力してください。**割引を含む場合は% または ¥ で入力**。")

    adult_extra_count = st.number_input("大人向け追加項目の数", min_value=0, value=0, step=1)

    adult_extra_items = []
    for i in range(adult_extra_count):
        st.write(f"**追加項目 #{i+1} (大人)**")
        col_ex1, col_ex2, col_ex3, col_ex4 = st.columns([2,1,1,1])
        with col_ex1:
            extra_name = st.text_input(f"項目名", value="", key=f"adult_extra_name_{i}")
        with col_ex2:
            extra_cost_str = st.text_input(f"料金 (円)", value="0", key=f"adult_extra_cost_{i}")
        with col_ex3:
            extra_qty = st.number_input(f"数量", min_value=0, value=1, key=f"adult_extra_qty_{i}")
        with col_ex4:
            extra_discount_str = st.text_input("割引 (例: '10%' or '¥500')", value="0", 
                                               key=f"adult_extra_discount_{i}")
        
        adult_extra_items.append({
            "name": extra_name,
            "cost_str": extra_cost_str,
            "qty": extra_qty,
            "discount_str": extra_discount_str
        })

# ---------- CHILD ADDITIONAL CHARGES ----------
with st.expander("子供向けの追加料金"):
    st.markdown("下記に子供用の追加料金を入力してください。**割引を含む場合は% または ¥ で入力**。")

    child_extra_count = st.number_input("子供向け追加項目の数", min_value=0, value=0, step=1)

    child_extra_items = []
    for i in range(child_extra_count):
        st.write(f"**追加項目 #{i+1} (子供)**")
        col_ex1, col_ex2, col_ex3, col_ex4 = st.columns([2,1,1,1])
        with col_ex1:
            extra_name = st.text_input(f"項目名", value="", key=f"child_extra_name_{i}")
        with col_ex2:
            extra_cost_str = st.text_input(f"料金 (円)", value="0", key=f"child_extra_cost_{i}")
        with col_ex3:
            extra_qty = st.number_input(f"数量", min_value=0, value=1, key=f"child_extra_qty_{i}")
        with col_ex4:
            extra_discount_str = st.text_input("割引 (例: '10%' or '¥300')", value="0", 
                                               key=f"child_extra_discount_{i}")
        
        child_extra_items.append({
            "name": extra_name,
            "cost_str": extra_cost_str,
            "qty": extra_qty,
            "discount_str": extra_discount_str
        })


# ====================
# CALCULATION
# ====================
btn_calculate = st.button("料金を計算する")
if btn_calculate:
    # --------------------------------------------------
    # 1) Room base & discount (EXISTING LOGIC - UNCHANGED)
    # --------------------------------------------------
    adult_base_price = parse_price(adult_base_str)
    child_base_price = parse_price(child_base_str)
    final_adult_price = apply_discount(adult_base_price, adult_discount_str)
    final_child_price = apply_discount(child_base_price, child_discount_str)

    total_adult_cost = final_adult_price * num_adults
    total_child_cost = final_child_price * num_children

    # --------------------------------------------------
    # 2) Meal costs (EXISTING LOGIC - UNCHANGED)
    # --------------------------------------------------
    adult_breakfast_price = parse_price(adult_breakfast_str)
    adult_dinner_price = parse_price(adult_dinner_str)
    child_breakfast_price = parse_price(child_breakfast_str)
    child_dinner_price = parse_price(child_dinner_str)

    total_adult_meal_cost = (adult_breakfast_price * adults_breakfast_count) \
                            + (adult_dinner_price * adults_dinner_count)
    total_child_meal_cost = (child_breakfast_price * children_breakfast_count) \
                            + (child_dinner_price * children_dinner_count)

    # --------------------------------------------------
    # 3) Additional charges (ADULTS) - NOW WITH DISCOUNT
    # --------------------------------------------------
    total_adult_extras = 0
    for item in adult_extra_items:
        cost_val = parse_price(item["cost_str"])
        # Apply per-item discount
        discounted_cost = apply_discount(cost_val, item["discount_str"])
        line_total = discounted_cost * item["qty"]
        total_adult_extras += line_total

    # --------------------------------------------------
    # 4) Additional charges (CHILDREN) - NOW WITH DISCOUNT
    # --------------------------------------------------
    total_child_extras = 0
    for item in child_extra_items:
        cost_val = parse_price(item["cost_str"])
        discounted_cost = apply_discount(cost_val, item["discount_str"])
        line_total = discounted_cost * item["qty"]
        total_child_extras += line_total

    # --------------------------------------------------
    # 5) Final Summation
    # --------------------------------------------------
    grand_total = (total_adult_cost + total_child_cost
                   + total_adult_meal_cost + total_child_meal_cost
                   + total_adult_extras + total_child_extras)

    # ==============
    # OUTPUT
    # ==============
    st.markdown("---")
    st.subheader("料金明細 / Summary")

    # Room Subtotals
    if num_adults > 0:
        st.write(
            f"**大人 客室小計**: ¥{int(total_adult_cost):,} "
            f"( {int(final_adult_price):,} 円 × {num_adults}名 )"
        )
    if num_children > 0:
        st.write(
            f"**子供 客室小計**: ¥{int(total_child_cost):,} "
            f"( {int(final_child_price):,} 円 × {num_children}名 )"
        )

    # Meal Subtotals
    st.write(
        f"**大人 食事小計**: ¥{int(total_adult_meal_cost):,} "
        f"（朝食: ¥{int(adult_breakfast_price):,} × {adults_breakfast_count}名 + "
        f"夕食: ¥{int(adult_dinner_price):,} × {adults_dinner_count}名）"
    )
    st.write(
        f"**子供 食事小計**: ¥{int(total_child_meal_cost):,} "
        f"（朝食: ¥{int(child_breakfast_price):,} × {children_breakfast_count}名 + "
        f"夕食: ¥{int(child_dinner_price):,} × {children_dinner_count}名）"
    )

    # Additional Charges Subtotals (Adults)
    if adult_extra_items:
        st.markdown("**大人 追加料金:**")
        for item in adult_extra_items:
            cost_val = parse_price(item["cost_str"])
            discounted_cost = apply_discount(cost_val, item["discount_str"])
            line_total = discounted_cost * item["qty"]
            # Show the original line with discount breakdown
            if item["discount_str"] and item["discount_str"] != "0":
                st.write(
                    f"- {item['name']} : "
                    f"**(割引前)** ¥{int(cost_val):,} → "
                    f"**(割引後)** ¥{int(discounted_cost):,} "
                    f"× {item['qty']}個 = ¥{int(line_total):,} "
                    f" _(割引: {item['discount_str']})_"
                )
            else:
                st.write(
                    f"- {item['name']} : ¥{int(cost_val):,} "
                    f"× {item['qty']} = ¥{int(line_total):,}"
                )
        st.write(f"**大人 追加料金小計**: ¥{int(total_adult_extras):,}")

    # Additional Charges Subtotals (Children)
    if child_extra_items:
        st.markdown("**子供 追加料金:**")
        for item in child_extra_items:
            cost_val = parse_price(item["cost_str"])
            discounted_cost = apply_discount(cost_val, item["discount_str"])
            line_total = discounted_cost * item["qty"]
            # Show the original line with discount breakdown
            if item["discount_str"] and item["discount_str"] != "0":
                st.write(
                    f"- {item['name']} : "
                    f"**(割引前)** ¥{int(cost_val):,} → "
                    f"**(割引後)** ¥{int(discounted_cost):,} "
                    f"× {item['qty']}個 = ¥{int(line_total):,} "
                    f" _(割引: {item['discount_str']})_"
                )
            else:
                st.write(
                    f"- {item['name']} : ¥{int(cost_val):,} "
                    f"× {item['qty']} = ¥{int(line_total):,}"
                )
        st.write(f"**子供 追加料金小計**: ¥{int(total_child_extras):,}")

    # Grand Total
    st.markdown(f"## **合計金額：¥{int(grand_total):,}**")
    st.balloons()
