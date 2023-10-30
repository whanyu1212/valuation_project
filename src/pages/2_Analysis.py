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
from statistics import mean

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

# Calculate WACC
wacc = (1 - debt) * cost_of_equity + debt * interest_rate * (1 - tax)


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


# Compte NPV
planet_npv = compute_NPV(planet_cash_flow, wacc)
beach_npv = compute_NPV(beach_cash_flow, wacc)

# Compte IRR
planet_irr = compute_IRR(planet_cash_flow)
beach_irr = compute_IRR(beach_cash_flow)


# Compte Payback Period
planet_payback_period = compute_payback_period(planet_cash_flow)
beach_payback_period = compute_payback_period(beach_cash_flow)

# * NPV, IRR, Payback Period


st.subheader("Comparisons")


selected = pills("", ["NPV", "IRR", "Payback Period","ROI"], ["💲", "🔣", "💹", "💸"])

if selected == "NPV":
    plot_col1, plot_col2 = st.columns(2)
    with plot_col1:
        waterfall_fig = create_waterfall_chart(planet_cash_flow, wacc, "Planet Karaoke Pub")
        st.plotly_chart(waterfall_fig, use_container_width=True, theme="streamlit")

    with plot_col2:
        waterfall_fig = create_waterfall_chart(beach_cash_flow, wacc, "Beach Karaoke Pub")
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
        
if selected == "ROI":
    initial_investment = planet_cash_flow[0]

    planet_roi_each_year = []

    for i in range(1, len(planet_cash_flow)):
        roi = (planet_cash_flow[i] / abs(initial_investment)) * 100  # Using abs() to ensure the initial investment is positive
        planet_roi_each_year.append(roi)
    planet_mean_roi = mean(planet_roi_each_year)
    
    initial_investment = beach_cash_flow[0]

    beach_roi_each_year = []

    for i in range(1, len(beach_cash_flow)):
        roi = (beach_cash_flow[i] / abs(initial_investment)) * 100  # Using abs() to ensure the initial investment is positive
        beach_roi_each_year.append(roi)
        
    beach_mean_roi = mean(beach_roi_each_year)
    
    col1, col2 = st.columns(2)
    with col1:
        years = [f"Year {i}" for i in range(1, len(planet_roi_each_year) + 1)]

        # Creating the plot
        fig = go.Figure(data=[go.Line(x=years, y=planet_roi_each_year)])

        # Updating the layout
        fig.update_layout(title='ROI Trend for Planet Karaoke Pub',
                        xaxis_title='Year',
                        yaxis_title='ROI (%)')
        
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")
        
        years = [f"Year {i}" for i in range(1, len(beach_roi_each_year) + 1)]

        # Creating the plot
        fig2= go.Figure(data=[go.Line(x=years, y=beach_roi_each_year)])

        # Updating the layout
        fig2.update_layout(title='ROI Trend for Beach Karaoke Pub',
                        xaxis_title='Year',
                        yaxis_title='ROI (%)')
        
        st.plotly_chart(fig2, use_container_width=True, theme="streamlit")
        
    
    with col2:
        fig = go.Figure(
        go.Scatter(x=[0, 1], y=[0, 1], mode="markers", marker=dict(opacity=0))
        )

        fig.add_annotation(
            x=0.5,
            y=0.5,
            text=f"Planet Karaoke Pub<br>ROI: {planet_mean_roi}%",
            showarrow=False,
            font=dict(size=24),
        )
        fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=600
        # title="Comparison of Average ROI",
    )

        st.plotly_chart(fig, use_container_width=True, theme="streamlit")
        
        fig2 = go.Figure(
        go.Scatter(x=[0, 1], y=[0, 1], mode="markers", marker=dict(opacity=0))
        )

        fig2.add_annotation(
            x=0.5,
            y=0.5,
            text=f"Beach Karaoke Pub<br>ROI: {beach_mean_roi}%",
            showarrow=False,
            font=dict(size=24),
        )
        fig2.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        # title="Comparison of Average ROI",
    )

        st.plotly_chart(fig2, use_container_width=True, theme="streamlit")
        


