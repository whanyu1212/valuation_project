import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode
from streamlit_extras.colored_header import colored_header
from streamlit_extras.stylable_container import stylable_container
from streamlit_lottie import st_lottie
from util.create_df import (
    compute_financials_planet,
    transpose_and_format_planet,
    compute_financials_beach,
    transpose_and_format_beach,
)
from util.sidebar import generate_sidebar

st.set_page_config(layout="wide")

# st.lottie(
#     "https://lottie.host/d377029b-f163-4e75-ac57-53ee2433b870/8v3sihrhak.json",
#     height=300,
#     width=800,
#     speed=1,
#     key="initial",
# )
# * Side bar content

# Generate the sidebar and get the values
(
    planet_investment_amount,
    tax,
    patronage_loss_rate,
    beach_investment_amount,
    debt,
    cost_of_equity,
    interest_rate,
) = generate_sidebar()
##########################################################################################
st.info("test")
st.text("")
##########################################################################################
# * Cash Flow for Planet Karaoke Pub

df = compute_financials_planet(planet_investment_amount, tax)
df_transposed = transpose_and_format_planet(df)


# * Cash Flow for Beach Karaoke Pub
df_1 = compute_financials_beach(beach_investment_amount, tax)


df_1_transposed = transpose_and_format_beach(df_1)


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
