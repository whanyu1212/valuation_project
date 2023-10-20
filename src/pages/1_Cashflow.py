import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode
from streamlit_extras.colored_header import colored_header
from streamlit_extras.stylable_container import stylable_container
from streamlit_lottie import st_lottie

st.set_page_config(layout="wide")

st.lottie(
    "https://lottie.host/d377029b-f163-4e75-ac57-53ee2433b870/8v3sihrhak.json",
    height=300,
    width=600,
    speed=1,
    key="initial",
)
# * Side bar content
sidebar = st.sidebar
with sidebar:
    st.markdown("#### Planet Karaoke Pub Inputs:")
    st.text("")
    planet_investment_amount = st.slider(
        "Planet Karaoke Pub Initial Investment",
        770000,
        1000000,
        770000,
        key="planet_investment_amount",
    )
    st.text("")
    tax = st.slider("Tax rate", 0.0, 0.30, 0.3, key="tax")
    st.text("")
    patronage_loss = st.slider("Patronage Loss", 0.0, 0.25, 0.25, key="patronage_loss")
    st.text("")
    st.divider()
    st.markdown("#### Beach Karaoke Pub Inputs:")
    st.text("")
    beach_investment_amount = st.slider(
        "Beach Karaoke Pub Initial Investment",
        800000,
        1200000,
        800000,
        key="beach_investment_amount",
    )
##########################################################################################
# * Cash Flow for Planet Karaoke Pub

data = {
    "Year": [0, 1, 2, 3, 4],
    "Initial Investment": [-1 * planet_investment_amount, 0, 0, 0, 0],
    "Net Room Revenue": [0, 13200000, 13464000, 14137000, 14844000],
    "Rental Revenue": [
        0,
        170000 * 12,
        170000 * 12,
        170000 * 1.05 * 12,
        170000 * 1.05 * 12,
    ],
    "25% Patronage Rate": [0, 1650000, 1683000, 1767125, 1855500],
    "Repair/Maintenance Cost": [0, 10000, 10000, 10000, 10000],
    "Depreciation": [
        0,
        planet_investment_amount / 4,
        planet_investment_amount / 4,
        planet_investment_amount / 4,
        planet_investment_amount / 4,
    ],
}

# Create DataFrame
df = pd.DataFrame(
    data,
)

df["EBT"] = (
    df["Rental Revenue"]
    - df["Repair/Maintenance Cost"]
    - df["Depreciation"]
    - df["25% Patronage Rate"]
)

df["Net Income"] = df["EBT"] * (1 - tax)
df["Operating Cash Flow"] = df["Net Income"] + df["Depreciation"]


df_transposed = (
    df.T.iloc[1:, :]
    .set_axis(["Year 0", "Year 1", "Year 2", "Year 3", "Year 4"], axis=1)
    .assign(Category=df.columns.tolist()[1:])[
        ["Category", "Year 0", "Year 1", "Year 2", "Year 3", "Year 4"]
    ]
    # .style.format("{:,.0f}")
)


# * Cash Flow for Beach Karaoke Pub
data_1 = {
    "Year": [0, 1, 2, 3, 4, 5, 6],
    "Initial Investment (Renovation & Capital)": [
        -1 * beach_investment_amount - 900000,
        0,
        0,
        0,
        0,
        0,
        0,
    ],
    "Net Room Revenue": [0, 13200000, 13464000, 14137000, 14844000, 15140000, 15443000],
    "Sales Revenue": [
        0,
        4672000,
        4905600,
        5150880,
        5408424,
        5678845,
        5962537.25,
    ],
    "25% Patronage Rate": [0, 1650000, 1683000, 1767125, 1855500, 1892500, 1930375],
    "Food & Beverage Cost": [
        0,
        1168000,
        1226400,
        1287720,
        1352106,
        1419711.3,
        1490696.87,
    ],
    "Other Expenses": [
        0,
        1027840,
        1079232,
        1133192.6,
        1189853.3,
        1249345.9,
        1311813.24,
    ],
    "Repair/Maintenance Cost": [0, 10000, 10000, 10000, 10000, 10000, 10000],
    "Depreciation": [
        0,
        -1 * (-1 * beach_investment_amount - 900000) / 6,
        -1 * (-1 * beach_investment_amount - 900000) / 6,
        -1 * (-1 * beach_investment_amount - 900000) / 6,
        -1 * (-1 * beach_investment_amount - 900000) / 6,
        -1 * (-1 * beach_investment_amount - 900000) / 6,
        -1 * (-1 * beach_investment_amount - 900000) / 6,
    ],
}


