import plotly.express as px
import csv
import pandas as pd

# National solid waste management dataset from EPA
# https://edg.epa.gov/metadata/catalog/search/resource/details.page?uuid=C9310A59-16D2-4002-B36B-2B0A1C637D4E
# Credit to Professor Matt Miller for initial convertion of the CSV 
# to a dictionary that could be visualized with the Plotly module.
# Further effort has been made to remove data that are out of the 
# scope of this project.

with open("National_MSW_total.csv","r") as USmswTotal_csv:
    reader = csv.DictReader(USmswTotal_csv)

    USmswTotal = {}

    # Select data to be included in the USmswTotal{}
    for row in reader:
        if "Materials" in row:

            # Skip footer description rows in the CSV
            if row["Materials"] != "" and "Table 1" not in row["Materials"]:
                for year in row:

                    # Read and create keys with year values from the first row
                    if year != "Materials":
                        
                        # Take data from 2010
                        if int(year) >= 2010:
                            if year not in USmswTotal:
                                USmswTotal[year] = {"year" : year}
                            
                            # Add corresponding materials as keys and their values to each year
                            USmswTotal[year][row["Materials"]] = row[year]
   
    #print(USmswTotal)

    # Calculate percentage and write to new file
    for year in USmswTotal:
        year_total = int(USmswTotal[year]["Total MSW Generated - Weight"])
        
        paper_pt = int(USmswTotal[year]["Products - Paper and Paperboard"])/year_total*100
        USmswTotal[year]["Products - Paper and Paperboard"] = paper_pt
        
        glass_pt = int(USmswTotal[year]["Products - Glass"])/year_total*100
        USmswTotal[year]["Products - Glass"] = glass_pt

        metal_pt = int(USmswTotal[year]["Products - Metals - Total"])/year_total*100
        USmswTotal[year]["Products - Metals - Total"] = metal_pt

        plastic_pt = int(USmswTotal[year]["Products - Plastics"])/year_total*100
        USmswTotal[year]["Products - Plastics"] = plastic_pt

        notRecycled_pt = 100-paper_pt-glass_pt-metal_pt-plastic_pt
        USmswTotal[year]["Not recycled"] = notRecycled_pt

    # Remove unwanted data
    for year in USmswTotal:
        for p in ["Products - Metals - Ferrous", "Products - Metals - Aluminum", "Products - Metals - OtherNonferrous", "Products - Rubber and Leather", "Products - Textiles", "Products - Wood", "Products - Other", "Products - Total Materials", "Other Wastes - Food Waste", "Other Wastes - Yard Trimmings", "Other Wastes - Miscellaneous Inorganic Wastes", "Other Wastes - Total", "Total MSW Generated - Weight"]:
            USmswTotal[year].pop(p)

    # Write to new csv for plotly
    with open("USmswTotal_p.csv","w") as outfile:
        
        # Create a list of keys from any of the years for headers
        fieldnames = list(USmswTotal["2010"])
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        # Populate data in rows
        for year in USmswTotal:
            writer.writerow(USmswTotal[year])

# Create a list of years by listing the first element's value of each dictionary
years = list(USmswTotal)
#print(years)

# Create a list of materials like creating the header list in outputting the new csv file
materials = list(USmswTotal["2010"])
#print(materials)
materials.remove("year")

data = pd.read_csv("USmswTotal_p.csv")

print(data)



# This one works. Just to hide temperary to save time
fig = px.bar(data, x=years, y=materials)
fig.show()




# data = pd.read_csv("National_MSW_total.csv", skipfooter=3, index_col=0)
# #data = data.reset_index(drop=True)
# print(data)

# Before transpose: make column headers as a list
# year = list(data.columns.values)
# year = year[7:]
#print(year)

# Before transpose: select materials
# materials = list(data["Materials"].values)
# materials = materials[0], materials[1], materials[5], materials[6], materials[11]
# print(materials)

# Try convert columns to rows and see if the bars can be base on year.

# dataT = data.transpose()
# dataT = dataT.reset_index()
# print(dataT)
# # print(dataT[1])

# materials = "Products - Paper and Paperboard|Products - Glass|Products - Metals - Total|Products - Plastics"

# fig = px.bar(dataT, x=data.iloc[6:], y="Products - Plastics")
# fig.show()

# Before transpose: not good bar chart
# fig = px.bar(data, x=year, y="Materials")

# Not successful
# fig = px.bar(data,x=year,y=[list(materials)])

# fig = px.bar(dataT, x=dataT.iloc[7:16],
#              y="Products - Glass|Products - Metals - Total")
# fig.show()



#print(data["Materials"])     #use header key for column
#print(data.loc[1])      #use loc for rows
#print(data.loc[3,"1960"])  #Specific cell, .loc[row, col]
#print(data["1960"].loc[3] + data["1960"].loc[4])   #calculate specific cells


#print(data)

#for yr in data[""]

# National MSW numbers (tons):
# Products - Paper and Paperboard [0]
# Products - Glass [1]
# Products - Metals - Total [5]
# Products - Plastics [6]
# Products - Other Recyclable = Total Materials [11] - Above four
# Total MSW Generated-Weight [16] = Total Materials + Other Wastes-Total [15]

