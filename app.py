import streamlit as st
import google.generativeai as genai
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model_ai = genai.GenerativeModel("gemini-2.5-flash")
import streamlit as st
import joblib
import pandas as pd


st.set_page_config(
    page_title="Sustainify AI",
    page_icon="🌱",
    layout="wide"
)

model = joblib.load("models/electricity_model.pkl")


city_encoder = joblib.load("models/city_encoder.pkl")
company_encoder = joblib.load("models/company_encoder.pkl")
water_model = joblib.load("models/water_model.pkl")

# Sidebar
st.sidebar.title("🌱 Sustainify AI")

page = st.sidebar.radio(
    "Select Module",
    [
        "Home",
        "Electricity Prediction",
        "Water Prediction",
        "Carbon Footprint",
        "AI Sustainability Advisor"
    ]
)

# Home Page
if page == "Home":

    st.title("🌱 Sustainify AI")

    st.subheader("Predict • Analyze • Sustain")

    st.write("""
    Sustainify AI is a smart sustainability platform.

    It helps users:
    - ⚡ Predict Electricity Bills
    - 💧 Predict Water Consumption
    - 🌍 Calculate Carbon Footprint
    - 🤖 Get AI-powered Sustainability Tips
    """)

    st.markdown("---")

    st.header("Project Features")

    st.write("✔ Electricity Bill Prediction")
    st.write("✔ Water Consumption Prediction")
    st.write("✔ Carbon Footprint Calculator")
    st.write("✔ AI Sustainability Advisor")


elif page == "Electricity Prediction":

    st.title("⚡ Electricity Bill Prediction")

    st.write("Please enter your household details.")

    fan = st.number_input(
    "Number of Fans",
    min_value=0,
    max_value=20,
    value=1
)
    refrigerator = st.number_input(
    "Number of Refrigerators",
    min_value=0,
    max_value=10,
    value=1
)
    airconditioner = st.number_input(
    "Number of Air Conditioners",
    min_value=0,
    max_value=10,
    value=1
)
    television = st.number_input(
    "Number of Televisions",
    min_value=0,
    max_value=10,
    value=1
)
    monitor = st.number_input(
    "Number of Monitors",
    min_value=0,
    max_value=10,
    value=1
)
    motorpump = st.number_input(
    "Number of Motor Pumps",
    min_value=0,
    max_value=5,
    value=0
)


    month = st.selectbox(
        "Select Month",
        [1,2,3,4,5,6,7,8,9,10,11,12]
    )

    city = st.selectbox(
    "Select City",
    list(city_encoder.classes_)
)

    company = st.selectbox(
    "Select Electricity Company",
    list(company_encoder.classes_)
)

    monthlyhours = st.number_input("Monthly Usage Hours", min_value=0, value=150)

    tariff_rate = st.number_input("Tariff Rate (₹/unit)", min_value=0.0, value=8.0)

    if st.button("Predict Electricity Bill"):

    
     city_encoded = city_encoder.transform([city])[0]
    company_encoded = company_encoder.transform([company])[0]

    # Create input dataframe
    input_data = pd.DataFrame({
        "Fan":[fan],
        "Refrigerator":[refrigerator],
        "AirConditioner":[airconditioner],
        "Television":[television],
        "Monitor":[monitor],
        "MotorPump":[motorpump],
        "Month":[month],
        "City":[city_encoded],
        "Company":[company_encoded],
        "MonthlyHours":[monthlyhours],
        "TariffRate":[tariff_rate]
    })

    # Predict
    prediction = model.predict(input_data)[0]

    st.success(f"Predicted Electricity Bill: ₹ {prediction:.2f}")

    st.markdown("### 💡 Energy Saving Tips")
    if prediction > 5000:
      st.warning("""
    Your predicted electricity bill is high.

    Suggestions:
    - Reduce AC usage
    - Switch to LED bulbs
    - Turn off appliances when not in use
    """)
    else:
       st.success("""
    Great! Your electricity consumption is moderate.
    Keep following energy-efficient practices.
    """)
