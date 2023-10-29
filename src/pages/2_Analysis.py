import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode
from streamlit_extras.colored_header import colored_header
from streamlit_extras.stylable_container import stylable_container
from streamlit_lottie import st_lottie
from streamlit_pills import pills
from util.create_df import (
    compute_financials_planet,
    transpose_and_format_planet,
    compute_financials_beach,
    transpose_and_format_beach,
)
from util.sidebar import generate_sidebar
from util.markdown_latex import analysis_description, npv_irr_payback
from util.functions import compute_NPV, compute_IRR, compute_payback_period
from util.charts import (
    create_waterfall_chart,
    plot_irr_gauge,
    plot_payback_period,
)

st.set_page_config(layout="wide")

# st.lottie(
#     "https://lottie.host/fd313525-130c-4793-9d88-da7bf8d56e5e/15ZGSc6gTA.json",
#     height=300,
#     width=600,
#     speed=1,
#     key="initial",
# )

##########################################################################################
# * Side bar content
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
# * Cash Flow for Planet Karaoke Pub

df = compute_financials_planet(planet_investment_amount, tax)
df_transposed = transpose_and_format_planet(df)


# * Cash Flow for Beach Karaoke Pub
df_1 = compute_financials_beach(beach_investment_amount, tax)
df_1_transposed = transpose_and_format_beach(df_1)
##########################################################################################

st.info(analysis_description)
st.text("")
st.markdown("###### Formula:")
st.latex(npv_irr_payback)
st.text("")
st.text("")
st.text("")

planet_cash_flow = [df_transposed["Year 0"][0]] + df_transposed.iloc[-1:, 2:].values[
    0
].tolist()


# planet_cash_flow = [ round(elem,2) for elem in planet_cash_flow ]

beach_cash_flow = [df_1_transposed["Year 0"][0]] + df_1_transposed.iloc[-1:, 2:].values[
    0
].tolist()


# beach_cash_flow = [ round(elem,2) for elem in beach_cash_flow ]

# Compte NPV
planet_npv = compute_NPV(planet_cash_flow)
beach_npv = compute_NPV(beach_cash_flow)

# Compte IRR
planet_irr = compute_IRR(planet_cash_flow)
beach_irr = compute_IRR(beach_cash_flow)


# Compte Payback Period
planet_payback_period = compute_payback_period(planet_cash_flow)
beach_payback_period = compute_payback_period(beach_cash_flow)

# * NPV, IRR, Payback Period


st.subheader("Comparisons")

# tab1, tab2, tab3, tab4 = st.tabs(["Cash Flow Trend", "NPV", "IRR", "Payback Period"])

selected = pills("", ["NPV", "IRR", "Payback Period"], ["💲", "🔣", "	💹"])

if selected == "NPV":
    plot_col1, plot_col2 = st.columns(2)
    with plot_col1:
        waterfall_fig = create_waterfall_chart(planet_cash_flow, 0.115, "Planet Karaoke Pub")
        st.plotly_chart(waterfall_fig, use_container_width=True, theme="streamlit")

    with plot_col2:
        waterfall_fig = create_waterfall_chart(beach_cash_flow, 0.115, "Beach Karaoke Pub")
        st.plotly_chart(waterfall_fig, use_container_width=True, theme="streamlit")


if selected == "IRR":
    plot_col1, plot_col2 = st.columns(2)
    with plot_col1:
        irr_fig = plot_irr_gauge(planet_irr, "Planet Karaoke Pub")
        st.plotly_chart(irr_fig, use_container_width=True, theme="streamlit")

    with plot_col2:
        irr_fig = plot_irr_gauge(beach_irr, "Beach Karaoke Pub")
        st.plotly_chart(irr_fig, use_container_width=True, theme="streamlit")

if selected == "Payback Period":
    plot_col1, plot_col2 = st.columns(2)
    with plot_col1:
        pp = plot_payback_period(planet_cash_flow, "Planet Karaoke Pub")
        st.plotly_chart(pp, use_container_width=True, theme="streamlit")

    with plot_col2:
        pp = plot_payback_period(beach_cash_flow, "Beach Karaoke Pub")
        st.plotly_chart(pp, use_container_width=True, theme="streamlit")
