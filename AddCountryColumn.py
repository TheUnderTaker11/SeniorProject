import reverse_geocoder
import pandas as pd
import numpy as np
import json
import country_converter

#This Python script only needs to be run once, since it actually takes quite awhile to do.



#Function to get the country from latitude and longitude coordinates
def getplace(lat, lon):
    coordinates = (float(lat), float(lon))
    locationResults = reverse_geocoder.get(coordinates,mode=1)
    some_names = [locationResults['cc']]
    standard_names = country_converter.convert(names=some_names, to='name_short')
    country = standard_names
    return country


earthquakefile = open("EarthquakeData.csv",'r')
Lines = earthquakefile.readlines()
writeLines = []
firstIndex = 1
totalLines = len(Lines)
count = 0
print("total lines to do:",totalLines)
print("Be paitent, based on my calculations this takes 16-17 minutes on my Gaming PC, so it could be awhile.")
for line in Lines:
    if(firstIndex == 1):
        firstIndex = 0
        toWriteLine = "country," + line
        writeLines.append(toWriteLine)
    else:
        if(count == 5853):
            print("25% done")
        elif(count == 11706):
            print("50% done")
        elif(count == 17559):
            print("75% done")
        lineArray = line.split(",")
        lat = lineArray[2]
        lon = lineArray[3]
        country = getplace(lat, lon)
        country = str(country).replace(",","")
        toWriteLine = country + "," + line
        writeLines.append(toWriteLine)
        count += 1
earthquakefile.close()

file2 = open('EarthquakeDataWithCountries.csv','w')
file2.writelines(writeLines)
file2.close()
print("Finished creating converted file!")