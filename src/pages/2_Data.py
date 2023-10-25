import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode
from streamlit_extras.colored_header import colored_header
from streamlit_extras.stylable_container import stylable_container
from streamlit_lottie import st_lottie


st.set_page_config(layout="wide")

st.lottie(
    "https://lottie.host/fd313525-130c-4793-9d88-da7bf8d56e5e/15ZGSc6gTA.json",
    height=300,
    width=600,
    speed=1,
    key="initial",
)
