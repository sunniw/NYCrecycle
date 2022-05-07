# =================================================================================
# INFO-664-02 Programing for Cultural Heritage 22/SP - Sunni Wong
# Final Project: New York City Recyclable Collection 2010-2018
# Part 2: National Municipal Recyclable and Waste Collection Rate, 2010-2018
# Data set: National solid waste management dataset from EPA
# https://edg.epa.gov/metadata/catalog/search/resource/details.page?uuid=C9310A59-16D2-4002-B36B-2B0A1C637D4E
# =================================================================================

import plotly.express as px
import csv
import pandas as pd

# Credit to Professor Matt Miller for initial conversion of the EPA CSV file 
# to a dataset that works with the Plotly module.

with open("National_MSW_total.csv","r") as USmswOriginal_csv:
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
   
    # Find out total MSW weight before dropping irrelevant columns
    for year in USmswOriginal:
        year_total = int(USmswOriginal[year]["Total MSW Generated - Weight"])
        
        paper_pt = int(USmswOriginal[year]["Products - Paper and Paperboard"])
        USmswOriginal[year]["Products - Paper and Paperboard"] = paper_pt
        
        glass_pt = int(USmswOriginal[year]["Products - Glass"])
        USmswOriginal[year]["Products - Glass"] = glass_pt

        metal_pt = int(USmswOriginal[year]["Products - Metals - Total"])
        USmswOriginal[year]["Products - Metals - Total"] = metal_pt

        plastic_pt = int(USmswOriginal[year]["Products - Plastics"])
        USmswOriginal[year]["Products - Plastics"] = plastic_pt

        USmswOriginal[year]["Non-Recyclable & Others"] = year_total - paper_pt - glass_pt - metal_pt - plastic_pt

    # Remove unwanted data
    for year in USmswOriginal:
        for p in ["Products - Metals - Ferrous", "Products - Metals - Aluminum", 
        "Products - Metals - OtherNonferrous", "Products - Rubber and Leather", 
        "Products - Textiles", "Products - Wood", "Products - Other", 
        "Products - Total Materials", "Other Wastes - Food Waste", 
        "Other Wastes - Yard Trimmings", "Other Wastes - Miscellaneous Inorganic Wastes", 
        "Other Wastes - Total"]:
            USmswOriginal[year].pop(p)

    # Write to new csv for plotly
    with open("USmswTotal_p.csv","w") as outfile:
        
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
    "year":"YEAR", 
    "Products - Paper and Paperboard" : "PAPER COLLECTED",
    "Products - Glass" : "GLASS COLLECTED",
    "Products - Metals - Total": "METALS COLLECTED",
    "Products - Plastics" : "PLASTICS COLLECTED",
    "Non-Recyclable & Others" : "NON-RECYCLABLE & OTHERS",
    "Total MSW Generated - Weight" : "MSW TOTAL"
    }, inplace=True)


# Find out percentage of each material
USmswTotal["PAPER COLLECTED"] = USmswTotal["PAPER COLLECTED"] / USmswTotal["MSW TOTAL"]
USmswTotal["GLASS COLLECTED"] = USmswTotal["GLASS COLLECTED"] / USmswTotal["MSW TOTAL"]
USmswTotal["METALS COLLECTED"] = USmswTotal["METALS COLLECTED"] / USmswTotal["MSW TOTAL"]
USmswTotal["PLASTICS COLLECTED"] = USmswTotal["PLASTICS COLLECTED"] / USmswTotal["MSW TOTAL"]
USmswTotal["NON-RECYCLABLE & OTHERS"] = USmswTotal["NON-RECYCLABLE & OTHERS"] / USmswTotal["MSW TOTAL"]

# Swap plastic and paper columns
cols = list(USmswTotal.columns)
a, b = cols.index("GLASS COLLECTED"), cols.index("PLASTICS COLLECTED")
cols[a], cols[b] = cols[b], cols[a]
USmswTotal = USmswTotal[cols]

# Selecting columns to compare
USp_cols = list(USmswTotal)
USp_cols.remove("YEAR")
USp_cols.remove("MSW TOTAL")

# Show US bar chart
# Numbers presented as percentage with 2 decimal places
# Reversed legend order to adhere to bar chart order.

USbarcolor = {"PAPER COLLECTED" : "#7AC142",
              "PLASTICS COLLECTED" : "#0093D0",
              "GLASS COLLECTED" : "#46A7D1",
              "METAL COLLECTED" : "#8BBCD1",
              "NON-RECYCLABLE & OTHERS" : "#FFA15A"}

fig = px.bar(USmswTotal, 
        x="YEAR", 
        y=USp_cols, 
        labels={"value": "Percentage to Total MSW", "YEAR": "Year"}, 
        color_discrete_sequence = [*USbarcolor.values()],
        title="National Municipal Recyclable and Waste Collection Rate, 2010-2018",
        text_auto=".2%")

fig.update_layout(legend_traceorder="reversed",
                    legend_title="Types of Materials",
                    yaxis = dict(
                        tickmode = "array",
                        tickvals = [0,0.2,0.4,0.6,0.8,1],
                        ticktext = ["0", "20%", "40%", "60%", "80%", "100%"]
                  )
                  )

fig.show()