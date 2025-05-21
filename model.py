
import os
import pandas as pd
from datetime import datetime

DATA_DIR = "data"

def log_measurement(cultivar, tree, cluster, fruitlet, size_mm, date=None):
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    entry = {
        "Date": date,
        "Cultivar": cultivar,
        "Tree": tree,
        "Cluster": cluster,
        "Fruitlet": fruitlet,
        "Size_mm": size_mm
    }

    path = os.path.join(DATA_DIR, f"{cultivar}_measurements.csv")
    if os.path.exists(path):
        df = pd.read_csv(path)
    else:
        df = pd.DataFrame(columns=entry.keys())

    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv(path, index=False)

    fruit_df = df[(df["Tree"] == tree) & (df["Cluster"] == cluster) & (df["Fruitlet"] == fruitlet)]
    if fruit_df["Date"].nunique() >= 2:
        sorted_df = fruit_df.sort_values("Date")
        growth = sorted_df["Size_mm"].iloc[-1] - sorted_df["Size_mm"].iloc[0]
        return f"Recorded. Growth: {growth:.1f} mm"
    return "Recorded. Awaiting second measurement."

def run_thinning_model(cultivar, tree, cluster):
    path = os.path.join(DATA_DIR, f"{cultivar}_measurements.csv")
    if not os.path.exists(path):
        return "No data found."

    df = pd.read_csv(path)
    cluster_df = df[(df["Tree"] == tree) & (df["Cluster"] == cluster)]
    growth_data = []

    for fid, group in cluster_df.groupby("Fruitlet"):
        if group["Date"].nunique() < 2:
            continue
        sorted_group = group.sort_values("Date")
        growth = sorted_group["Size_mm"].iloc[-1] - sorted_group["Size_mm"].iloc[0]
        growth_data.append((fid, growth))

    if len(growth_data) < 2:
        return "Not enough data for thinning model."

    growth_df = pd.DataFrame(growth_data, columns=["Fruitlet", "Growth"])
    top_growth = growth_df["Growth"].nlargest(max(1, int(len(growth_df) * 0.2))).mean()
    growth_df["Persist"] = growth_df["Growth"] >= 0.5 * top_growth

    n_total = len(growth_df)
    n_persist = growth_df["Persist"].sum()
    percent_abscise = 100 * (1 - n_persist / n_total)

    return f"{n_persist} of {n_total} fruitlets predicted to persist. Abscission rate: {percent_abscise:.1f}%"
