import country_converter

file = open("SuicideData.csv",'r')
Lines = file.readlines()
writeLines = []
count = 0
for line in Lines:
    if(count == 0):
        print("Starting conversion")
        print("This is going to take awhile (10+ minutes), so don't be suprised if it seems like nothing is happening.")
        writeLines.append(line)
    else:
        if (count == 6955):
            print("25% done")
        elif (count == 13910):
            print("50% done")
        elif (count == 20865):
            print("75% done")
        lineArray = line.split(",")
        some_names = [lineArray[0]]
        standard_name = country_converter.convert(names=some_names, to='name_short')
        lineArray[0] = standard_name
        strToAdd = ""
        firstIndex = 1
        for entry in lineArray:
            if(firstIndex == 1):
                strToAdd = entry
                firstIndex = 0
            else:
                strToAdd = strToAdd + "," + entry
        writeLines.append(strToAdd)
    count += 1

file.close()

file2 = open('SuicideDataContriesConverted.csv','w')
file2.writelines(writeLines)
file2.close()

print("Finished converting all SuicideData country names")