
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[1]
raw = pd.read_csv(BASE / "data" / "netflix_titles_raw.csv")

clean = raw.copy()
for col in clean.columns:
    if clean[col].dtype == object:
        clean[col] = clean[col].astype(str).str.strip().replace({"nan": pd.NA})

for col in ["director", "cast", "country", "rating"]:
    clean[col] = clean[col].fillna("Unknown")

clean["date_added"] = pd.to_datetime(clean["date_added"], errors="coerce")
clean["year_added"] = clean["date_added"].dt.year.astype("Int64")
clean["main_country"] = clean["country"].fillna("Unknown").str.split(",").str[0].str.strip()
clean["genre_main"] = clean["listed_in"].str.split(",").str[0].str.strip()

dur = clean["duration"].str.extract(r"(?P<duration_value>\d+)\s*(?P<duration_unit>\w+)")
clean["duration_value"] = pd.to_numeric(dur["duration_value"], errors="coerce").astype("Int64")
clean["duration_unit"] = dur["duration_unit"]

clean.to_csv(BASE / "data" / "netflix_titles_clean.csv", index=False)

titles_by_year = clean.dropna(subset=["year_added"]).groupby("year_added").size().reset_index(name="titles")
titles_by_year["year_added"] = titles_by_year["year_added"].astype(int)

plt.figure(figsize=(8, 5))
plt.plot(titles_by_year["year_added"], titles_by_year["titles"], marker="o")
plt.title("Titles added to Netflix by year")
plt.xlabel("Year added")
plt.ylabel("Number of titles")
plt.tight_layout()
plt.savefig(BASE / "visualizations" / "titles_by_year_added.png", dpi=200)
