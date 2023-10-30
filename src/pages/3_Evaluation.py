import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from streamlit_extras.colored_header import colored_header
from streamlit_lottie import st_lottie
from util.markdown_latex import evaluation_description
from util.sidebar import generate_sidebar
from util.functions import (
    compute_NPV,
    compute_IRR,
    compute_payback_period,
    extend_cashflows_for_LCM,
    calculate_EAA,
    profitability_index,
)
from util.create_df import (
    compute_financials_planet,
    transpose_and_format_planet,
    compute_financials_beach,
    transpose_and_format_beach,
    normalize_values,
)
from statistics import mean

# st.set_page_config(layout="wide")
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

initial_investment = planet_cash_flow[0]

planet_roi_each_year = []

for i in range(1, len(planet_cash_flow)):
    roi = (
        planet_cash_flow[i] / abs(initial_investment)
    ) * 100  # Using abs() to ensure the initial investment is positive
    planet_roi_each_year.append(roi)
planet_mean_roi = mean(planet_roi_each_year)

initial_investment = beach_cash_flow[0]

beach_roi_each_year = []

for i in range(1, len(beach_cash_flow)):
    roi = (
        beach_cash_flow[i] / abs(initial_investment)
    ) * 100  # Using abs() to ensure the initial investment is positive
    beach_roi_each_year.append(roi)

beach_mean_roi = mean(beach_roi_each_year)


df_normalized = normalize_values(
    npv_A=planet_npv,
    npv_B=beach_npv,
    irr_A=planet_irr,
    irr_B=beach_irr,
    payback_A=planet_payback_period,
    payback_B=beach_payback_period,
    roi_A=planet_mean_roi,
    roi_B=beach_mean_roi,
)

df_long = df_normalized.melt(
    id_vars=["Project"],
    value_vars=["NPV", "IRR", "Payback", "ROI"],
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
st.subheader("Other Metrics to Consider")
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Sensitivity Analysis",
        "Least Common Multiple",
        "Equivalent Annual Annuity",
        "Profitability Index",
    ]
)

with tab1:
    wacc_values = np.linspace(0.05, 0.2, 100)  # WACC range from 5% to 20%
    npvs_project1 = []
    npvs_project2 = []

    # Compute NPV for each WACC for both projects
    for w in wacc_values:
        npvs_project1.append(compute_NPV(planet_cash_flow, w))
        npvs_project2.append(compute_NPV(beach_cash_flow, w))

    # Plot with Plotly for both projects
    fig = go.Figure()

    # Project 1 NPVs
    fig.add_trace(
        go.Scatter(
            x=wacc_values,
            y=npvs_project1,
            mode="lines+markers",
            name="Planet Karaoke Pub",
            line=dict(width=3, color="blue"),
        )
    )

    # Project 2 NPVs
    fig.add_trace(
        go.Scatter(
            x=wacc_values,
            y=npvs_project2,
            mode="lines+markers",
            name="Beach Karaoke Pub",
            line=dict(width=3, color="red"),
        )
    )

    fig.update_layout(
        title="NPV Sensitivity to WACC for Two Projects",
        xaxis_title="WACC",
        yaxis_title="Net Present Value (NPV)",
    )

    st.plotly_chart(fig, use_container_width=True, theme="streamlit")
    st.markdown(
        """
### Sensitivity of NPV to WACC: Interpretation

From the graph above, we can derive the following insights:

1. **Slope of the NPV curves**:
   - The steeper the slope of the NPV curve with respect to changes in WACC, the more sensitive the project's NPV is to those changes. 
   - In the provided chart, it appears that the NPV of **Beach Karaoke Pub** (red line) has a steeper slope compared to **Planet Karaoke Pub** (blue line). This indicates that **Beach Karaoke Pub's NPV is more sensitive to changes in WACC** than Planet Karaoke Pub's NPV.

2. **Implication of Sensitivity**:
   - A project's sensitivity to changes in WACC provides insights into its risk profile.
     - **Higher Sensitivity (Steeper Slope)**: If a project's NPV is highly sensitive to WACC changes, it implies that small changes in the project's cost of capital can result in significant fluctuations in its value. Such a project might be considered **more risky**, as its profitability is more susceptible to changes in the financing environment.
     - **Lower Sensitivity (Gentler Slope)**: Conversely, a project with a more gradual slope (i.e., less sensitivity to WACC) indicates that the project's value is relatively stable against changes in the cost of capital. This could be interpreted as the project being **less risky** in terms of its financing environment.

In conclusion, based on the provided graph, **Beach Karaoke Pub's NPV is more sensitive to changes in WACC** than Planet Karaoke Pub's NPV. This suggests that Beach Karaoke Pub might have a higher financial risk profile compared to Planet Karaoke Pub, given that its value is more susceptible to fluctuations in the cost of capital. On the other hand, Planet Karaoke demonstrates a more stable value proposition against changes in its financing conditions.
"""
    )

