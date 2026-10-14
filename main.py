import os
import requests
import streamlit as st

# -------------------- PAGE --------------------
st.set_page_config(
    page_title="AutoLux | Car Price AI",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- THEME --------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    .stApp {
      background:
        radial-gradient(ellipse at 8% 0%, rgba(14,165,233,.14), transparent 35%),
        radial-gradient(ellipse at 95% 8%, rgba(139,92,246,.14), transparent 33%),
        linear-gradient(145deg,#070b13,#0b1221 52%,#080d18);
      color:#f3f7ff;
    }
    html,body,[class*="css"] { font-family:'DM Sans',sans-serif; }
    [data-testid="stHeader"] { background:rgba(8,13,24,.65); }
    [data-testid="stSidebar"] { background:linear-gradient(180deg,#101a2d,#0b1220); }
    [data-testid="stSidebar"] * { color:#edf4ff; }
    .block-container { max-width:1200px; padding-top:2rem; padding-bottom:3rem; }
    .hero {
      padding:30px; border:1px solid rgba(148,163,184,.22); border-radius:26px;
      background:linear-gradient(120deg,rgba(17,29,51,.96),rgba(15,23,42,.82));
      box-shadow:0 20px 65px rgba(0,0,0,.25); animation:rise .55s ease-out both;
    }
    .eyebrow { display:inline-block; padding:7px 12px; border:1px solid rgba(103,232,249,.28);
      border-radius:999px; color:#a5f3fc; background:rgba(8,145,178,.12);
      font-size:12px; font-weight:700; letter-spacing:1px; }
    .hero-title { font-family:'Space Grotesk',sans-serif; font-size:clamp(2.2rem,4vw,3.6rem);
      line-height:1.05; font-weight:700; letter-spacing:-1px; margin:18px 0 12px; color:#fff; }
    .gradient-text { background:linear-gradient(90deg,#67e8f9,#a5b4fc,#c4b5fd);
      -webkit-background-clip:text; background-clip:text; color:transparent; }
    .hero-copy { max-width:700px; color:#b8c5da; line-height:1.7; }
    .car-art { font-size:6rem; text-align:center; animation:float 3.5s ease-in-out infinite;
      filter:drop-shadow(0 12px 25px rgba(103,232,249,.18)); }
    .metric { padding:19px; border:1px solid rgba(148,163,184,.18); border-radius:18px;
      background:linear-gradient(145deg,rgba(23,34,57,.82),rgba(13,21,37,.82));
      transition:transform .2s,border-color .2s; animation:rise .5s ease-out both; }
    .metric:hover { transform:translateY(-3px); border-color:rgba(103,232,249,.4); }
    .metric-label { color:#a7b5cb; font-size:.8rem; font-weight:700; letter-spacing:.6px; }
    .metric-value { font-family:'Space Grotesk',sans-serif; color:#f8fbff; font-size:1.25rem; font-weight:700; margin-top:8px; }
    .result { padding:26px; border:1px solid rgba(103,232,249,.4); border-radius:22px;
      background:radial-gradient(circle at 90% 0%,rgba(103,232,249,.15),transparent 35%),
      linear-gradient(135deg,rgba(15,45,62,.94),rgba(24,27,54,.94)); animation:pop .35s ease-out both; }
    .result-label { color:#a5f3fc; font-size:.82rem; font-weight:700; letter-spacing:1px; text-transform:uppercase; }
    .result-price { font-family:'Space Grotesk',sans-serif; font-size:clamp(2rem,4vw,3rem);
      font-weight:700; color:white; margin:10px 0; }
    div[data-testid="stForm"] { background:rgba(15,23,42,.55); border:1px solid rgba(148,163,184,.18); border-radius:22px; padding:22px; }
    .stTextInput label,.stNumberInput label,.stSelectbox label { color:#dbeafe !important; font-weight:600 !important; }
    .stButton > button,[data-testid="stFormSubmitButton"] > button {
      border:1px solid rgba(103,232,249,.45); border-radius:12px; min-height:46px;
      background:linear-gradient(100deg,#67e8f9,#a5b4fc); color:#07111f; font-weight:800;
      transition:transform .2s,filter .2s; }
    .stButton > button:hover,[data-testid="stFormSubmitButton"] > button:hover {
      transform:translateY(-2px); filter:brightness(1.08); color:#07111f; }
    .footer { text-align:center; color:#8293ad; font-size:.8rem; padding-top:28px; line-height:1.8; }
    @keyframes rise { from{opacity:0;transform:translateY(12px)} to{opacity:1;transform:translateY(0)} }
    @keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-9px)} }
    @keyframes pop { from{opacity:0;transform:scale(.985)} to{opacity:1;transform:scale(1)} }
    @media (prefers-reduced-motion:reduce) { *,*::before,*::after { animation:none!important;transition:none!important; } }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- CONNECTION SETTINGS --------------------
st.sidebar.markdown("## 🚘 AutoLux AI")
st.sidebar.caption("CAR VALUE INTELLIGENCE")
st.sidebar.markdown("---")

# Set CAR_PRICE_API_URL in the environment to override this URL.
API_URL = os.getenv("CAR_PRICE_API_URL", "http://127.0.0.1:8000/predict").strip()
api_url = st.sidebar.text_input(
    "FastAPI prediction URL",
    value=API_URL,
    help="Must match the address and port used by Uvicorn.",
)
st.sidebar.caption("Backend URL is editable here.")
st.sidebar.markdown(
    """
    <div style="padding:13px;border-radius:13px;background:rgba(103,232,249,.08);
    border:1px solid rgba(103,232,249,.18);font-size:12px;line-height:1.7;">
    <b style="color:#a5f3fc;">Run in two terminals</b><br>
    Backend: <code>python -m uvicorn main:app --host 127.0.0.1 --port 8000</code><br>
    Frontend: <code>streamlit run app.py</code>
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------- HERO --------------------
left, right = st.columns([1.6, 0.65], vertical_alignment="center")
with left:
    st.markdown(
        """
        <div class="hero">
          <div class="eyebrow">✦ SMART VALUATION · AI INSIGHTS</div>
          <div class="hero-title">Know your car's<br><span class="gradient-text">real potential.</span></div>
          <div class="hero-copy">Estimate a used car's selling price using your trained machine-learning model.
          Enter the vehicle details and receive the result from your FastAPI backend.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with right:
    st.markdown('<div class="car-art">🚘</div><p style="text-align:center;color:#8da3c3;letter-spacing:2px;font-size:12px;">DATA IN · INSIGHT OUT</p>', unsafe_allow_html=True)

a, b, c = st.columns(3)
for col, icon, label, value in [
    (a, "⚡", "PREDICTION", "Instant estimate"),
    (b, "🧠", "MODEL", "Random Forest"),
    (c, "🔌", "BACKEND", "FastAPI"),
]:
    with col:
        st.markdown(
            f'<div class="metric"><div style="font-size:1.3rem">{icon}</div><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>',
            unsafe_allow_html=True,
        )

st.markdown('<h3 style="font-family:Space Grotesk,sans-serif;margin-top:25px;">🚗 Vehicle details</h3>', unsafe_allow_html=True)
st.caption("Enter values that match your training dataset.")

# -------------------- FORM --------------------
with st.form("car_form", clear_on_submit=False):
    lcol, rcol = st.columns(2, gap="large")
    with lcol:
        car_name = st.text_input("Car name", value="swift", placeholder="e.g. swift, i20, city")
        year = st.number_input("Manufacturing year", min_value=1990, max_value=2026, value=2016, step=1)
        present_price = st.number_input("Present price (in lakhs)", min_value=0.0, max_value=1000.0, value=4.70, step=0.10, format="%.2f")
        kms_driven = st.number_input("Kilometres driven", min_value=0, max_value=2_000_000, value=50000, step=1000)
    with rcol:
        fuel_type = st.selectbox("Fuel type", ["Petrol", "Diesel", "CNG"])
        seller_type = st.selectbox("Seller type", ["Dealer", "Individual"])
        transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
        owner_label = st.selectbox("Previous owners", ["0 (First Owner)", "1 (Second Owner)", "3 (Third Owner)"])
        owner = int(owner_label.split()[0])
    submitted = st.form_submit_button("✨  Predict car price", use_container_width=True)

payload = {
    "Car_Name": car_name.strip().lower(),
    "Year": int(year),
    "Present_Price": float(present_price),
    "Kms_Driven": int(kms_driven),
    "Fuel_Type": fuel_type,
    "Seller_Type": seller_type,
    "Transmission": transmission,
    "Owner": int(owner),
}

with st.expander("🔍 Review request payload", expanded=False):
    st.caption("This JSON is sent to the backend.")
    st.json(payload)

# -------------------- PREDICTION --------------------
if submitted:
    if not car_name.strip():
        st.error("Enter a car name first.")
    elif not api_url.strip():
        st.error("Enter the FastAPI URL in the sidebar.")
    else:
        try:
            with st.spinner("Contacting FastAPI and calculating estimate…"):
                # Do not assume the response key: inspect the actual JSON response.
                response = requests.post(api_url.strip(), json=payload, timeout=30)

            if response.ok:
                try:
                    result_data = response.json()
                except ValueError:
                    st.error("FastAPI returned a non-JSON response.")
                    st.code(response.text[:4000])
                else:
                    prediction = None
                    if isinstance(result_data, dict):
                        for key in ("prediction_price", "prediction", "predicted_price", "price"):
                            if key in result_data:
                                prediction = result_data[key]
                                break

                    if prediction is None:
                        st.error("Request reached FastAPI, but I could not find a price field in its response.")
                        st.write("Actual API response:")
                        st.json(result_data)
                    else:
                        try:
                            prediction = float(prediction)
                        except (ValueError, TypeError):
                            st.error("The price field returned by FastAPI is not numeric.")
                            st.json(result_data)
                        else:
                            st.markdown(
                                f'<div class="result"><div class="result-label">✦ Estimated selling price</div>'
                                f'<div class="result-price">₹ {prediction:,.2f} lakhs</div>'
                                f'<div style="color:#b9c9dc">AI estimate only — not a guaranteed market offer.</div></div>',
                                unsafe_allow_html=True,
                            )
                            st.success("Prediction completed.")
                            with st.expander("View API response"):
                                st.json(result_data)
            else:
                st.error(f"FastAPI returned HTTP {response.status_code}.")
                st.write("Response details:")
                try:
                    st.json(response.json())
                except ValueError:
                    st.code(response.text[:4000] or "(Empty response)")
        except requests.exceptions.ConnectionError as exc:
            st.error("Streamlit cannot connect to FastAPI.")
            st.markdown(
                """
                **Check these items:**
                1. Keep the FastAPI terminal running.
                2. Confirm the sidebar URL exactly matches the Uvicorn host and port.
                3. If Streamlit runs on another computer/container, `127.0.0.1` refers to that environment, not your backend computer.
                """
            )
            with st.expander("Connection error details"):
                st.code(str(exc))
        except requests.exceptions.Timeout:
            st.error("FastAPI did not respond within 30 seconds.")
            st.info("Check the backend terminal for model-loading or prediction errors.")
        except requests.exceptions.RequestException as exc:
            st.error("The HTTP request failed.")
            st.code(str(exc))

st.markdown('<div class="footer">AUTOLUX AI · SMARTER CAR VALUATION<br>Predictions depend on your trained model and data quality.</div>', unsafe_allow_html=True)
