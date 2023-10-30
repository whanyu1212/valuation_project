import pandas as pd


def compute_financials_planet(planet_investment_amount, tax):
    data = {
        "Year": [0, 1, 2, 3, 4],
        "Initial Investment": [-1 * planet_investment_amount, 0, 0, 0, 0],
        "Net Room Revenue": [0, 13200000, 13464000, 14137000, 14844000],
        "Rental Revenue": [
            0,
            170000 * 12,
            170000 * 12,
            170000 * 1.05 * 12,
            170000 * 1.05 * 12,
        ],
        "25% Patronage Rate": [0, 1650000, 1683000, 1767125, 1855500],
        "Repair/Maintenance Cost": [0, 10000, 10000, 10000, 10000],
        "Depreciation": [
            0,
            planet_investment_amount / 4,
            planet_investment_amount / 4,
            planet_investment_amount / 4,
            planet_investment_amount / 4,
        ],
    }

    # Create DataFrame
    df = pd.DataFrame(data)

    df["EBT"] = (
        df["Rental Revenue"]
        - df["Repair/Maintenance Cost"]
        - df["Depreciation"]
        - df["25% Patronage Rate"]
    )

    df["Net Income"] = df["EBT"] * (1 - tax)
    df["Operating Cash Flow"] = df["Net Income"] + df["Depreciation"]

    return df


def transpose_and_format_planet(df):
    df_transposed = (
        df.T.iloc[1:, :]
        .set_axis(["Year 0", "Year 1", "Year 2", "Year 3", "Year 4"], axis=1)
        .assign(Category=df.columns.tolist()[1:])[
            ["Category", "Year 0", "Year 1", "Year 2", "Year 3", "Year 4"]
        ]
        # .style.format("{:,.0f}")  # Uncomment if you wish to style the DataFrame
    )
    return df_transposed


def compute_financials_beach(beach_investment_amount, tax):
    data = {
        "Year": [0, 1, 2, 3, 4, 5, 6],
        "Initial Investment (Renovation & Capital)": [
            -1 * beach_investment_amount - 900000,
            0,
            0,
            0,
            0,
            0,
            0,
        ],
        "Net Room Revenue": [
            0,
            13200000,
            13464000,
            14137000,
            14844000,
            15140000,
            15443000,
        ],
        "Sales Revenue": [
            0,
            4672000,
            4905600,
            5150880,
            5408424,
            5678845,
            5962787.46,
        ],
        "25% Patronage Rate": [0, 1650000, 1683000, 1767125, 1855500, 1892500, 1930375],
        "Food & Beverage Cost": [
            0,
            1168000,
            1226400,
            1287720,
            1352106,
            1419711.3,
            1490696.87,
        ],
        "Other Expenses": [
            0,
            1027840,
            1079232,
            1133192.6,
            1189853.3,
            1249345.9,
            1311813.24,
        ],
        "Repair/Maintenance": [0, 10000, 10000, 10000, 10000, 10000, 10000],
        "Depreciation": [
            0,
            -1 * (-1 * beach_investment_amount - 900000) / 6,
            -1 * (-1 * beach_investment_amount - 900000) / 6,
            -1 * (-1 * beach_investment_amount - 900000) / 6,
            -1 * (-1 * beach_investment_amount - 900000) / 6,
            -1 * (-1 * beach_investment_amount - 900000) / 6,
            -1 * (-1 * beach_investment_amount - 900000) / 6,
        ],
    }

    df = pd.DataFrame(data)

    df["EBT"] = (
        df["Sales Revenue"]
        - df["Food & Beverage Cost"]
        - df["Other Expenses"]
        - df["25% Patronage Rate"]
        - df["Repair/Maintenance"]
        - df["Depreciation"]
    )

    df["Net Income"] = df["EBT"] * (1 - tax)
    df["Capital Expenditure"] = df["Depreciation"]
    df["Operating Cash Flow"] = (
        df["Net Income"] + df["Depreciation"] - df["Capital Expenditure"]
    )

    return df


def transpose_and_format_beach(df):
    df_transposed = (
        df.T.iloc[1:, :]
        .set_axis(
            ["Year 0", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5", "Year 6"],
            axis=1,
        )
        .assign(Category=df.columns.tolist()[1:])[
            [
                "Category",
                "Year 0",
                "Year 1",
                "Year 2",
                "Year 3",
                "Year 4",
                "Year 5",
                "Year 6",
            ]
        ]
    )
    return df_transposed


def normalize_values(npv_A, npv_B, irr_A, irr_B, payback_A, payback_B, roi_A, roi_B):
    # NPV and IRR normalization
    max_npv = max(npv_A, npv_B)
    max_irr = max(irr_A, irr_B)
    max_roi = max(roi_A, roi_B)

    normalized_npv_A = npv_A / max_npv
    normalized_npv_B = npv_B / max_npv

    normalized_irr_A = irr_A / max_irr
    normalized_irr_B = irr_B / max_irr

    normalized_roi_A = roi_A / max_roi
    normalized_roi_B = roi_B / max_roi

    # Payback normalization (inverse since lower is better)
    max_payback = max(payback_A, payback_B)

    normalized_payback_A = max_payback / payback_A
    normalized_payback_B = max_payback / payback_B

    # Create DataFrame to store values
    data = {
        "Project": ["Planet Karaoke Pub", "Beach Karaoke Pub"],
        "NPV": [normalized_npv_A, normalized_npv_B],
        "IRR": [normalized_irr_A, normalized_irr_B],
        "Payback": [normalized_payback_A, normalized_payback_B],
        "ROI": [normalized_roi_A, normalized_roi_B],
    }
    df = pd.DataFrame(data)

    return df
