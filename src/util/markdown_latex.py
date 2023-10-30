import streamlit as st

npv_irr_payback = r"""
\begin{align*}
&\text{NPV}  = \sum \frac{CF_t}{(1 + r)^t} \\
&\text{IRR}  : 0 = \sum \frac{CF_t}{(1 + IRR)^t} \\
&\text{Payback Period}  = \text{Time taken for} \sum CF_t\ \text{to equal initial investment}\\
&\text{ROI}  = \frac{\text{Gain from Investment} - \text{Cost of Investment}}{\text{Cost of Investment}}
\end{align*}
"""

st.latex(r"")
analysis_description = """
**Given Cash Flow Data:**

- **NPV:** Reflects profitability considering the time value of money. Maximizes shareholder wealth.
- **IRR:** Indicates expected return rate, aiding in gauging relative project risks.
- **Payback Period:** Shows how quickly the initial investment is recovered, highlighting liquidity implications.
- **ROI:** Indicates the efficiency of an investment or project, highlighting the profitability of a company's investments.
"""

evaluation_description = """
While Net Present Value (NPV), Internal Rate of Return (IRR),
and Payback Period are standard metrics used in capital budgeting,
they have limitations when used in isolation to compare projects of different durations

**Limitations of traditional metrics:**
1. Net Present Value (NPV) Limitations:
    - It is not an annualized metric. Thus, a project with a higher NPV but longer duration might not necessarily be more beneficial than a shorter-duration project with a slightly lower NPV.
    
2. Internal Rate of Return (IRR) Limitations:
    - It doesn't account for the size of the investment. A smaller project might have a higher IRR but yield less total profit than a larger project with a slightly lower IRR.
3. Payback Period Limitations:
    - It doesn't account for the time value of money. A project with a shorter payback period might not necessarily be more beneficial than a longer-duration project with a slightly longer payback period.
    - It only indicates the time required to recover the initial investment, ignoring cash flows that occur after the payback period. A project might have a short payback period but low cash flows thereafter, whereas another with a longer payback period might yield substantial benefits in the long run
4. Return on Investment (ROI) Limitations:
    - It is not an annualized metric. Thus, a project with a higher ROI but longer duration might not necessarily be more beneficial than a shorter-duration project with a slightly lower ROI.
    - It doesn't account for the time value of money. A project with a higher ROI but longer duration might not necessarily be more beneficial than a shorter-duration project with a slightly lower ROI.
"""
