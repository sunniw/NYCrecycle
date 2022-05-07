## Pratt INFO 664 - Programming for Cultural Heritage Final Project
<img src="https://github.com/sunniw/NYCrecycle/blob/8698cb43ffc15e81a87ee1ac30e225f9c8dc8e03/banner.png" alt="New York City Recyclable Collection 2010 - 2018">

### New York City Recyclable Collection 2010-2018
This project attempted to look at the New York City recycle rate changes over the last decade. It focused on the two mainstream recyclables: paper and MGP (metal, glass, and plastic). The project used the US Environmental Protection Agency's data as a benchmark to measure the effectiveness of the NYC program. Products of this project were three bar charts: NYC collection rate, national collection rate, and a comparison of the two. As the EPA data covered only up to 2018, the final comparison did not include the latest three years of the NYC data.

### Dataset used
1. [DSNY Monthly Tonnage Data](https://data.cityofnewyork.us/City-Government/DSNY-Monthly-Tonnage-Data/ebb7-mvp5) - NYC Open Data<br>
Contains NYC monthly waste collection data between 1990 and 2022. Besides the two mainstream recyclables, this dataset also includes organic materials, which is out of this project's focus. Those data are combined with the trash numbers, and shown as "NYC non-recyclable & others" in the charts.
2. [Materials Municipal Waste Stream 1960-2018](https://edg.epa.gov/metadata/catalog/search/resource/details.page?uuid=C9310A59-16D2-4002-B36B-2B0A1C637D4E) - United States Environmental Protection Agency<br>
Contains national annual waste collection data from 1960 to 2018. This dataset reflects more specific material types collected in waste stream. To be compared with the NYC data, this project combined the four types of metals into one "metal" category. All other materials, except for paper, glass and plastic, are grouped under "US non-recyclable and others" in the charts.

### File description
File | Description
---- | -----------
NYCmswTotal_p.csv | Checkpoint dataset created from recycle_stat_NY.py, used to create the final combined chart.
USmswTotal_p.csv | Checkpoint dataset created from recycle_stat_US.py, used to create the final combined chart.
banner.png | Project header image.
barchart_NY.png | Stacked bar chart created from recycle_stat_NY.py.
barchart_US.png | Stacked bar chart created from recycle_stat_US.py.
barchart_compare.png | Combined stacked bar chart created from recycle_stat.py.
recycle_stat.py | Main script to compare NYC and US datasets in a stacked bar chart. Should run **AFTER** the next two scripts if not downloading the checkpoint datasets from this list.
recycle_stat_NY.py | Script handling the NYC data and create a new csv file and a visual.
recycle_stat_US.py | Script handling the EPA data to create a new csv file and a visual.

### To use the scripts
All scripts are written in Python 3. The resulting charts will be opened in a web browser upon running the scripts. To run locally, please download the two original datasets from sources listed in previous section, the latest version of Python, and the following modules installed:
- [pandas](https://pandas.pydata.org/getting_started.html) version 1.3.5 or later.
- [plotly](https://plotly.com/python/getting-started/) version 5.6.0 or later.

**Both [recycle_stat_NY.py](https://github.com/sunniw/NYCrecycle/blob/9e8852e92448395aa82e8576fe293b9c70a4f72d/recycle_stat_NY.py) and [recycle_stat_US.py](https://github.com/sunniw/NYCrecycle/blob/9e8852e92448395aa82e8576fe293b9c70a4f72d/recycle_stat_US.py) should be run _BEFORE_ [recycle_stat.py](https://github.com/sunniw/NYCrecycle/blob/9e8852e92448395aa82e8576fe293b9c70a4f72d/recycle_stat.py), so that the two checkpoint datasets will be created for final comparison.**

### Results
This project produces three stacked bar charts.
<img src="https://github.com/sunniw/NYCrecycle/blob/9e8852e92448395aa82e8576fe293b9c70a4f72d/barchart_NY.png" width = "800px" alt="Municipal Recyclable and Waste Collection Rate of the New York City, 2010-2022"></br>
<img src="https://github.com/sunniw/NYCrecycle/blob/9e8852e92448395aa82e8576fe293b9c70a4f72d/barchart_US.png" width = "800px" alt="Municipal Recyclable and Waste Collection Rate of the United States, 2010-2018"></br>
When reading separately, New York shows a slow annual increase in collecting recyclables. The total reached the highest point of 19.78% (9.35% in Paper and 10.43% in MGP) in 2020, then declined in the next two years. While nationally, the total collection of recyclables declined slowly, and reached the lowest point of 48.2% on 2018.
<img src="https://github.com/sunniw/NYCrecycle/blob/9e8852e92448395aa82e8576fe293b9c70a4f72d/barchart_compare.png" width = "800px" alt="Comparison of Municipal Recyclable and Waste Collection Rate of NYC and US, 2010-2018"></br>
When comparing side-by-side, New York's collection of paper and MGP continued to be dwarfed by the national percentage. Even in its worst year, the national collection rate of paper and MGP still more than double to the New York's. It shows the City has rooms to improve its recycle program.
