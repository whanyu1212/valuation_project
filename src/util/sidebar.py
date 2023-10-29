import streamlit as st


def generate_sidebar():
    sidebar = st.sidebar
    with sidebar:
        c0, c1 = st.columns(2)

        with c0:
            tax = st.number_input("Tax Rate", min_value=0.0, max_value=1.0, value=0.3)
            debt = st.number_input(
                "Debt Proportion",
                min_value=0.0,
                max_value=1.0,
                value=0.25,
            )

            cost_of_equity = st.number_input(
                "Cost of Equity", min_value=0.0, max_value=1.0, value=0.08
            )

        with c1:
            patronage_loss = st.number_input(
                "Patronage Loss", min_value=0.0, max_value=1.0, value=0.25
            )

            interest_rate = st.number_input(
                "Interest Rate", min_value=0.0, max_value=1.0, value=0.05
            )
            st.text("")
        st.markdown("#### Planet Karaoke Pub Inputs:")
        st.text("")
        planet_investment_amount = st.slider(
            "Initial Investment",
            770000,
            1000000,
            770000,
            key="planet_investment_amount",
        )
        st.text("")
        st.text("")
        st.divider()
        st.markdown("#### Beach Karaoke Pub Inputs:")
        st.text("")
        beach_investment_amount = st.slider(
            "Initial Investment",
            800000,
            1200000,
            800000,
            key="beach_investment_amount",
        )

    return (
        planet_investment_amount,
        tax,
        patronage_loss,
        beach_investment_amount,
        debt,
        cost_of_equity,
        interest_rate,
    )
