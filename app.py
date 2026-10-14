import os
import requests
import streamlit as st

st.set_page_config(
    page_title="AutoLux | Car Price AI",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    :root { --line: rgba(148,163,184,.18); }
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp {
      background: radial-gradient(ellipse at 8% 0%,rgba(14,165,233,.15),transparent 34%),
      radial-gradient(ellipse at 95% 8%,rgba(139,92,246,.16),transparent 32%),
      linear-gradient(145deg,#070b13 0%,#0b1221 48%,#080d18 100%);
      color:#f3f7ff;
    }
    [data-testid="stHeader"] { background:rgba(8,13,24,.72); backdrop-filter:blur(14px); }
    [data-testid="stSidebar"] { background:linear-gradient(180deg,#101a2d,#0b1220); border-right:1px solid var(--line); }
    [data-testid="stSidebar"] * { color:#edf4ff; }
    .block-container { max-width:1320px; padding-top:2rem; padding-bottom:3rem; }
    .hero {
      padding:30px 32px; border:1px solid rgba(148,163,184,.22); border-radius:28px;
      background:radial-gradient(circle at 85% 25%,rgba(103,232,249,.19),transparent 28%),
      radial-gradient(circle at 70% 100%,rgba(167,139,250,.18),transparent 34%),
      linear-gradient(120deg,rgba(17,29,51,.96),rgba(15,23,42,.78));
      box-shadow:0 24px 80px rgba(0,0,0,.26); animation:riseIn .7s ease-out both; margin-bottom:24px;
    }
    .eyebrow { display:inline-flex; padding:7px 12px; border:1px solid rgba(103,232,249,.25);
      border-radius:999px; color:#a5f3fc; background:rgba(8,145,178,.12); font-size:12px;
      font-weight:700; letter-spacing:1.2px; text-transform:uppercase; }
    .hero-title { font-family:'Space Grotesk',sans-serif; font-size:clamp(2.2rem,4vw,3.8rem);
      line-height:1.05; font-weight:700; letter-spacing:-1.7px; margin:18px 0 12px; color:#f8fbff; }
    .gradient-text { background:linear-gradient(90deg,#67e8f9,#a5b4fc 55%,#c4b5fd);
      -webkit-background-clip:text; background-clip:text; color:transparent; }
    .hero-copy { max-width:660px; color:#b8c5da; font-size:1.02rem; line-height:1.7; }
    .hero-car { font-size:clamp(5rem,11vw,9rem); text-align:center;
      filter:drop-shadow(0 12px 25px rgba(103,232,249,.18)); animation:floatCar 4s ease-in-out infinite; }
    .section-heading { font-family:'Space Grotesk',sans-serif; font-size:1.35rem; font-weight:700;
      color:#f1f5ff; margin:10px 0 4px; }
    .section-sub { color:#98a8c2; font-size:.92rem; margin-bottom:18px; }
    .glass-card { padding:20px 22px; border-radius:20px; border:1px solid var(--line);
      background:linear-gradient(145deg,rgba(23,34,57,.82),rgba(13,21,37,.82));
      box-shadow:0 12px 34px rgba(0,0,0,.14); transition:transform .25s,border-color .25s,box-shadow .25s;
      animation:riseIn .55s ease-out both; }
    .glass-card:hover { transform:translateY(-3px); border-color:rgba(103,232,249,.35);
      box-shadow:0 18px 42px rgba(0,0,0,.22); }
    .metric-label { color:#a7b5cb; font-size:.83rem; font-weight:600; margin-bottom:8px; }
    .metric-value { font-family:'Space Grotesk',sans-serif; color:#f8fbff; font-size:1.55rem; font-weight:700; }
    .metric-icon { font-size:1.35rem; margin-bottom:12px; }
    .result-card { border:1px solid rgba(103,232,249,.36);
      background:radial-gradient(circle at 90% 0%,rgba(103,232,249,.16),transparent 35%),
      linear-gradient(135deg,rgba(15,45,62,.94),rgba(24,27,54,.94));
      border-radius:24px; padding:26px; box-shadow:0 18px 55px rgba(6,182,212,.10);
      animation:resultPop .45s ease-out both; }
    .result-kicker { color:#a5f3fc; font-size:.83rem; font-weight:700; text-transform:uppercase; letter-spacing:1.3px; }
    .result-price { font-family:'Space Grotesk',sans-serif; font-size:clamp(2rem,4vw,3.3rem);
      line-height:1.2; font-weight:700; color:#fff; margin:10px 0 8px; }
    .result-note { color:#b9c9dc; font-size:.9rem; }
    div[data-testid="stForm"] { background:rgba(15,23,42,.55); border:1px solid var(--line); border-radius:22px; padding:22px; }
    .stTextInput label,.stNumberInput label,.stSelectbox label { color:#dbeafe !important; font-weight:600 !important; }
    .stTextInput input,.stNumberInput input,.stSelectbox [data-baseweb="select"] > div { border-radius:12px !important; }
    .stButton > button,[data-testid="stFormSubmitButton"] > button {
      width:100%; min-height:48px; border:1px solid rgba(103,232,249,.42); border-radius:13px;
      color:#07111f; background:linear-gradient(100deg,#67e8f9,#a5b4fc); font-weight:800;
      transition:transform .2s,filter .2s,box-shadow .2s; box-shadow:0 8px 24px rgba(103,232,249,.13);
    }
    .stButton > button:hover,[data-testid="stFormSubmitButton"] > button:hover {
      transform:translateY(-2px); filter:brightness(1.08); box-shadow:0 12px 30px rgba(103,232,249,.22);
      color:#07111f; border-color:#a5f3fc;
    }
    div[data-testid="stAlert"] { border-radius:14px; }
    .footer { color:#7f91ad; font-size:.8rem; text-align:center; padding-top:28px; line-height:1.8; }
    @keyframes riseIn { from {opacity:0;transform:translateY(14px)} to {opacity:1;transform:translateY(0)} }
    @keyframes floatCar { 0%,100% {transform:translateY(0)} 50% {transform:translateY(-10px)} }
    @keyframes resultPop { from {opacity:0;transform:scale(.98) translateY(8px)} to {opacity:1;transform:scale(1) translateY(0)} }
    @media (prefers-reduced-motion:reduce) { *,*::before,*::after {animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important;} }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar settings
st.sidebar.markdown("## 🚘 AutoLux AI")
st.sidebar.caption("CAR VALUE INTELLIGENCE")
st.sidebar.markdown("---")
default_api_url = os.getenv("CAR_PRICE_API_URL", "http://127.0.0.1:8000/predict")
api_url = st.sidebar.text_input(
    "FastAPI prediction URL",
    value=default_api_url,
    help="Must match the port used by your FastAPI backend.",
)
st.sidebar.markdown(
    """
    <div style="padding:14px;border-radius:14px;background:rgba(103,232,249,.08);
    border:1px solid rgba(103,232,249,.18);font-size:13px;line-height:1.7;">
      <b style="color:#a5f3fc;">Quick setup</b><br>
      1. Start FastAPI in one terminal.<br>2. Start Streamlit in another.<br>
      3. Keep both terminals running.
    </div>
    """,
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")
st.sidebar.caption("Predictions depend on your model and training data.")

# Hero
hero_left, hero_right = st.columns([1.55, 0.75], vertical_alignment="center")
with hero_left:
    st.markdown(
        """
        <div class="hero">
          <div class="eyebrow">✦ SMART VALUATION · AI INSIGHTS</div>
          <div class="hero-title">Know your car's<br><span class="gradient-text">real potential.</span></div>
          <div class="hero-copy">Get an instant machine-learning estimate for a used car.
          Enter the vehicle details, run the prediction, and review the information sent to your API.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with hero_right:
    st.markdown(
        '<div class="hero-car">🚘</div><div style="text-align:center;color:#8da3c3;font-size:12px;letter-spacing:2px;">DATA IN · INSIGHT OUT</div>',
        unsafe_allow_html=True,
    )

# Overview cards
m1, m2, m3 = st.columns(3)
for col, icon, label, value in [
    (m1, "⚡", "PREDICTION", "Instant estimate"),
    (m2, "🧠", "ENGINE", "Random Forest"),
    (m3, "🔌", "CONNECTION", "FastAPI"),
]:
    with col:
        st.markdown(
            f'<div class="glass-card"><div class="metric-icon">{icon}</div>'
            f'<div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>',
            unsafe_allow_html=True,
        )

st.markdown('<div class="section-heading">🚗 Vehicle details</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-sub">Enter the car information. Field names and categories must match your training dataset.</div>',
    unsafe_allow_html=True,
)

# Input form
with st.form("car_prediction_form", clear_on_submit=False):
    col1, col2 = st.columns(2, gap="large")
    with col1:
        car_name = st.text_input("Car name", value="swift", placeholder="e.g. swift, i20, city")
        year = st.number_input("Manufacturing year", min_value=1990, max_value=2026, value=2016, step=1)
        present_price = st.number_input("Present price (in lakhs)", min_value=0.0, max_value=1000.0, value=4.70, step=0.10, format="%.2f")
        kms_driven = st.number_input("Kilometres driven", min_value=0, max_value=2_000_000, value=50000, step=1000)
    with col2:
        fuel_type = st.selectbox("Fuel type", ["Petrol", "Diesel", "CNG"])
        seller_type = st.selectbox("Seller type", ["Dealer", "Individual"])
        transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
        owner_label = st.selectbox("Previous owners", ["0 (First Owner)", "1 (Second Owner)", "3 (Third Owner)"])
        owner = int(owner_label.split()[0])
    submitted = st.form_submit_button("✨  Predict car price", use_container_width=True)

payload = {
    "Car_Name": str(car_name).strip().lower(),
    "Year": int(year),
    "Present_Price": float(present_price),
    "Kms_Driven": int(kms_driven),
    "Fuel_Type": str(fuel_type),
    "Seller_Type": str(seller_type),
    "Transmission": str(transmission),
    "Owner": int(owner),
}

with st.expander("🔍 Review request payload", expanded=False):
    st.caption("This is the JSON data sent to FastAPI.")
    st.json(payload)

if submitted:
    if not car_name.strip():
        st.error("Please enter a car name before predicting.")
    elif not api_url.strip():
        st.error("Enter your FastAPI prediction URL in the sidebar.")
    else:
        try:
            with st.spinner("Connecting to the prediction engine…"):
                response = requests.post(api_url.strip(), json=payload, timeout=30)

            if response.status_code == 200:
                try:
                    data = response.json()
                except ValueError:
                    st.error("The API returned a response that is not valid JSON.")
                    st.code(response.text)
                else:
                    # main.py returns PredictionResponse(prediction_price=price)
                    pred = data.get("prediction_price", data.get("prediction", data.get("predicted_price")))
                    if pred is None:
                        st.error("The API responded, but no recognized prediction field was found.")
                        st.caption("Expected a field named prediction_price, prediction, or predicted_price.")
                        st.json(data)
                    else:
                        try:
                            pred = float(pred)
                        except (TypeError, ValueError):
                            st.error("The prediction returned by the API is not a number.")
                            st.json(data)
                        else:
                            st.markdown(
                                f"""
                                <div class="result-card">
                                  <div class="result-kicker">✦ Your estimated selling price</div>
                                  <div class="result-price">₹ {pred:,.2f} lakhs</div>
                                  <div class="result-note">AI-generated estimate based on the details you entered.
                                  This is not a guaranteed market offer.</div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                            st.success("Prediction completed successfully.")
                            with st.expander("View full API response"):
                                st.json(data)
            else:
                st.error(f"API returned HTTP {response.status_code}.")
                st.caption("Check the backend and ensure the request matches schema.py.")
                try:
                    st.json(response.json())
                except ValueError:
                    st.code(response.text or "(The server returned an empty response.)")
        except requests.exceptions.Timeout:
            st.error("The prediction request timed out after 30 seconds.")
            st.info("Check whether FastAPI is running and whether the model is loading correctly.")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to FastAPI.")
            st.markdown(
                """
                - Start the backend in a separate terminal.
                - Confirm the port in the sidebar matches the backend port.
                - Open the backend's `/docs` page to verify it is running.
                """
            )
        except requests.exceptions.RequestException as exc:
            st.error("The request could not be completed.")
            st.code(str(exc))

st.markdown(
    '<div class="footer">BUILT FOR SMARTER CAR VALUATION · AUTOLUX AI<br>'
    'Estimates are model outputs, not a guarantee of resale value.</div>',
    unsafe_allow_html=True,
)
