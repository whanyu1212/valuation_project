import pandas as pd
import streamlit as st
from annotated_text import annotated_text
from streamlit_extras.colored_header import colored_header
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stylable_container import stylable_container
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode
from streamlit_lottie import st_lottie
from util.markdown_latex import evaluation_description
from util.sidebar import generate_sidebar
from util.functions import compute_NPV, compute_IRR, compute_payback_period
from util.create_df import (
    compute_financials_planet,
    transpose_and_format_planet,
    compute_financials_beach,
    transpose_and_format_beach,
    normalize_values,
)
import plotly.graph_objects as go


st.set_page_config(layout="wide")
st_lottie(
    "https://lottie.host/40f2b045-cfe3-48c1-99fb-8d9d959fad39/HZEetoX5H1.json",
    height=300,
    width=600,
    speed=1,
    # key="initial",
)

colored_header(
    label="Evaluation & Recommendation",
    description="How to compare projects with different lifespan? Which project do we recommend?",
    color_name="gray-70",
)


(
    planet_investment_amount,
    tax,
    patronage_loss_rate,
    beach_investment_amount,
    debt,
    cost_of_equity,
    interest_rate,
) = generate_sidebar()

wacc = (1 - debt) * cost_of_equity + debt * interest_rate * (1 - tax)

df = compute_financials_planet(planet_investment_amount, tax)
df_transposed = transpose_and_format_planet(df)


# * Cash Flow for Beach Karaoke Pub
df_1 = compute_financials_beach(beach_investment_amount, tax)
df_1_transposed = transpose_and_format_beach(df_1)


planet_cash_flow = [df_transposed["Year 0"][0]] + df_transposed.iloc[-1:, 2:].values[
    0
].tolist()


beach_cash_flow = [df_1_transposed["Year 0"][0]] + df_1_transposed.iloc[-1:, 2:].values[
    0
].tolist()

# Compte NPV
planet_npv = compute_NPV(planet_cash_flow, wacc)
beach_npv = compute_NPV(beach_cash_flow, wacc)

# Compte IRR
planet_irr = compute_IRR(planet_cash_flow)
beach_irr = compute_IRR(beach_cash_flow)


# Compte Payback Period
planet_payback_period = compute_payback_period(planet_cash_flow)
beach_payback_period = compute_payback_period(beach_cash_flow)


df_normalized = normalize_values(
    npv_A=planet_npv,
    npv_B=beach_npv,
    irr_A=planet_irr,
    irr_B=beach_irr,
    payback_A=planet_payback_period,
    payback_B=beach_payback_period,
)

df_long = df_normalized.melt(
    id_vars=["Project"],
    value_vars=["NPV", "IRR", "Payback"],
    var_name="Metric",
    value_name="Value",
)

# Radar chart
categories = df.columns[1:].tolist()
fig = go.Figure()

# Loop through unique projects
for project in df_long["Project"].unique():
    subset = df_long[df_long["Project"] == project]
    fig.add_trace(
        go.Scatterpolar(
            r=subset["Value"].tolist(),
            theta=subset["Metric"].tolist(),
            fill="toself",
            name=project,
        )
    )

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 1.5])),
    showlegend=True,
    height=600,
)

st.plotly_chart(fig, use_container_width=True, theme="streamlit")

st.info(evaluation_description)
st.text("")
st.subheader("Complementary Metrics")
tab1, tab2, tab3 = st.tabs(
    ["Sensitivity Analysis", "Lowest Common Multiple", "Equivalent Annual Annuity"]
)