df_1 = pd.DataFrame(
    data_1,
)

df_1["EBT"] = (
    df_1["Sales Revenue"]
    - df_1["Food & Beverage Cost"]
    - df_1["Other Expenses"]
    - df_1["25% Patronage Rate"]
    - df_1["Repair/Maintenance Cost"]
    - df_1["Depreciation"]
)


df_1_transposed = (
    df_1.T.iloc[1:, :]
    .set_axis(
        ["Year 0", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5", "Year 6"], axis=1
    )
    .assign(Category=df_1.columns.tolist()[1:])[
        [
            "Category",
            "Year 0",
            "Year 1",
            "Year 2",
            "Year 3",
            "Year 4",
            "Year 5",
            "Year 6",
        ]
    ]
)


c0, c1, c2 = st.columns([1, 1, 3])
with c0:
    with stylable_container(
        key="container_with_border",
        css_styles="""
                {   background-color: #ADD8E6;
                    color: white;
                    # border: 1px solid rgba(49, 51, 63, 0.2);
                    border-radius: 0.5rem;
                    padding: calc(1em - 1px);
                }
                """,
    ):
        st.markdown("##### Planet Karaoke Pub:")
gb = GridOptionsBuilder.from_dataframe(df_transposed)
gb.configure_column("Category", wrapText=True, autoHeight=True)
gb.configure_column(
    "Year 0",
    type=[
        "numericColumn",
        "numberColumnFilter",
        "customNumericFormat",
    ],
    # custom_currency_symbol="฿",
    precision=2,
)
gb.configure_column(
    "Year 1",
    type=[
        "numericColumn",
        "numberColumnFilter",
        "customNumericFormat",
    ],
    # custom_currency_symbol="฿",
    precision=2,
)
gb.configure_column(
    "Year 2",
    type=[
        "numericColumn",
        "numberColumnFilter",
    ],
    # custom_currency_symbol="฿",
    precision=2,
)
gb.configure_column(
    "Year 3",
    type=[
        "numericColumn",
        "numberColumnFilter",
        "customNumericFormat",
    ],
    # custom_currency_symbol="฿",
    precision=2,
)
gb.configure_column(
    "Year 4",
    type=[
        "numericColumn",
        "numberColumnFilter",
        "customNumericFormat",
    ],
    # custom_currency_symbol="฿",
    precision=2,
)
response = AgGrid(
    df_transposed,
    editable=True,
    gridOptions=gb.build(),
    data_return_mode="filtered_and_sorted",
    update_mode="no_update",
    fit_columns_on_grid_load=True,
    theme="alpine",
    allow_unsafe_jscode=True,
)
st.divider()

gb = GridOptionsBuilder.from_dataframe(df_1_transposed)
gb.configure_column("Category", width=300)
gb.configure_column(
    "Year 0",
    type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
    precision=2,
)
gb.configure_column(
    "Year 1",
    type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
    precision=2,
)
gb.configure_column(
    "Year 2",
    type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
    precision=2,
)
gb.configure_column(
    "Year 3",
    type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
    precision=2,
)
gb.configure_column(
    "Year 4",
    type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
    precision=2,
)
gb.configure_column(
    "Year 5",
    type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
    precision=2,
)
gb.configure_column(
    "Year 6",
    type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
    precision=2,
)

c0, c1, c2 = st.columns([1, 1, 3])
with c0:
    with stylable_container(
        key="container_with_border",
        css_styles="""
                {   background-color: #ADD8E6;
                    color: white;
                    # border: 1px solid rgba(49, 51, 63, 0.2);
                    border-radius: 0.5rem;
                    padding: calc(1em - 1px);
                }
                """,
    ):
        st.markdown("##### Beach Karaoke Pub:")
response_1 = AgGrid(
    df_1_transposed,
    editable=True,
    gridOptions=gb.build(),
    data_return_mode="filtered_and_sorted",
    update_mode="no_update",
    fit_columns_on_grid_load=True,
    theme="alpine",
    allow_unsafe_jscode=True,
)


##########################################################################################
