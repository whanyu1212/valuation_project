import pandas as pd
import streamlit as st
from annotated_text import annotated_text
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode
from streamlit_lottie import st_lottie

st.set_page_config(layout="wide")

st_lottie(
    "https://lottie.host/7cf4fc5c-ae1a-44d0-99ee-9eb9230341e8/6xXWRb5Zft.json",
    height=300,
    width=600,
    speed=1,
    # key="initial",
)
c0, c1, c2 = st.columns([0.1, 0.1, 3])

with c0:
    st.caption("")

    st.image(
        "./pictures/Financial-analysis-icon-Graphics-29052787-1-580x386.jpg", width=80
    )

with c2:
    st.title("Valuing Mutually Exclusive Capital Projects")

st.text("")
st.markdown("##### Problem Statement:")
annotated_text(
    "Phuket Beach Hotel is presented with a capital budgeting dilemma regarding\
    its unutilized space. Management is torn between",
    ("two investment opportunities", "", "#fea"),
    ": ",
    ("leasing the space", "", "#fea"),
    "to Planet Karaoke Pub \
    or",
    ("developing it into the hotel's own venture", "", "#fea"),
    "Beach Karaoke Pub. The decision requires a thorough \
    assessment of financial projections, potential profitability,\
    and strategic fit. Which option offers the most promising return\
    and aligns with the hotel's future vision?",
)

sidebar = st.sidebar.title("User Input")
with sidebar:
    tax = st.slider("Tax rate", 0.0, 0.20, 0.1)
    planet_investment_amount = st.slider(
        "Planet Investment Amount", 770000, 1000000, 770000
    )
    patronage_loss = st.slider("Patronage Loss", 0.0, 0.25, 0.1)
st.divider()
st.markdown("#### Project A: Planet Karaoke Pub")
data = {
    "Year": [0, 1, 2, 3, 4],
    "Initial Investment": [-1 * planet_investment_amount - 55000, 0, 0, 0, 0],
    "Net Room Revenue": [0, 13200000, 13464000, 14137000, 14844000],
    "Rental Revenue": [
        0,
        170000 * 12,
        170000 * 12,
        170000 * 1.05 * 12,
        170000 * 1.05 * 12,
    ],
    "Patronage Loss": [
        0,
        -1 * 13200000 * patronage_loss,
        -1 * 13464000 * patronage_loss,
        -1 * 14137000 * patronage_loss,
        -1 * 14844000 * patronage_loss,
    ],
    "Operating Expenses": [0, 100000, 100000, 100000, 100000],
    "Depreciation": [
        0,
        planet_investment_amount / 4,
        planet_investment_amount / 4,
        planet_investment_amount / 4,
        planet_investment_amount / 4,
    ],
}

# Create DataFrame
df = pd.DataFrame(data)

df["Net Rental Revene"] = df["Rental Revenue"] + df["Patronage Loss"]
df["EBT"] = df["Net Rental Revene"] - df["Depreciation"]
df["Net Income After Tax"] = df["EBT"] * (1 - 0.3)
df["Operating Cash Flow"] = df["Net Income After Tax"] + df["Depreciation"]
df["Discounted Cash Flow"] = df["Operating Cash Flow"] / (1 + 0.115) ** df["Year"]

df_transposed = (
    df.T.iloc[1:, :].set_axis(
        ["Year 0", "Year 1", "Year 2", "Year 3", "Year 4"], axis=1
    )
    # .style.format("{:,.0f}")
)
# Set 'Year' as the index
# df.set_index("Year", inplace=True)

st.dataframe(df_transposed, use_container_width=True)
