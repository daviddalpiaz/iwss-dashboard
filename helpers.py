import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess


def process_data(df):
    df = (
        # Remove data using "old" method
        df.query("method != 0")
        # Keep data with gc/L less than 3000000
        .query("sars_cov_2 < 3000000")
        # Ensure sample_collect_date is in datetime format
        .assign(sample_collect_date=lambda df: pd.to_datetime(df["sample_collect_date"]))
        # Ensure data sorted by date
        .sort_values("sample_collect_date")
        # Extract variables of interest
        [["sample_collect_date", "sars_cov_2"]]
    )

    return df


def plot_data(df):
    # Create figure and axes objects with a specific size (width, height)
    _, ax = plt.subplots(figsize=(12, 5))

    # Create scatter plot with smaller, "dodgerblue" points
    ax.scatter(df["sample_collect_date"], df["sars_cov_2"], color="dodgerblue", s=10)

    # Apply lowess smoother
    smoothed = lowess(df["sars_cov_2"], df["sample_collect_date"].map(datetime.toordinal), frac=0.1)

    # Convert smoothed x values back to datetime
    smoothed_dates = [datetime.fromordinal(int(x)) for x in smoothed[:, 0]]

    # Plot the smoother line in dark orange
    ax.plot(smoothed_dates, smoothed[:, 1], "darkorange")

    # Set the font properties for the x and y labels
    ax.set_xlabel("Sample Collection Date", labelpad=20)
    ax.set_ylabel("Gene Copies per Liter (gc/L)", labelpad=20)

    # Disable scientific notation
    ax.get_yaxis().get_major_formatter().set_scientific(False)

    # Generate major ticks at the start of every other month
    major_ticks = pd.date_range(
        start=min(df["sample_collect_date"]), end=max(df["sample_collect_date"]), freq="2MS"
    )

    # Generate minor ticks at the start of every month
    minor_ticks = pd.date_range(
        start=min(df["sample_collect_date"]), end=max(df["sample_collect_date"]), freq="MS"
    )

    # Set the x-ticks positions
    ax.set_xticks(major_ticks)
    ax.set_xticks(minor_ticks, minor=True)

    # Add a light grey, dashed grid
    ax.grid(color="lightgrey", linestyle="--", linewidth=0.5)

    # Rotate x-axis labels
    plt.xticks(rotation=45, ha="right")
