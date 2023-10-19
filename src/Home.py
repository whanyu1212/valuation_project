import pandas as pd
import streamlit as st
from annotated_text import annotated_text
from streamlit_extras.colored_header import colored_header
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stylable_container import stylable_container
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode
from streamlit_lottie import st_lottie

st.set_page_config(layout="wide")

# Global variables
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
    st.text("")

##########################################################################################


# Main page content for Home
# * Problem Statement
colored_header(
    label="Problem Statement",
    description="Which project to undertake? Lease or build?",
    color_name="gray-70",
)
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

st.text("")
st.text("")

##########################################################################################

# * Contextual Information
colored_header(
    label="Contextual Information",
    description="Which project to undertake? Lease or build?",
    color_name="gray-70",
)
st.text("")
st.text("")

# * Capital Structure
c0, c1, c2 = st.columns([0.9, 1, 4])
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
        st.markdown("##### Capital Structure:")
st.text("")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Debt Proportion", "25%", "")
col2.metric("Interest Rate", "10%", "")
col3.metric("Equity Proportion", "75%", "")
col4.metric("Cost of Equity", "12%", "")
col5.metric("Tax Rate", "30%", "")
style_metric_cards(border_left_color="#ADD8E6")
st.text("")
st.latex(
    r"""
    \text{WACC} = \frac{E}{V} * R_e + \frac{D}{V} * R_d * (1 - T_c)\\
    """
)
st.latex(r"""0.75 * 0.12 + 0.25 * 0.10 * (1 - 0.30) = 0.115""")
st.caption("Remark: We will be using WACC = 11.5% to discount the cash flows")
st.divider()

##########################################################################################
# * Options

c0, c1, c2 = st.columns([0.9, 1, 4])
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
        st.markdown("##### Project Details:")
st.text("")


project_details = {
    "Details": [
        "Life Span",
        "Upfront Investment",
        "Depreciation",
        "Repair and Maintenance Cost",
        "Expenses",
        "Annula Capital Expenditure",
    ],
    "Planet Karaoke Pub (Lease)": [
        "4 Years",
        "770,000 - 1,000,000 Baht",
        "Straight line depreciation with 0 salvage value",
        "10,000 Baht",
        "Pub will pay for all expenses",
        "N/A",
    ],
    "Beach Karaoke Pub (Build)": [
        "6 Years",
        "800,00 - 1,200,000 Baht",
        "Straight line depreciation with 0 salvage value",
        "10,000 Baht",
        "Food & Beverage: 25% of sales, Salaries: 16% of sales, Others: 22% of sales",
        "Equal to depreciation",
    ],
}
df = pd.DataFrame(project_details)
# st.dataframe(
#     pd.DataFrame(project_details).set_index("Details"), use_container_width=True
# )

gb = GridOptionsBuilder.from_dataframe(df)

gb.configure_column("Details", type=["textColumn", "textColumnFilter"], width=80)

cellsytle_jscode = JsCode(
    """
function(params) {
    return {
        'color': 'gray',
        'backgroundColor': 'white'
    }
};
"""
)
gb.configure_column("Details", cellStyle=cellsytle_jscode)

response = AgGrid(
    df,
    editable=True,
    gridOptions=gb.build(),
    data_return_mode="filtered_and_sorted",
    update_mode="no_update",
    fit_columns_on_grid_load=True,
    theme="alpine",
    allow_unsafe_jscode=True,
)
