import csv
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =================================================================================
# National solid waste management dataset from EPA
# https://edg.epa.gov/metadata/catalog/search/resource/details.page?uuid=C9310A5s-16D2-4002-B36B-2B0A1C637D4E
# Credit to Professor Matt Miller for initial conversion of the CSV to a dictionary 
# that could be visualized with the Plotly module.
# Further effort has been made to focus on data necessary for this project.
# =================================================================================

with open("National_MSW_total.csv", "r") as USmswOriginal_csv:
    reader = csv.DictReader(USmswOriginal_csv)

    USmswOriginal = {}

    # Select data to be included in the USmswOriginal{}
    for row in reader:
        if "Materials" in row:

            # Skip footer description rows in the CSV
            if row["Materials"] != "" and "Table 1" not in row["Materials"]:
                for year in row:

                    # Read and create keys with year values from the first row
                    if year != "Materials":

                        # Take only data from 2010
                        if int(year) >= 2010:
                            if year not in USmswOriginal:
                                USmswOriginal[year] = {"year": year}

                            # Add corresponding materials as keys and their values to each year
                            USmswOriginal[year][row["Materials"]] = row[year]

    #print(USmswOriginal)

    # Calculate percentage and write to new file
    for year in USmswOriginal:
        year_total = int(USmswOriginal[year]["Total MSW Generated - Weight"])

        paper_pt = int(USmswOriginal[year]["Products - Paper and Paperboard"])/year_total*100
        USmswOriginal[year]["Products - Paper and Paperboard"] = paper_pt

        glass_pt = int(USmswOriginal[year]["Products - Glass"])/year_total*100
        USmswOriginal[year]["Products - Glass"] = glass_pt

        metal_pt = int(USmswOriginal[year]["Products - Metals - Total"])/year_total*100
        USmswOriginal[year]["Products - Metals - Total"] = metal_pt

        plastic_pt = int(USmswOriginal[year]["Products - Plastics"])/year_total*100
        USmswOriginal[year]["Products - Plastics"] = plastic_pt

        notRecycled_pt = 100-paper_pt-glass_pt-metal_pt-plastic_pt
        USmswOriginal[year]["Non-Recyclable & Others"] = notRecycled_pt

    # Remove unwanted data
    for year in USmswOriginal:
        for p in ["Products - Metals - Ferrous", "Products - Metals - Aluminum",
                  "Products - Metals - OtherNonferrous", "Products - Rubber and Leather",
                  "Products - Textiles", "Products - Wood", "Products - Other",
                  "Products - Total Materials", "Other Wastes - Food Waste",
                  "Other Wastes - Yard Trimmings", "Other Wastes - Miscellaneous Inorganic Wastes",
                  "Other Wastes - Total", "Total MSW Generated - Weight"]:
            USmswOriginal[year].pop(p)

    # Write to new csv for plotly
    with open("USmswTotal_p.csv", "w") as outfile:

        # Create a list of keys from any of the years for headers
        fieldnames = list(USmswOriginal["2010"])
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        # Populate data in rows
        for year in USmswOriginal:
            writer.writerow(USmswOriginal[year])

# Read new csv for building the bar chart
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
# NYC solid waste management dataset from NYC Open Data
# https://data.cityofnewyork.us/City-Government/DSNY-Monthly-Tonnage-Data/ebb7-mvp5
# =================================================================================

NYCmswOriginal = pd.read_csv("DSNY_Monthly_Tonnage_Data.csv")

# Drop columns of borough information
rm_borough = ["BOROUGH", "COMMUNITYDISTRICT", "BOROUGH_ID"]
for rm in rm_borough:
    NYCmswOriginal = NYCmswOriginal.drop(columns=rm)

# Remove month from date and create a year column
year = pd.to_datetime(NYCmswOriginal["MONTH"])
NYCmswOriginal["YEAR"] = year.dt.year
NYCmswOriginal = NYCmswOriginal.drop(columns="MONTH")

# Reorder columns so to have YEAR as the first column
cols = list(NYCmswOriginal.columns)
NYCmswOriginal = NYCmswOriginal[[cols[-1]] + cols[0:-1]]

# Get the sum of each type of MSW by year and output result as a new csv
nyc = NYCmswOriginal.groupby("YEAR").sum()
nyc.to_csv("NYCmswTotal_p.csv")

# Read new csv for further analysis
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
    title = "Comparing Municipal Recyclable and Waste Collection Rate of NYC with US",
    xaxis = dict(title_text = "Year"),
    yaxis = dict(title_text = "Percentage"),
    barmode = "stack",
)

# Sequence is important
groups = ["USpaper", "USplastic", "USmetal", "USglass", "USnon_recycle", "NYCpaper", "NYCmsw", "NYCnon_recycle"]
names = ["US PAPER", "US PLASTIC", "US METAL", "US GLASS", "US NON-RECYCLABLE", "NYC PAPER", "NYC PLASTIC", "NYC NON-RECYCLABLE"]
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
