import plotly.express as px
import csv
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
# 2) Calculate the percentage of each type of MSW

# Ignore year when doing sums across rows
NYCp_cols = list(NYCmswTotal)
NYCp_cols.remove("YEAR")

NYCmswTotal["MSW TOTAL"] = NYCmswTotal[NYCp_cols].sum(axis=1)
NYCmswTotal["PAPER COLLECTED"] = NYCmswTotal["PAPERTONSCOLLECTED"] / NYCmswTotal["MSW TOTAL"] * 100
NYCmswTotal["MSP COLLECTED"] = NYCmswTotal["MGPTONSCOLLECTED"] / NYCmswTotal["MSW TOTAL"] * 100
NYCmswTotal["NON-RECYCLED & OTHERS"] = 100 - NYCmswTotal["PAPER COLLECTED"] - NYCmswTotal["MSP COLLECTED"]

# Show NYC bar chart
fig = px.bar(NYCmswTotal, x="YEAR", y=["PAPER COLLECTED", "MSP COLLECTED", "NON-RECYCLED & OTHERS"])
fig.show()