elif page == "Water Prediction":

 st.title("💧 Water Consumption Prediction")
    
st.write("Enter household water usage details.")

household = st.number_input(
        "Household ID",
        min_value=1,
        value=1
    )

bathroom = st.number_input(
        "Bathroom Water Usage (Litres)",
        min_value=0.0,
        value=100.0
    )

kitchen = st.number_input(
        "Kitchen Water Usage (Litres)",
        min_value=0.0,
        value=80.0
    )

laundry = st.number_input(
        "Laundry Water Usage (Litres)",
        min_value=0.0,
        value=60.0
    )

gardening = st.number_input(
        "Gardening Water Usage (Litres)",
        min_value=0.0,
        value=50.0
    )

day = st.number_input(
        "Day",
        min_value=1,
        max_value=31,
        value=1
    )

month_water = st.number_input(
        "Month",
        min_value=1,
        max_value=12,
        value=1
    )

year = st.number_input(
        "Year",
        min_value=2024,
        max_value=2035,
        value=2025
    )

if st.button("Predict Water Consumption"):

        input_df = pd.DataFrame({

            "Household_ID":[household],
            "Bathroom_Liters":[bathroom],
            "Kitchen_Liters":[kitchen],
            "Laundry_Liters":[laundry],
            "Gardening_Liters":[gardening],
            "Day":[day],
            "Month":[month_water],
            "Year":[year]

        })

        prediction = water_model.predict(input_df)[0]

        st.metric(
            "💧 Predicted Water Consumption",
            f"{prediction:.2f} Litres"
        )

        if prediction > 400:

            st.warning("⚠️ Water consumption is high. Try saving water.")

        else:

            st.success("✅ Water consumption is within the normal range.")


elif page == "Carbon Footprint":

    st.title("🌍 Carbon Footprint Calculator")

    st.write("Estimate your household carbon emissions.")

    electricity_bill = st.number_input(
        "Monthly Electricity Bill (₹)",
        min_value=0.0,
        value=1000.0
    )

    water_consumption = st.number_input(
        "Monthly Water Consumption (Litres)",
        min_value=0.0,
        value=5000.0
    )

    if st.button("Calculate Carbon Footprint"):

        # Approximate electricity units
        electricity_units = electricity_bill / 8

        # Emission factors
        electricity_emission = electricity_units * 0.82
        water_emission = (water_consumption / 1000) * 0.344

        total_emission = electricity_emission + water_emission

        trees_needed = total_emission / 21

        st.markdown("---")

        st.metric(
            "⚡ Electricity Units",
            f"{electricity_units:.2f} units"
        )

        st.metric(
            "🌍 Total CO₂ Emissions",
            f"{total_emission:.2f} kg CO₂"
        )

        st.metric(
            "🌳 Trees Needed to Offset",
            f"{trees_needed:.1f}"
        )

        st.subheader("♻ Sustainability Score")

        if total_emission < 100:

            st.success("Excellent 🌱")

        elif total_emission < 250:

            st.info("Good 😊")

        elif total_emission < 500:

            st.warning("Average ⚠")

        else:

            st.error("High Carbon Footprint ❌")

        st.subheader("💡 Eco Recommendations")

        if electricity_units > 250:
            st.write("• Reduce AC usage during peak hours.")
            st.write("• Replace bulbs with LEDs.")
            st.write("• Switch off unused appliances.")

        if water_consumption > 10000:
            st.write("• Fix leaking taps.")
            st.write("• Harvest rainwater.")
            st.write("• Reuse RO wastewater for cleaning.")

            if total_emission <= 100:
             st.write("🎉 Great job! Keep following sustainable practices.")
    elif page == "AI Sustainability Advisor":

     st.title("🤖 AI Sustainability Advisor")

    question = st.text_area(
        "Ask a sustainability question",
        placeholder="Example: How can I reduce my electricity bill?"
    )

    if st.button("Get AI Advice"):

        if question.strip() == "":
            st.warning("Please enter a question.")
        else:
            response = model_ai.generate_content(question)
            st.subheader("AI Recommendation")
            st.write(response.text)