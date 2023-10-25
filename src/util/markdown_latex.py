import streamlit as st

npv_irr_payback = r"""
\begin{align*}
&\text{NPV}  = \sum \frac{CF_t}{(1 + r)^t} \\
&\text{IRR}  : 0 = \sum \frac{CF_t}{(1 + IRR)^t} \\
&\text{Payback Period}  = \text{Time taken for} \sum CF_t\ \text{to equal initial investment}
\end{align*}
"""


analysis_description = """
**Given Cash Flow Data:**

- **NPV:** Reflects profitability considering the time value of money. Maximizes shareholder wealth.
- **IRR:** Indicates expected return rate, aiding in gauging relative project risks.
- **Payback Period:** Shows how quickly the initial investment is recovered, highlighting liquidity implications.
"""
