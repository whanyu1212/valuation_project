import plotly.graph_objects as go


# def create_waterfall_chart(cash_flow, npv, project_name="Project"):
#     """
#     Create a waterfall chart given a list of cash flows.

#     Parameters:
#     - cash_flow (list): List of cash flows excluding the starting value (which is assumed to be 0).
#     - project_name (str): Name of the project for labeling purposes.

#     Returns:
#     - fig (go.Figure): Plotly Figure object with the waterfall chart.
#     """
#     start_value = 0
#     values = [start_value] + cash_flow
#     # end_value = sum(cash_flow)
#     end_value = npv
#     values.append(end_value)

#     # Names for each bar in the waterfall chart
#     labels = [
#         "Before investment",
#         *["Year {}".format(i) for i in range(len(cash_flow))],
#         "End of project",
#     ]

#     # Create the waterfall chart
#     fig = go.Figure(
#         go.Waterfall(
#             name=project_name,
#             orientation="v",
#             measure=["absolute"] + ["relative" for _ in cash_flow] + ["total"],
#             x=labels,
#             textposition="outside",
#             text=[f"${v}" for v in values],
#             y=values,
#             connector={"line": {"color": "rgb(63, 63, 63)"}},
#         )
#     )

#     fig.update_layout(title=project_name, height=600)
#     # You can also add additional formatting, titles, or other customizations here

#     return fig


def compute_discounted_cash_flow(cash_flow, discount_rate):
    """
    Compute the discounted cash flow for each period.

    Parameters:
    - cash_flow (list): List of cash flows, starting with the initial investment.
    - discount_rate (float): Annual discount rate in decimal form (e.g., 0.05 for 5%).

    Returns:
    - List of discounted cash flows.
    """
    discounted_cash_flows = [
        cash_flow[0]
    ]  # First cash flow (initial investment) is not discounted
    for i, cf in enumerate(cash_flow[1:]):
        dcf = cf / (1 + discount_rate) ** (i + 1)
        discounted_cash_flows.append(dcf)
    return discounted_cash_flows


def create_waterfall_chart(cash_flow, discount_rate, project_name="Project"):
    """
    Create a waterfall chart given a list of cash flows.

    Parameters:
    - cash_flow (list): List of cash flows starting with the initial investment (which is typically negative).
    - discount_rate (float): Annual discount rate in decimal form (e.g., 0.05 for 5%).
    - project_name (str): Name of the project for labeling purposes.

    Returns:
    - fig (go.Figure): Plotly Figure object with the waterfall chart.
    """
    discounted_cash_flows = compute_discounted_cash_flow(cash_flow, discount_rate)
    print(discounted_cash_flows)
    start_value = 0
    values = [start_value] + discounted_cash_flows
    end_value = sum(discounted_cash_flows)
    values.append(end_value)

    # Names for each bar in the waterfall chart
    labels = [
        "Before investment",
        *["Year {}".format(i) for i in range(len(cash_flow))],
        "End of project",
    ]

    # Create the waterfall chart
    fig = go.Figure(
        go.Waterfall(
            name=project_name,
            orientation="v",
            measure=["absolute"]
            + ["relative" for _ in discounted_cash_flows]
            + ["total"],
            x=labels,
            textposition="outside",
            text=[f"${v:.2f}" for v in values],  # formatting to 2 decimal places
            y=values,
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        )
    )

    fig.update_layout(title=project_name, height=600)
    # You can also add additional formatting, titles, or other customizations here

    return fig


def plot_irr_gauge(irr_value, project_name="Project"):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=irr_value * 100,
            number={"suffix": "%", "font": {"size": 40}},
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "IRR for {}".format(project_name), "font": {"size": 24}},
            gauge={
                "axis": {"range": [None, 30], "tickwidth": 1, "tickcolor": "darkblue"},
                "bar": {"color": "darkblue"},
                "bgcolor": "white",
                "borderwidth": 2,
                "bordercolor": "gray",
                "steps": [
                    {"range": [0, 10], "color": "cyan"},
                    {"range": [10, 20], "color": "royalblue"},
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": 11.5,
                },
            },
        )
    )
    fig.update_layout(font={"color": "darkblue", "family": "Arial"})
    return fig


def plot_payback_period(cashflows, project_name="Project"):
    # Calculate cumulative cash flows
    cumulative_cashflows = [sum(cashflows[: i + 1]) for i in range(len(cashflows))]

    # Determine payback period
    payback_period = None
    for i, val in enumerate(cumulative_cashflows):
        if val >= 0:
            payback_period = i
            break

    # Plotting
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=list(range(len(cashflows))),
            y=cumulative_cashflows,
            mode="lines+markers",
            name="Cumulative Cash Flow",
        )
    )

    # Highlight payback period
    if payback_period is not None:
        fig.add_shape(
            type="line",
            x0=payback_period,
            y0=0,
            x1=payback_period,
            y1=cumulative_cashflows[payback_period],
            line=dict(color="red", width=2),
            name="Payback Period",
        )
        fig.add_annotation(
            x=payback_period,
            y=cumulative_cashflows[payback_period] / 2,
            text=f"Payback at year {payback_period}",
            showarrow=True,
            arrowhead=4,
            ax=90,
            ay=-40,
        )

    fig.update_layout(
        title="Cumulative Cash Flow and Payback Period for {}".format(project_name),
        xaxis_title="Years",
        yaxis_title="Cumulative Cash Flow",
    )

    return fig
