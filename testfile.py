import pandas as pd
import numpy as np
import matplotlib.pyplot as pyplot


# Make sure you either have these converted files, or run the 2 scripts to convert them!
earthquakes = pd.read_csv("EarthquakeDataWithCountries.csv")
suicides = pd.read_csv("SuicideDataContriesConverted.csv")


print("Now formatting Earthquake part.")

earthquake_avg_year_depth = [0] * 2020
earthquake_year_depths = dict()
for x in range(2020):
    earthquake_year_depths[x] = []

index = 0
for date in earthquakes['Date']:
    split_date = date.split("/")
    if len(split_date) == 3:
        year = int(split_date[2])
        val = earthquakes['Magnitude'].iloc[index]
        earthquake_year_depths[year].append(val)

    index += 1


for year_index in range(1985, 2017):
    totalNum = len(earthquake_year_depths[year_index])
    total = 0
    for depth in earthquake_year_depths[year_index]:
        total += int(depth)
    average = total / totalNum
    # earthquake_avg_year_depth[year_index] = average
    earthquake_avg_year_depth[year_index] = totalNum



fig, plot1 = pyplot.subplots(1,1,figsize=(12,6))
# Earthquake plot
plot1.plot(earthquake_avg_year_depth, label="earthquakes")
plot1.axis([1995, 2013, 0, 1000])
plot1.set_xlabel("Year",fontsize=14)
plot1.set_ylabel("Average Earthquake Amount",color="red",fontsize=14)
plot1.legend(loc='upper left')

pyplot.show()