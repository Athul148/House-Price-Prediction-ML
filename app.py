import streamlit as st
import pickle
import base64

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏠",
    layout="centered"
)

# ---------------- LOAD MODEL ---------------- #
model = pickle.load(open("reg_model.save", "rb"))
encoder = pickle.load(open("label_encoder.save", "rb"))

# ---------------- BACKGROUND IMAGE ---------------- #
def set_background(image_file):

    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()

    st.markdown(
        f"""
        <style>

        .stApp {{
            background-image:
            linear-gradient(rgba(0,0,0,0.7),
            rgba(0,0,0,0.7)),
            url("data:image/jpg;base64,{encoded}");

            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .main-container {{
            background: rgba(255,255,255,0.10);
            padding: 45px;
            border-radius: 25px;
            backdrop-filter: blur(15px);
            box-shadow: 0px 8px 35px rgba(0,0,0,0.4);
            margin-top: 30px;
        }}

        h1 {{
            text-align: center;
            color: white !important;
            font-size: 52px !important;
            font-weight: 800 !important;
            margin-bottom: 5px;
        }}

        .sub {{
            text-align: center;
            color: #E0E0E0;
            font-size: 18px;
            margin-bottom: 30px;
        }}

        label {{
            color: white !important;
            font-size: 17px !important;
            font-weight: 600 !important;
        }}

        .stTextInput>div>div>input {{
            background-color: rgba(255,255,255,0.92);
            border-radius: 12px;
            border: none;
            padding: 15px;
            font-size: 16px;
            color: black;
        }}

        .stSelectbox>div>div {{
            background-color: rgba(255,255,255,0.92);
            border-radius: 12px;
            color: black;
        }}

        div.stButton > button:first-child {{
            width: 100%;
            height: 58px;
            border-radius: 14px;
            border: none;
            background: linear-gradient(135deg,#ff512f,#dd2476);
            color: white;
            font-size: 22px;
            font-weight: bold;
            transition: 0.3s;
            margin-top: 20px;
        }}

        div.stButton > button:first-child:hover {{
            transform: scale(1.02);
            box-shadow: 0px 8px 25px rgba(221,36,118,0.5);
        }}

        .result {{
            background: linear-gradient(135deg,#00b09b,#96c93d);
            padding: 25px;
            border-radius: 18px;
            text-align: center;
            font-size: 30px;
            font-weight: bold;
            color: white;
            margin-top: 25px;
            animation: fade 0.7s ease-in;
        }}

        @keyframes fade {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0px);
            }}
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

# SET BACKGROUND
set_background("house.jpg")

# ---------------- TITLE ---------------- #
st.markdown(
    """
    <h1>🏠 HOUSE PRICE PREDICTION</h1>
    <div class="sub">
        Predict your dream home's value instantly
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- FORM ---------------- #
st.markdown('<div class="main-container">', unsafe_allow_html=True)

house = st.selectbox(
    "🏡 House Type",
    ["Villa", "Apartment", "Bungalow", "Townhouse"]
)

col1, col2 = st.columns(2)

with col1:
    area = st.text_input("📐 Area (sq.ft)")
    bedrooms = st.text_input("🛏 Bedrooms")
    age = st.text_input("🏗 House Age")

with col2:
    distance = st.text_input("🚗 Distance to City")
    crime = st.text_input("🚨 Crime Rate")
    floors = st.text_input("🏢 Floors")

predict = st.button("✨ Predict House Price")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- PREDICTION ---------------- #
if predict:

    try:

        house_encoded = encoder.transform([house])[0]

        features = [[
            house_encoded,
            float(area),
            int(bedrooms),
            int(age),
            float(distance),
            float(crime)
        ]]

        result = model.predict(features)

        st.markdown(
            f"""
            <div class="result">
                💰 Estimated Price <br><br>
                ₹ {result[0]:,.2f}
            </div>
            """,
            unsafe_allow_html=True
        )

    except:
        st.error("⚠ Please enter valid values in all fields")