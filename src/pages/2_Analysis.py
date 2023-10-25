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
from util.markdown_latex import analysis_description, npv_irr_payback
from util.functions import compute_NPV, compute_IRR, compute_payback_period
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.lottie(
    "https://lottie.host/fd313525-130c-4793-9d88-da7bf8d56e5e/15ZGSc6gTA.json",
    height=300,
    width=600,
    speed=1,
    key="initial",
)

##########################################################################################
# * Side bar content
(
    planet_investment_amount,
    tax,
    patronage_loss_rate,
    beach_investment_amount,
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

planet_cash_flow = [df_transposed["Year 0"][0]] + df_transposed.iloc[-1:, 2:].values[
    0
].tolist()

beach_cash_flow = [df_1_transposed["Year 0"][0]] + df_1_transposed.iloc[-1:, 2:].values[
    0
].tolist()

# Compte NPV
planet_npv = compute_NPV(planet_cash_flow) / 1000000
beach_npv = compute_NPV(beach_cash_flow) / 1000000

# Compte IRR
planet_irr = compute_IRR(planet_cash_flow)
beach_irr = compute_IRR(beach_cash_flow)


# Compte Payback Period
planet_payback_period = compute_payback_period(planet_cash_flow)
beach_payback_period = compute_payback_period(beach_cash_flow)

# * NPV, IRR, Payback Period

df_plot = pd.DataFrame(
    {
        "Project": ["Planet Karaoke Pub", "Beach Karaoke Pub"],
        "NPV": [planet_npv, beach_npv],
        "IRR": [planet_irr, beach_irr],
        "Payback Period": [planet_payback_period, beach_payback_period],
    }
)


# import plotly.graph_objects as go

# Extracting data from dataframe
labels = df_plot.columns[1:].tolist()
planet_data = df_plot.iloc[0, 1:].tolist()
beach_data = df_plot.iloc[1, 1:].tolist()

# Create radar chart
fig = go.Figure()

# Add traces for each project
fig.add_trace(
    go.Scatterpolar(
        r=planet_data,
        theta=labels,
        fill="toself",
        name="Planet Karaoke Pub",
        line=dict(color="royalblue"),
        marker=dict(color="royalblue"),
    )
)

fig.add_trace(
    go.Scatterpolar(
        r=beach_data,
        theta=labels,
        fill="toself",
        name="Beach Karaoke Pub",
        line=dict(color="firebrick"),
        marker=dict(color="firebrick"),
    )
)

# Update layout for a custom theme
fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[
                0,
                max(max(planet_data), max(beach_data)) * 1.1,
            ],  # Setting maximum range to 110% of max data
        )
    ),
    showlegend=True,
)
fig.update_layout(height=600)
# Show the figure
st.plotly_chart(fig, use_container_width=True, theme="streamlit")
