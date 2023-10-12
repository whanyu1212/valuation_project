import streamlit as st
from streamlit_lottie import st_lottie
st.set_page_config(layout="wide")
st_lottie("https://lottie.host/05bd1305-2d92-4bfd-a7e8-f8c4a8873499/PcI1k0m71q.json", height=300, width=600, speed=1, key="initial")
c30, c31, c32 = st.columns([0.1, 0.02, 3])

with c30:

    st.caption("")

    st.image("./pictures/Financial-analysis-icon-Graphics-29052787-1-580x386.jpg", width=80)

with c32:

    st.title("Valuing Mutually Exclusive Capital Projects")

