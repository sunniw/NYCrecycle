# Pratt INFO 664 - Programming for Cultural Heritage Final Project
<img src="https://github.com/sunniw/NYCrecycle/blob/e5a0271c1d5796302f6eef6805c104f78d6893ca/banner.png" alt="New York City Recyclable Collection 2010 - 2018">

## New York City Recyclable Collection 2010 - 2018
This project attempts to look at the New York City recycle rate changes over the last decade. It focuses on the two mainstream recyclables: paper and MGP (metal, glass, and plastic). The project uses the US Environmental Protection Agency's data as a benchmark to measure the effectiveness of the NYC program. Products of this project are three bar charts: NYC collection rate, national collection rate, and a comparison of the two datasets. Please note that the final comparison is only up to 2018, as the EPA data does not provide later years' information.

## Dataset used
1. [DSNY Monthly Tonnage Data](https://data.cityofnewyork.us/City-Government/DSNY-Monthly-Tonnage-Data/ebb7-mvp5) - NYC Open Data<br>
Contains NYC monthly waste collection data between 1990 and 2022. Besides the two mainstream recyclables, this dataset also includes organic materials, which is out of this project's focus. Those data are combined with the trash numbers, and shown as "NYC non-recyclable & others" in the charts.
2. [Materials Municipal Waste Stream 1960-2018](https://edg.epa.gov/metadata/catalog/search/resource/details.page?uuid=C9310A59-16D2-4002-B36B-2B0A1C637D4E) - United States Environmental Protection Agency<br>
Contains national annual waste collection data from 1960 to 2018. This dataset reflects more specific material types collected in waste stream. To be compared with the NYC data, this project combined the four types of metals into one "metal" category. All other materials, except for paper, glass and plastic, are grouped under "US non-recyclable and others" in the charts.

## To use the scripts
All three scripts are written in Python 3 and can be run independently. The resulting charts will be opened in a web browser upon running the scripts. To run locally, please be sure to have the latest version of Python, and the following modules installed:
- [pandas](https://pandas.pydata.org/getting_started.html)
- [plotly](https://plotly.com/python/getting-started/)

## Results
This project produces three stacked bar charts.
<img src="https://github.com/sunniw/NYCrecycle/blob/main/barchart_NY.png" alt="Municipal Recyclable and Waste Collection Rate of the New York City, 2010-2022">
<img src="https://github.com/sunniw/NYCrecycle/blob/main/barchart_US.png" alt="Municipal Recyclable and Waste Collection Rate of the United States, 2010-2018">
When reading separately, New York shows a slow annual increase in collecting recyclables. The total reached the highest point of 19.78% (9.35% in Paper and 10.43% in MGP) in 2020, then declined in the next two years. While nationally, the total collection of recyclables declined slowly, and reached the lowest point of 48.2% on 2018.
<img src="https://github.com/sunniw/NYCrecycle/blob/main/barchart_compare.png" alt="Comparison of Municipal Recyclable and Waste Collection Rate of NYC and US, 2010-2018">
When comparing side-by-side, New York's collection of paper and MGP continued to be dwarfed by the national percentage. Even in its worst year, the national collection rate of paper and MGP still more than double to the New York's. It shows the City has rooms to improve its recycle program.
