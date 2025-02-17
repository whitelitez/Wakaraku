import streamlit as st

# ---------- PAGE CONFIGURATION ----------
st.set_page_config(
    page_title="High-End Japanese Hotel - Room Pricing",
    page_icon=":shinto_shrine:",  # An optional emoji or icon
    layout="centered"
)

# ---------- CUSTOM STYLING / CSS ----------
# Below is an example of injecting custom CSS to give a "lush" feel.
# Adjust the background, colors, fonts, etc. to match your hotel's branding.
custom_css = """
<style>
/* Lush background image */
body {
    background: url("https://images.unsplash.com/photo-1586500051230-836e79a2b353?ixlib=rb-4.0.3&auto=format&fit=crop&w=2067&q=80");
    background-size: cover;
    background-position: center;
    color: #fff; /* White text for contrast */
    font-family: 'Noto Sans JP', sans-serif; /* Good for Japanese text */
}

/* Make the main container slightly translucent */
[data-testid="stAppViewContainer"] {
    background-color: rgba(0,0,0,0.4) !important;
    padding: 2rem;
    border-radius: 1rem;
}

/* Style the sidebar (optional) */
[data-testid="stSidebar"] {
    background-color: rgba(0,0,0,0.7) !important;
}

/* Heading styles */
h1, h2, h3, h4 {
    font-family: 'Noto Serif JP', serif;
    font-weight: 500;
    color: #fffae6;
    text-shadow: 1px 1px 2px #000;
}

/* Input fields style */
label {
    font-size: 1.1rem;
    color: #fffae6;
}

/* Buttons */
.stButton button {
    background-color: #6B2E5F !important; /* Deep purple/pink-ish color */
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

# ---------- APPLICATION TITLE ----------
st.title("高級温泉旅館 料金計算システム")
st.markdown("Welcome to our high-end Japanese hotel pricing calculator. Please input your room rates, discounts, and meal options below.")

# ---------- HELPER FUNCTIONS ----------
def parse_price(input_str):
    """
    Attempt to parse a free-text yen input (e.g., '¥30,000' or '30000').
    Returns a numeric value (float) or 0 if parsing fails.
    """
    # Remove any Yen symbols, commas, spaces, etc.
    cleaned = input_str.replace("¥", "").replace(",", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return 0.0

def parse_discount(input_str):
    """
    Parse a discount input, which could be '10%' or '¥2000' or '2000'.
    Returns a tuple: (is_percentage, value)
      - is_percentage = True if it's a '%' discount
      - value = numeric discount amount (e.g., 10.0, 2000.0)
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
    If discount is percentage, calculates base_price * (discount/100).
    If discount is absolute yen, subtracts discount.
    Returns the final price after discount (or the original base_price if error).
    """
    (is_percent, val) = parse_discount(discount_str)
    if is_percent:
        # val is the percent
        discounted_price = base_price - (base_price * (val / 100.0))
        return discounted_price if discounted_price > 0 else 0
    else:
        # val is a currency amount
        discounted_price = base_price - val
        return discounted_price if discounted_price > 0 else 0

# ---------- UI LAYOUT ----------
# We’ll split the UI into 3 main sections (Adults, Children, Summary).
# For a more refined look, we can use columns or expanders.

st.subheader("1. 大人料金 / Adult Room Price")
col1, col2 = st.columns(2)
with col1:
    adult_price_str = st.text_input("大人1名あたりの客室料金 (税込)", value="30000")
with col2:
    adult_discount_str = st.text_input("大人向け割引 (例: '10%' or '¥2000')", value="10%")
num_adults = st.number_input("大人の人数", min_value=1, value=2)

st.subheader("2. 子供料金 / Children Room Price")
col3, col4 = st.columns(2)
with col3:
    child_price_str = st.text_input("子供1名あたりの客室料金 (税込)", value="15000")
with col4:
    child_discount_str = st.text_input("子供向け割引 (例: '5%' or '¥1000')", value="5%")
num_children = st.number_input("子供の人数", min_value=0, value=1)

st.subheader("3. 食事オプション / Meals")
col5, col6 = st.columns(2)
with col5:
    breakfast_price_str = st.text_input("朝食オプション (1名あたり)", value="3000")
with col6:
    dinner_price_str = st.text_input("夕食オプション (1名あたり)", value="5000")

# ---------- CALCULATIONS ----------
btn_calculate = st.button("料金を計算する")  # "Calculate Price"
if btn_calculate:
    # Parse numeric values
    base_adult_price = parse_price(adult_price_str)
    base_child_price = parse_price(child_price_str)
    breakfast_price = parse_price(breakfast_price_str)
    dinner_price = parse_price(dinner_price_str)

    # Apply discounts
    final_adult_price = apply_discount(base_adult_price, adult_discount_str)
    final_child_price = apply_discount(base_child_price, child_discount_str)

    # Calculate totals
    total_adult_cost = final_adult_price * num_adults
    total_child_cost = final_child_price * num_children

    # Meal costs:
    # Assumption: Breakfast and dinner prices are also "per person" (adult or child).
    total_meal_cost = 0
    total_guests = num_adults + num_children
    if total_guests > 0:
        total_meal_cost = (breakfast_price + dinner_price) * total_guests

    grand_total = total_adult_cost + total_child_cost + total_meal_cost

    # Per-person cost (optional)
    cost_per_person = grand_total / total_guests if total_guests else 0

    # ---------- OUTPUT DISPLAY ----------
    st.markdown("---")
    st.subheader("料金明細 / Summary")
    
    st.write(f"**大人の合計**: ¥{int(total_adult_cost):,} ( {int(final_adult_price):,} 円 × {num_adults}名 )")
    st.write(f"**子供の合計**: ¥{int(total_child_cost):,} ( {int(final_child_price):,} 円 × {num_children}名 )")
    st.write(f"**食事オプションの合計**: ¥{int(total_meal_cost):,} ( {int(breakfast_price + dinner_price):,} 円 × {total_guests}名 )")
    
    st.markdown(f"## **合計金額: ¥{int(grand_total):,}**")
    st.write(f"**1人あたりの料金**: ¥{int(cost_per_person):,} （{total_guests}名で割り勘）")
    st.balloons()  # A Streamlit fun effect
