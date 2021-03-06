# =================================================================================
# INFO-664-02 Programing for Cultural Heritage 22/SP - Sunni Wong
# Final Project: New York City Recyclable Collection 2010-2018
# Part 1: NYC Municipal Recyclable and Waste Collection Rate, 2010-2022
# Data set: DSNY Monthly Tonnage Data from NYC Open Data
# https://data.cityofnewyork.us/City-Government/DSNY-Monthly-Tonnage-Data/ebb7-mvp5
# =================================================================================

import plotly.express as px
import pandas as pd

# NYC solid waste management dataset from NYC Open Data
# https://data.cityofnewyork.us/City-Government/DSNY-Monthly-Tonnage-Data/ebb7-mvp5

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

# Get the sum of each type of MSW by year and output as a new csv
nyc = NYCmswOriginal.groupby("YEAR").sum()
nyc.to_csv("NYCmswTotal_p.csv")

# Read new csv for further analysis
NYCmswTotal = pd.read_csv("NYCmswTotal_p.csv")

# Keep only data from 2010
NYCmswTotal = NYCmswTotal[20:]
NYCmswTotal.reset_index(drop=True, inplace=True)

# 1) Calculate the total tonnage of MSW of each year
# 2) Calculate the percentage of each type of MSW in float number

# Ignore year when doing sums across rows
NYCp_cols = list(NYCmswTotal)
NYCp_cols.remove("YEAR")

# Calculate percentage and create bar chart

NYCmswTotal["MSW TOTAL"] = NYCmswTotal[NYCp_cols].sum(axis=1)
NYCmswTotal["PAPER COLLECTED"] = NYCmswTotal["PAPERTONSCOLLECTED"] / NYCmswTotal["MSW TOTAL"]
NYCmswTotal["MGP COLLECTED"] = NYCmswTotal["MGPTONSCOLLECTED"] / NYCmswTotal["MSW TOTAL"]
NYCmswTotal["NON-RECYCLABLE & OTHERS"] = 1 - NYCmswTotal["PAPER COLLECTED"] - NYCmswTotal["MGP COLLECTED"]

# Show NYC bar chart
# Numbers presented as percentage with 2 decimal places
# Reversed legend order to adhere to bar chart order.

fig = px.bar(NYCmswTotal, 
        x = "YEAR", 
        y = ["PAPER COLLECTED", "MGP COLLECTED", "NON-RECYCLABLE & OTHERS"], 
        color_discrete_sequence = ["#7AC142", "#0093D0", "#FFA15A"],
        title = "New York City Municipal Recyclable and Waste Collection Rate, 2010-2022",
        labels = {"value" : "Percentage to total waste", "YEAR" : "Year"}, 
        text_auto = ".2%")

fig.update_layout(legend_traceorder="reversed",
                    legend_title="Types of Materials",
                    yaxis = dict(
                        tickmode = "array",
                        tickvals = [0,0.2,0.4,0.6,0.8,1],
                        ticktext = ["0", "20%", "40%", "60%", "80%", "100%"]
                  )
                  )

fig.show()
