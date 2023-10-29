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


st.info(evaluation_description)
st.text("")
st.subheader("Complementary Metrics")
tab1, tab2, tab3 = st.tabs(
    ["Sensitivity Analysis", "Lowest Common Multiple", "Equivalent Annual Annuity"]
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
