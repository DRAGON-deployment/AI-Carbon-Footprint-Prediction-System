import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(
    page_title="Carbon Footprint Calculator",
    page_icon="🌱",
    layout="wide"
)

st.sidebar.title("Carbon Footprint Project")
st.sidebar.write("Dataset-based sustainability analysis system")
st.sidebar.write("Built using Python and Streamlit")

st.title("AI Carbon Footprint Future Prediction System 🌱")
st.write("Upload an Excel or CSV dataset to analyze carbon emissions and predict future output.")

uploaded_file = st.file_uploader(
    "Upload Carbon Footprint Dataset",
    type=["xlsx", "csv"]
)

if uploaded_file is None:
    st.info("Please upload your Excel or CSV file to start analysis.")
    st.stop()

if uploaded_file.name.endswith(".csv"):
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_excel(uploaded_file)

df.columns = df.columns.str.strip()

st.subheader("Uploaded Dataset")
st.dataframe(df)

required_columns = [
    "year",
    "car_km_per_week",
    "Flight_km_per_year",
    "Electricity_kWh_per_month",
    "Diet",
    "Lifestyle_Text"
]

missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    st.error(f"Missing columns in dataset: {missing_columns}")
    st.write("Your Excel file must contain these columns:")
    st.write(required_columns)
    st.stop()

CAR_EMISSION = 0.12
FLIGHT_EMISSION = 0.15
ELECTRICITY_EMISSION = 0.5

df["Car_Emission"] = df["car_km_per_week"] * 52 * CAR_EMISSION
df["Flight_Emission"] = df["Flight_km_per_year"] * FLIGHT_EMISSION
df["Electricity_Emission"] = df["Electricity_kWh_per_month"] * 12 * ELECTRICITY_EMISSION

def calculate_food_emission(diet):
    diet = str(diet).strip().lower()

    if "vegan" in diet:
        return 500
    elif "vegetarian" in diet and "non" not in diet:
        return 1000
    else:
        return 2000

df["Food_Emission"] = df["Diet"].apply(calculate_food_emission)

df["Total_Emission"] = (
    df["Car_Emission"] +
    df["Flight_Emission"] +
    df["Electricity_Emission"] +
    df["Food_Emission"]
)

st.subheader("Calculated Carbon Emissions")
st.dataframe(df)

st.subheader("Carbon Emission Summary")

average_emission = df["Total_Emission"].mean()
latest_emission = df["Total_Emission"].iloc[-1]

st.success(f"Average Carbon Emission: {average_emission:.2f} kg CO₂/year")
st.info(f"Latest Year Carbon Emission: {latest_emission:.2f} kg CO₂/year")

st.subheader("Emission Breakdown Chart")

breakdown_values = [
    df["Car_Emission"].mean(),
    df["Flight_Emission"].mean(),
    df["Electricity_Emission"].mean(),
    df["Food_Emission"].mean()
]

labels = ["Car", "Flight", "Electricity", "Food"]

fig, ax = plt.subplots()
ax.pie(breakdown_values, labels=labels, autopct="%1.1f%%")
ax.set_title("Average Carbon Emission Breakdown")
st.pyplot(fig)

st.subheader("Future Carbon Footprint Prediction")

X = df[["year"]]
y = df["Total_Emission"]

model = LinearRegression()
model.fit(X, y)

future_years = np.array([2025, 2026, 2027]).reshape(-1, 1)
future_predictions = model.predict(future_years)

future_df = pd.DataFrame({
    "Year": [2025, 2026, 2027],
    "Predicted_Carbon_Emission": future_predictions
})

st.dataframe(future_df)

st.subheader("Historical and Future Emission Trend")

fig2, ax2 = plt.subplots()
ax2.plot(df["year"], df["Total_Emission"], marker="o", label="Historical Emissions")
ax2.plot(future_df["Year"], future_df["Predicted_Carbon_Emission"], marker="o", label="Predicted Emissions")
ax2.set_xlabel("Year")
ax2.set_ylabel("Carbon Emission kg CO₂/year")
ax2.set_title("Carbon Footprint Future Prediction")
ax2.legend()
st.pyplot(fig2)

st.subheader("Unstructured Lifestyle Text Analysis")

df["Lifestyle_Text"] = df["Lifestyle_Text"].astype(str)

high_car_words = df["Lifestyle_Text"].str.contains("car|daily|frequently", case=False, na=False).sum()
high_energy_words = df["Lifestyle_Text"].str.contains("electricity|energy|high", case=False, na=False).sum()
flight_words = df["Lifestyle_Text"].str.contains("flight|flights|air", case=False, na=False).sum()

st.write(f"Rows mentioning car usage: {high_car_words}")
st.write(f"Rows mentioning high electricity/energy usage: {high_energy_words}")
st.write(f"Rows mentioning flights: {flight_words}")

st.subheader("Smart Sustainability Alerts 🔔")

avg_car = df["Car_Emission"].mean()
avg_flight = df["Flight_Emission"].mean()
avg_electricity = df["Electricity_Emission"].mean()

if avg_car > 2500:
    st.error("⚠ High car usage detected. Consider using public transportation or carpooling.")
elif avg_car > 1500:
    st.warning("🚗 Moderate car emissions detected. Reducing car travel can lower carbon footprint.")
else:
    st.success("✅ Transportation emissions are under control.")

if avg_flight > 2000:
    st.error("✈ High flight emissions detected. Try reducing air travel when possible.")
elif avg_flight > 1000:
    st.warning("✈ Moderate flight emissions detected.")
else:
    st.success("✅ Flight emissions are within sustainable range.")

if avg_electricity > 2500:
    st.error("⚡ High electricity consumption detected. Use energy-efficient appliances.")
elif avg_electricity > 1500:
    st.warning("⚡ Moderate electricity usage detected.")
else:
    st.success("✅ Electricity usage looks sustainable.")

st.subheader("Country Carbon Footprint Comparison 🌍")

country_data = {
    "Dataset Average": average_emission,
    "Germany Average": 7900,
    "World Average": 4700
}

fig3, ax3 = plt.subplots()
ax3.bar(country_data.keys(), country_data.values())
ax3.set_ylabel("Carbon Emission kg CO₂/year")
ax3.set_title("Dataset Average vs Country Averages")
st.pyplot(fig3)

st.subheader("Eco Sustainability Score 🌱")

if average_emission < 4000:
    eco_score = 90
    status = "Excellent Sustainability"
elif average_emission < 7000:
    eco_score = 70
    status = "Moderate Sustainability"
else:
    eco_score = 45
    status = "High Carbon Impact"

st.metric("Eco Score", f"{eco_score}/100")
st.write(f"Environmental Status: {status}")

st.subheader("Tree Plantation Equivalent 🌳")

trees_needed = average_emission / 21

st.info(
    f"Approximately {trees_needed:.0f} trees are needed to offset the average annual carbon emissions."
)

st.subheader("Project Summary")

st.write("""
This project analyzes semi-structured Excel/CSV data and unstructured lifestyle text to calculate carbon emissions.
It uses Machine Learning to predict future carbon footprint values and provides sustainability recommendations.
""")

st.success("Analysis completed successfully 🌱")
