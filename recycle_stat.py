import csv
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =================================================================================
# Compare the NYC recycle collection rate with national rate
# Uses the two datasets (USmswTotal_p.csv and NYCmswTotal_p.csv) created in 
# recycle_stat_NY.py and recycle_stat_US.py.
# If running this script alone, please download the two new datasets from GitHub,
# and save them in the same directory with this script.
# =================================================================================

# =================================================================================
# US data
# =================================================================================

USmswTotal = pd.read_csv("USmswTotal_p.csv")

# Rename columns' name
USmswTotal.rename(columns={
    "year": "YEAR",
    "Products - Paper and Paperboard": "PAPER COLLECTED",
    "Products - Glass": "GLASS COLLECTED",
    "Products - Metals - Total": "METALS COLLECTED",
    "Products - Plastics": "PLASTICS COLLECTED",
    "Non-Recyclable & Others": "NON-RECYCLABLE & OTHERS"
}, inplace=True)

# Swap plastic and paper columns
cols = list(USmswTotal.columns)
a, b = cols.index("GLASS COLLECTED"), cols.index("PLASTICS COLLECTED")
cols[a], cols[b] = cols[b], cols[a]
USmswTotal = USmswTotal[cols]

# Selecting columns to compare
USp_cols = list(USmswTotal)
USp_cols.remove("YEAR")

# =================================================================================
# NYC data
# =================================================================================

NYCmswTotal = pd.read_csv("NYCmswTotal_p.csv")

# Keep only data from 2010
NYCmswTotal = NYCmswTotal[20:]
NYCmswTotal.reset_index(drop=True, inplace=True)

# 1) Calculate the total tonnage of MSW of each year
# 2) Calculate the percentage of each type of MSW

# Ignore year when doing sums across rows
NYCp_cols = list(NYCmswTotal)
NYCp_cols.remove("YEAR")

NYCmswTotal["MSW TOTAL"] = NYCmswTotal[NYCp_cols].sum(axis=1)
NYCmswTotal["PAPER COLLECTED"] = NYCmswTotal["PAPERTONSCOLLECTED"] / NYCmswTotal["MSW TOTAL"] * 100
NYCmswTotal["MGP COLLECTED"] = NYCmswTotal["MGPTONSCOLLECTED"] / NYCmswTotal["MSW TOTAL"] * 100
NYCmswTotal["NON-RECYCLABLE & OTHERS"] = 100 - NYCmswTotal["PAPER COLLECTED"] - NYCmswTotal["MGP COLLECTED"]

# =================================================================================
# Combine two stacked bar charts together by using subgroups.
# Based on Stackoverflow answer https://stackoverflow.com/a/65314442
# =================================================================================

USNY = pd.DataFrame(
    dict(
        year = NYCmswTotal["YEAR"][0:9].tolist(),
        USpaper = USmswTotal["PAPER COLLECTED"].tolist(),
        USplastic = USmswTotal["PLASTICS COLLECTED"].tolist(),
        USmetal = USmswTotal["METALS COLLECTED"].tolist(),
        USglass = USmswTotal["GLASS COLLECTED"].tolist(),
        USnon_recycle = USmswTotal["NON-RECYCLABLE & OTHERS"].tolist(),
        NYCpaper = NYCmswTotal["PAPER COLLECTED"][0:9].tolist(),
        NYCmsw = NYCmswTotal["MGP COLLECTED"][0:9].tolist(),
        NYCnon_recycle = NYCmswTotal["NON-RECYCLABLE & OTHERS"][0:9].tolist(),
    )
)

fig = go.Figure()

fig.update_layout(
    title = "Comparison of Municipal Recyclable and Waste Collection Rate of NYC and US, 2010-2018",
    xaxis = dict(title_text = "Year"),
    yaxis = dict(title_text = "Percentage"),
    barmode = "stack",
)

# Sequence is important
groups = ["USpaper", "USplastic", "USmetal", "USglass", "USnon_recycle", "NYCpaper", "NYCmsw", "NYCnon_recycle"]
names = ["US PAPER", "US PLASTIC", "US METAL", "US GLASS", "US NON-RECYCLABLE & OTHERS", "NYC PAPER", "NYC PLASTIC", "NYC NON-RECYCLABLE & OTHERS"]
colors = {"USpaper" : "#7AC142",
          "USplastic" : "#0093D0",
          "USglass" : "#46A7D1",
          "USmetal" : "#8BBCD1",
          "USnon_recycle" : "#FFA15A",
          "NYCpaper" : "#7AC142",
          "NYCmsw" : "#0093D0",
          "NYCnon_recycle" : "#FFA15A"}

repeat = len(USNY.year)

i = 0
for r,n,c in zip(groups,names,colors.values()):
    if i <= 4:
        fig.add_trace(
            go.Bar(x=[USNY.year, ["US"] * repeat], 
                   y=USNY[r], 
                   name=n, 
                   marker_color=c,
                   text=["%.1f%%" % n for n in USNY[r]],
                   marker_pattern_shape = ["."] * repeat,
                   marker_pattern_fgcolor = ["#ffffff"] * repeat,
                   marker_pattern_solidity = [0.05] * repeat
                   ),
        )
    else:
        fig.add_trace(
            go.Bar(x=[USNY.year, ["NYC"] * repeat], 
                   y=USNY[r], 
                   name=n, 
                   marker_color=c,
                   text=["%.1f%%" % n for n in USNY[r]],
                   ),
        )
    i += 1

fig.show()
