import numpy as np
from scipy.optimize import fsolve


def compute_NPV(cash_flows, discount_rate):
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


def extend_cashflows_for_LCM(cash_flows, lcm_duration):
    """
    Extend cash flows for the LCM duration without repeating the initial investment.

    Parameters:
    - cash_flows (list): An array of cash flows where the index represents the time period (starting from 0).
    - lcm_duration (int): The LCM duration over which the project should be extended.

    Returns:
    - list: The extended cash flows over the LCM duration.
    """

    # Find out how many times the project needs to be repeated
    repetitions = lcm_duration // (len(cash_flows) - 1)

    # Extend the cash flows without the initial investment
    extended_cashflows = [cash_flows[0]]  # Include initial investment only once
    for _ in range(repetitions):
        extended_cashflows.extend(cash_flows[1:])

    return extended_cashflows


def calculate_EAA(npv, discount_rate, n):
    """
    Calculate the Effective Annual Annuity (EAA) based on the NPV of a project.

    Parameters:
    - npv (float): Net Present Value of the project's cash flows.
    - discount_rate (float): The discount rate used for NPV calculations (e.g., 0.05 for 5%).
    - n (int): The number of years or lifespan of the project.

    Returns:
    - float: The Effective Annual Annuity (EAA).
    """

    annuity_factor = discount_rate / (1 - (1 + discount_rate) ** -n)
    eaa = npv * annuity_factor

    return eaa


def profitability_index(cash_flows, discount_rate):
    """
    Compute the Profitability Index given an array of cash flows and a discount rate.

    Parameters:
    - cash_flows (list or array): An array of cash flows where the first value is the initial investment (negative),
      and the subsequent values are expected cash inflows.
    - discount_rate (float): Discount rate used to calculate the present value of future cash flows.

    Returns:
    - float: Profitability Index.
    """

    # Calculate the present value of each cash inflow
    discounted_cashflows = [
        cf / (1 + discount_rate) ** i for i, cf in enumerate(cash_flows)
    ]

    # The PV of expected future cash inflows is the sum of discounted cashflows minus the initial investment
    pv_cash_inflows = np.sum(discounted_cashflows) - cash_flows[0]

    return pv_cash_inflows / -cash_flows[0]