with tab2:
    extended_planet_cashflows = extend_cashflows_for_LCM(planet_cash_flow, 12)
    extended_beach_cashflows = extend_cashflows_for_LCM(beach_cash_flow, 12)

    planet_npv_extended = compute_NPV(extended_planet_cashflows, wacc)
    beach_npv_extended = compute_NPV(extended_beach_cashflows, wacc)

    df_long = pd.DataFrame(
        {
            "Project": [
                "Planet Karaoke Pub",
                "Planet Karaoke Pub",
                "Beach Karaoke Pub",
                "Beach Karaoke Pub",
            ],
            "NPV": [planet_npv, planet_npv_extended, beach_npv, beach_npv_extended],
            "Metric": ["Original", "Extended", "Original", "Extended"],
        }
    )

    fig = px.bar(
        df_long,
        x="Project",
        y="NPV",
        color="Metric",
        barmode="group",
        text="NPV",
        title="NPV for Both Projects",
    )
    st.plotly_chart(fig, use_container_width=True, theme="streamlit")
    st.markdown(
        """
**In conducting an LCM analysis** for projects with differing durations, 
we aim to provide a standardized comparison over a **common time horizon**. 
By extending the cash flows of each project to match the **LCM duration**, 
we essentially simulate multiple cycles of the project without repeating the initial investment. 
The extended cash flows allow us to calculate metrics like **NPV** over the same time frame, 
offering a more equitable basis for comparison. Based on the values calculated above,
we can see that **Beach Karaoke Pub** has a higher NPV than **Planet Karaoke Pub**.
"""
    )

with tab3:
    planet_eaa = calculate_EAA(planet_npv, wacc, 4)
    beach_eaa = calculate_EAA(beach_npv, wacc, 6)
    df_plot = pd.DataFrame(
        {
            "Project": ["Planet Karaoke Pub", "Beach Karaoke Pub"],
            "EAA": [planet_eaa, beach_eaa],
        }
    )

    fig = px.bar(
        df_plot,
        x="Project",
        y="EAA",
        text="EAA",
        color="Project",
        title="Equivalent Annual Annuity",
    )
    st.plotly_chart(fig, use_container_width=True, theme="streamlit")
    st.markdown(
        """By converting the net present value (NPV) of each project 
            into an equivalent annual amount, it's easier to compare them 
            on an "apples-to-apples" basis. The one with the higher EAA is
            seen as the more attractive investment option. However,
            it does not capture the risk profile of each project, and since it
            is a derived metric from NPV, it is also subject to the same limitations"""
    )
with tab4:
    planet_pi = profitability_index(planet_cash_flow, wacc)
    beach_pi = profitability_index(beach_cash_flow, wacc)
    fig = go.Figure(
        go.Scatter(x=[0, 1], y=[0, 1], mode="markers", marker=dict(opacity=0))
    )

    # Add annotations (numbers) for the PI of both projects
    fig.add_annotation(
        x=0.25,
        y=0.5,
        text=f"Planet Karaoke Pub<br>PI: {planet_pi}",
        showarrow=False,
        font=dict(size=24),
    )

    fig.add_annotation(
        x=0.75,
        y=0.5,
        text=f"Beach Karaoke Pub<br>PI: {beach_pi}",
        showarrow=False,
        font=dict(size=24),
    )

    # Update layout to hide axis and set title
    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        title="Comparison of Profitability Index (PI)",
    )

    st.plotly_chart(fig, use_container_width=True, theme="streamlit")

    st.text("")
    st.markdown(
        """The Profitability Index (PI) serves as a crucial indicator of a project's potential return
        in relation to its initial investment. Essentially, it quantifies the present value of future 
        cash flows per unit of investment, allowing us to gauge the relative value delivered by each project. 
        Based on the values calculated above, we can see that **Beach Karaoke Pub** has a slightly 
        higher PI than **Planet Karaoke Pub**. """
    )
