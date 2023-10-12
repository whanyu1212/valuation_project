import streamlit as st
from streamlit_lottie import st_lottie

st.set_page_config(layout="wide")

st_lottie(
    "https://lottie.host/7cf4fc5c-ae1a-44d0-99ee-9eb9230341e8/6xXWRb5Zft.json",
    height=300,
    width=600,
    speed=1,
    # key="initial",
)
c30, c31, c32 = st.columns([0.1, 0.1, 3])

with c30:
    st.caption("")

    st.image(
        "./pictures/Financial-analysis-icon-Graphics-29052787-1-580x386.jpg", width=80
    )

with c32:
    st.title("Valuing Mutually Exclusive Capital Projects")

st = st.sidebar.title("Inputs")
