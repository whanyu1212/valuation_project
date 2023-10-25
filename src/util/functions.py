import numpy as np
from scipy.optimize import fsolve


def compute_NPV(cash_flows, discount_rate=0.115):
    """
    Compute the NPV given an array of cash flows and a discount rate.

    Parameters:
    - cash_flows (list or array): An array of cash flows where the index represents the time period (starting from 0).
    - discount_rate (float): The discount rate as a fraction (e.g., 0.05 for 5%).

    Returns:
    - float: The computed NPV.
    """
    npv = cash_flows[0] + sum(
        [cf / (1 + discount_rate) ** t for t, cf in enumerate(cash_flows[1:], start=1)]
    )
    return npv


def compute_IRR(cash_flows):
    """
    Compute the IRR given an array of cash flows.

    Parameters:
    - cash_flows (list or array): An array of cash flows where the index represents the time period (starting from 0).

    Returns:
    - float: The computed IRR as a fraction (e.g., 0.05 for 5%).
    """

    # Define the NPV function with rate as the variable to solve for
    def npv(rate):
        discounted_cashflows = [cf / (1 + rate) ** i for i, cf in enumerate(cash_flows)]
        return np.sum(discounted_cashflows)

    # Use fsolve to find the root (IRR)
    irr = fsolve(npv, 0.1)[0]  # 0.1 is an initial guess
    return irr


def compute_payback_period(cash_flows):
    """
    Compute the payback period given an array of cash flows.

    Parameters:
    - cash_flows (list or array): An array of cash flows where the index represents the time period (starting from 0).

    Returns:
    - int: The payback period rounded to the nearest whole number.
    """
    initial_investment = abs(cash_flows[0])
    running_total = 0

    for i, cash_flow in enumerate(cash_flows[1:]):
        running_total += cash_flow
        if running_total >= initial_investment:
            # Return the year (i+1 since we started counting from 1)
            return i + 1
    # If payback period is not achieved within the given period
    return None
