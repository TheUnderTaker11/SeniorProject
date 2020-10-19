#############
# This script is for part 1 of my prompt to give some 2d correlation.
# This one scales suicides down so you can see the relation between both lines.
#
# Author: Clay Bellou
#############
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as pyplot


# Handle the color-picking accessibility option!
color1 = "blue"
color2 = "red"

if len(sys.argv) == 2:
    print("To few color arguments! Using default colors")
elif len(sys.argv) == 3:
    print("Using colors ",sys.argv[1], " and ", sys.argv[2], " instead of the default colors!")
    print("(Default colors for this visualization are blue and red)")
    color1 = sys.argv[1]
    color2 = sys.argv[2]
elif len(sys.argv) > 3:
    print("To many color arguments! Using default colors")


earthquakes = pd.read_csv("EarthquakeData.csv")
suicides = pd.read_csv("SuicideData.csv")

print("Starting 2D Correlation graph.")

#init arrays
earthquake_avg_year_depth = [0] * 2020
earthquake_year_depths = dict()
for x in range(2020):
    earthquake_year_depths[x] = []

#enter all relevant depth data into it's array, with year as the index
index = 0
for date in earthquakes['Date']:
    split_date = date.split("/")
    if len(split_date) == 3:
        year = int(split_date[2])
        val = earthquakes['Depth'].iloc[index]
        # it's a 2d array so append the value to the array within the overall year array
        earthquake_year_depths[year].append(val)

    index += 1

# Use the 2d array to calculate the average depth value in each year
for year_index in range(1985, 2017):
    totalNum = len(earthquake_year_depths[year_index])
    total = 0
    for depth in earthquake_year_depths[year_index]:
        total += int(depth)
    average = total / totalNum
    earthquake_avg_year_depth[year_index] = average


###################### Begin suicide part ###################
suicides_per_year = [0] * 2020

#Calculate total number of suicides for all countries for each year
index = 0
for yearStr in suicides['year']:
    year = int(yearStr)
    suicides_per_year[year] += int(suicides['suicides_no'].iloc[index])
    index += 1


############## Begin plotting the data from above ################
fig, plot1 = pyplot.subplots(1,1,figsize=(12,6))

# Earthquake plot
plot1.plot(earthquake_avg_year_depth, label="Avg Earthquake Depth",color=color1)
pyplot.title('Relation of Avg Earthquake Depth and Total Suicides Globally Through the Years')
plot1.axis([1995, 2013, 0, 150])
plot1.set_xlabel("Year",fontsize=14)
plot1.set_ylabel("Average Earthquake Depth (km)",color=color1,fontsize=14)
plot1.legend(loc='upper left')

plot2 = plot1.twinx()
plot2.plot(suicides_per_year, label="suicides",color=color2)
plot2.axis([1995, 2013, 190000, 300000])
plot2.set_ylabel("Total Suicides Globally",color=color2,fontsize=14)
plot2.legend(loc='upper right')
pyplot.show()


print("Program Finished")
