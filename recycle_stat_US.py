import plotly.express as px
import csv
import pandas as pd

# National solid waste management dataset from EPA
# https://edg.epa.gov/metadata/catalog/search/resource/details.page?uuid=C9310A59-16D2-4002-B36B-2B0A1C637D4E
# Credit to Professor Matt Miller for initial conversion of the EPA CSV file 
# to a dataset that works with the Plotly module.
# Further effort has been made on converting numbers to percentage,
# and to remove data that are out of the scope of this project.

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
   
    #print(USmswOriginal)

    # Calculate percentage and write to new file
    for year in USmswOriginal:
        year_total = int(USmswOriginal[year]["Total MSW Generated - Weight"])
        
        paper_pt = int(USmswOriginal[year]["Products - Paper and Paperboard"])/year_total
        USmswOriginal[year]["Products - Paper and Paperboard"] = paper_pt
        
        glass_pt = int(USmswOriginal[year]["Products - Glass"])/year_total
        USmswOriginal[year]["Products - Glass"] = glass_pt

        metal_pt = int(USmswOriginal[year]["Products - Metals - Total"])/year_total
        USmswOriginal[year]["Products - Metals - Total"] = metal_pt

        plastic_pt = int(USmswOriginal[year]["Products - Plastics"])/year_total
        USmswOriginal[year]["Products - Plastics"] = plastic_pt

        notRecycled_pt = 1 - paper_pt - glass_pt - metal_pt - plastic_pt
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
    "Non-Recyclable & Others" : "NON-RECYCLABLE & OTHERS"
    }, inplace=True)

# Swap plastic and paper columns
cols = list(USmswTotal.columns)
a, b = cols.index("GLASS COLLECTED"), cols.index("PLASTICS COLLECTED")
cols[a], cols[b] = cols[b], cols[a]
USmswTotal = USmswTotal[cols]

#print(USmswTotal)
# Selecting columns to compare
USp_cols = list(USmswTotal)
USp_cols.remove("YEAR")

#print(USmswTotal)

# Show US bar chart
# float number is formatted as % with 2 digits behind decimal

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
        title="Municipal Recyclable and Waste Collection Rate of the United States, 2010-2018",
        text_auto=".2%")
fig.show()