
INPUT_FILE = "input.txt"


def part1Version1():
    def findIndexOfLine(data, line, startIndex = 0):
        """ Searches for and returns the index of the line 
            whose content matches line
        """
        while (not data[startIndex].startswith(line)):
            startIndex += 1
        return startIndex

    def parseMap(data):
        """ Parses the given data into a map
            Each line should either be an empty line or follow the format:
                X Y Z
            where X is the start of the destination range, 
                Y the start of the source range
                and Z the length of the range that is mapped
            
            Returns the map as a function and the number of lines that were parsed
        """
        ranges = []
        #result = (lambda x: x)  # by default, return the same number
        i = 0
        while (i < len(data) and data[i] != ''):
            destStart, sourceStart, rangeLen = [int(num) for num in data[i].split(" ")]
            increase = destStart - sourceStart
            sourceEnd = sourceStart + rangeLen
            
            # update the mapping function
            ranges.append([sourceStart, sourceEnd, increase])
            # PREVIOUS APPROACH 2 (causes max recursion depth to be reached, probably because recursive call is not resolved how i expected it to)
            # result = (lambda y: y + increase if sourceStart <= y < sourceEnd else result(y))
            # PREVIOUS APPROACH (very slow for big numbers)
            '''
            for j in range(rangeLen):
                result[sourceStart + j] = destStart + j
            '''
            
            i += 1
        
        def result(n):
            # if one of the ranges applies, modify n accordingly
            for [sourceStart, sourceEnd, increase] in ranges:
                if sourceStart <= n < sourceEnd:
                    return n + increase
            # otherwise, return the unmodified number
            return n
        
        return i, result


    with open(INPUT_FILE, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
        
        # parse the seeds (line 0)
        seeds = [int(num) for num in lines[0][len("seeds:"):].strip().split(" ")]
        
        # parse the first map, the seed-to-soil map
        # 1) find where it starts in the input
        seedToSoilStart = findIndexOfLine(lines, 'seed-to-soil map:', 1)
        # 2) parse its description
        numParsedLines, seedToSoil = parseMap(lines[seedToSoilStart + 1:])
        
        # parse the second map, the soil-to-fertilizer map
        # 1) find where it starts in the input
        soilToFertilizerStart = findIndexOfLine(lines, 'soil-to-fertilizer map:', seedToSoilStart + 1 + numParsedLines)
        # 2) parse its description
        numParsedLines, soilToFertilizer = parseMap(lines[soilToFertilizerStart + 1:])
        
        # parse the third map, fertilizer-to-water map
        # 1) find where it starts in the input
        fertilizerToWaterStart = findIndexOfLine(lines, 'fertilizer-to-water map:', soilToFertilizerStart + 1 + numParsedLines)
        # 2) parse its description
        numParsedLines, fertilizerToWater = parseMap(lines[fertilizerToWaterStart + 1:])
        
        # parse the fourth map, water-to-light map
        # 1) find where it starts in the input
        waterToLightStart = findIndexOfLine(lines, 'water-to-light map:', fertilizerToWaterStart + 1 + numParsedLines)
        # 2) parse its description
        numParsedLines, waterToLight = parseMap(lines[waterToLightStart + 1:])
        
        # parse the fifth map, light-to-temperature map
        # 1) find where it starts in the input
        lightToTempStart = findIndexOfLine(lines, 'light-to-temperature map:', waterToLightStart + 1 + numParsedLines)
        # 2) parse its description
        numParsedLines, lightToTemp = parseMap(lines[lightToTempStart + 1:])
        
        # parse the sixth map, temperature-to-humidity map
        # 1) find where it starts in the input
        tempToHumidStart = findIndexOfLine(lines, 'temperature-to-humidity map:', lightToTempStart + 1 + numParsedLines)
        # 2) parse its description
        numParsedLines, tempToHumid = parseMap(lines[tempToHumidStart + 1:])
        
        # parse the seventh and last map, humidity-to-location map
        # 1) find where it starts in the input
        humidToLocationStart = findIndexOfLine(lines, 'humidity-to-location map:', tempToHumidStart + 1 + numParsedLines)
        # 2) parse its description
        numParsedLines, humidToLocation = parseMap(lines[humidToLocationStart + 1:])
        
        
        # then map all seeds through all of the maps to get the locations
        soil = map(seedToSoil, seeds)
        fertilizers = map(soilToFertilizer, soil)
        water = map(fertilizerToWater, fertilizers)
        light = map(waterToLight, water)
        temp = map(lightToTemp, light)
        humidity = map(tempToHumid, temp)
        locations = map(humidToLocation, humidity)
        
        # finally, print the smallest location
        print(f"The lowest location number corresponding to one of the seeds is {min(locations)}")
        # ANSWER: 662197086


def part1Version2():
    with open(INPUT_FILE, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
        
        # extract all the data and transform to int arrays
        # 1) extract the seeds data
        i = 0
        seeds = [int(num) for num in lines[i][len("seeds:"):].strip().split(" ")]
        # 2) extract the map data
        i = 1
        mapHeaders = ["seed-to-soil map:", "soil-to-fertilizer map:", "fertilizer-to-water map:", "water-to-light map:", "light-to-temperature map:", "temperature-to-humidity map:", "humidity-to-location map:"]
        mapData = []
        for mapIndex in range(len(mapHeaders)):
            # skip ahead until you find the correct header
            while (not lines[i].startswith(mapHeaders[mapIndex])):
                i += 1
            # skip the header too
            i += 1
            # add all the lines until the end of the numbers
            mapData.append([])
            while (i < len(lines) and not lines[i] == ''):
                mapData[mapIndex].append(lines[i])
                i += 1
            
            # once all the lines are in there, process the lines further
            mapData[mapIndex] = [[int(num) for num in line.strip().split(" ")] for line in mapData[mapIndex]]
            # --> will split e.g. "50 98 2" into [50, 98, 2]
            # but I also want to map it from [destinationRangeStart, sourceRangeStart, rangeLength]
            #   to something like [sourceRangeStart, sourceRangeEnd, IncreaseToReachDestinationRange]
            for i in range(len(mapData[mapIndex])):
                destRangeStart = mapData[mapIndex][i][0]
                sourceRangeStart = mapData[mapIndex][i][1]
                rangeLength = mapData[mapIndex][i][2]
                # compute complementary info
                sourceRangeEnd = sourceRangeStart + rangeLength
                increaseToDestinationRange = destRangeStart - sourceRangeStart
                
                # replace data
                mapData[mapIndex][i] = [sourceRangeStart, sourceRangeEnd, increaseToDestinationRange]

        # once all the data is collected, we can proceed with the mapping
        mappedValues = [[] for mapIndex in range(len(mapData))]
        for i in range(len(seeds)):
            # do the first mapping
            mapIndex = 0
            hasBeenMapped = False
            # search if this seed value is mapped due to any range
            for mapRange in mapData[mapIndex]:
                if (mapRange[0] <= seeds[i] and seeds[i] < mapRange[1]):
                    # map it to its new value
                    mappedValues[mapIndex].append(seeds[i] + mapRange[2])
                    hasBeenMapped = True
                    break
            # otherwise, it keeps the same value
            if (not hasBeenMapped):
                mappedValues[mapIndex].append(seeds[i])
            
            # for each next map, compute values based on previous map's results
            for mapIndex in range(1, len(mapData)):
                hasBeenMapped = False
                # search if this seed value is mapped due to any range
                for mapRange in mapData[mapIndex]:
                    if (mapRange[0] <= mappedValues[mapIndex - 1][i] and mappedValues[mapIndex - 1][i] < mapRange[1]):
                        # map it to its new value
                        mappedValues[mapIndex].append(mappedValues[mapIndex - 1][i] + mapRange[2])
                        hasBeenMapped = True
                        break
                # otherwise, it keeps the same value
                if (not hasBeenMapped):
                    mappedValues[mapIndex].append(mappedValues[mapIndex - 1][i])
        
        # finally, return the minimum location
        minLocation = min(mappedValues[-1])
        
        print(f"The lowest location number corresponding to one of the seeds is {minLocation}")
        # ANSWER: 662197086


if __name__ == "__main__":
    part1Version2()