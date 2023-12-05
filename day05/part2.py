
INPUT_FILE = "input.txt"


def part2Version1():
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
            # SECOND APPROACH (causes max recursion depth to be reached, probably because recursive call is not resolved how i expected it to)
            ''' result = (lambda y: y + increase if sourceStart <= y < sourceEnd else result(y)) '''
            # FIRST APPROACH (very slow for big numbers)
            '''
            for j in range(rangeLen):
                result[sourceStart + j] = destStart + j
            '''
            
            i += 1
        
        def result(allNumRanges):
            resultRanges = []
            i = 0
            while (i < len(allNumRanges)):
                inputRangeStart = allNumRanges[i][0]
                inputRangeEnd = allNumRanges[i][1]
                
                # if the ranges have an intersection,
                wasRangeChanged = False
                for [sourceStart, sourceEnd, increase] in ranges:
                    if ((sourceStart <= inputRangeStart < sourceEnd) or (sourceStart < inputRangeEnd <= sourceEnd) or (inputRangeStart < sourceStart and sourceEnd < inputRangeEnd)):
                        # there is an overlap of the ranges, and the range is modified
                        if (inputRangeStart < sourceStart):
                            # the input range starts before the target range.
                            # we need to split the range in 2
                            # edit the start of this range
                            allNumRanges[i][0] = sourceStart
                            # and add the remaining range
                            allNumRanges.append([inputRangeStart, sourceStart])
                        if (sourceEnd < inputRangeEnd):
                            # the input range ends after the target range
                            # we need to split the range in 2
                            # edit the end of this range
                            allNumRanges[i][1] = sourceEnd
                            # and add the remaining range
                            allNumRanges.append([sourceEnd, inputRangeEnd])
                        
                        # modify the range
                        wasRangeChanged = True
                        resultRanges.append([allNumRanges[i][0] + increase, allNumRanges[i][1] + increase])
                
                if (not wasRangeChanged):
                    resultRanges.append([inputRangeStart, inputRangeEnd])
                
                i += 1
                
            return resultRanges
                
                
        
        return i, result


    with open(INPUT_FILE, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
        
        # parse the seeds (line 0)
        seedRanges = [int(num) for num in lines[0][len("seeds:"):].strip().split(" ")]
        groupedSeedRanges = []
        for i in range(0, len(seedRanges), 2):
            rangeStart = seedRanges[i]
            rangeLen = seedRanges[i+1]
            rangeEnd = rangeStart + rangeLen
            
            groupedSeedRanges.append([rangeStart, rangeEnd])
        
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
        soil = seedToSoil(groupedSeedRanges)
        fertilizers = soilToFertilizer(soil)
        water = fertilizerToWater(fertilizers)
        light = waterToLight(water)
        temp = lightToTemp(light)
        humidity = tempToHumid(temp)
        locations = humidToLocation(humidity)
        
        # finally, search and print the smallest location
        minLocation = min([locationRange[0] for locationRange in locations])
        
        # finally, print the smallest location
        print(f"The lowest location number corresponding to one of the seeds is {minLocation}")
        # ANSWER: 52510809


def part2Version2():
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

        # once all the data is collected, we can further process it and then proceed to the mapping
        seedRanges = []
        for i in range(0, len(seeds), 2):
            seedRanges.append([seeds[i], seeds[i] + seeds[i+1]])
            # seedRanges' entries are all [rangeStart, rangeEnd]
        
        mappedRanges = [[] for mapIndex in range(len(mapData))]
        i = 0
        mapIndex = 0
        while (i < len(seedRanges)):
            # do the first mapping
            hasBeenMapped = False
            # search if this seed value is mapped due to any range
            seedRangeStart = seedRanges[i][0]
            seedRangeEnd = seedRanges[i][1]
            for [sourceStart, sourceEnd, increase] in mapData[mapIndex]:
                if ((sourceStart <= seedRangeStart < sourceEnd) or (sourceStart < seedRangeEnd <= sourceEnd) or (seedRangeStart < sourceStart and sourceEnd < seedRangeEnd)):
                    # the ranges have an overlap
                    # split up the seedRange if it's not fully inside the mapping range
                    if (seedRangeStart < sourceStart):
                        # fix the current range
                        seedRanges[i][0] = sourceStart
                        # and add the remaining range
                        seedRanges.append([seedRangeStart, sourceStart])
                    if (sourceEnd < seedRangeEnd):
                        # fix the current range
                        seedRanges[i][1] = sourceEnd
                        # and add the remaining range
                        seedRanges.append([sourceEnd, seedRangeEnd])
                    
                    # and map the current range to its new values
                    mappedRanges[mapIndex].append([seedRanges[i][0] + increase, seedRanges[i][1] + increase])
                    hasBeenMapped = True
            
            # otherwise, it keeps the same value
            if (not hasBeenMapped):
                mappedRanges[mapIndex].append([seedRanges[i][0], seedRanges[i][1]])
            
            # and go to next seed
            i += 1
        
        # for each next map, compute values based on previous map's results
        for mapIndex in range(1, len(mapData)):
            i = 0
            while (i < len(mappedRanges[mapIndex - 1])):
                hasBeenMapped = False
                # search if this seed value is mapped due to any range
                inputRangeStart = mappedRanges[mapIndex - 1][i][0]
                inputRangeEnd = mappedRanges[mapIndex - 1][i][1]
                for [sourceStart, sourceEnd, increase] in mapData[mapIndex]:
                    if ((sourceStart <= inputRangeStart < sourceEnd) or (sourceStart < inputRangeEnd <= sourceEnd) or (inputRangeStart < sourceStart and sourceEnd < inputRangeEnd)):
                        # the ranges have an overlap
                        # split up the seedRange if it's not fully inside the mapping range
                        if (inputRangeStart < sourceStart):
                            # fix the current range
                            mappedRanges[mapIndex - 1][i][0] = sourceStart
                            # and add the remaining range
                            mappedRanges[mapIndex - 1][i].append([inputRangeStart, sourceStart])
                        if (sourceEnd < inputRangeEnd):
                            # fix the current range
                            mappedRanges[mapIndex - 1][i][1] = sourceEnd
                            # and add the remaining range
                            mappedRanges[mapIndex - 1][i].append([sourceEnd, inputRangeEnd])
                        
                        # and map the current range to its new values
                        mappedRanges[mapIndex].append([mappedRanges[mapIndex - 1][i][0] + increase, mappedRanges[mapIndex - 1][i][1] + increase])
                        hasBeenMapped = True
                
                # otherwise, it keeps the same value
                if (not hasBeenMapped):
                    mappedRanges[mapIndex].append([mappedRanges[mapIndex - 1][i][0], mappedRanges[mapIndex - 1][i][1]])
                
                # and go to next mapped value
                i += 1
        
        # finally, return the minimum location
        # NOTE: we know that the minimum location will be the start of some range, hence we only need to find the minimum of the rangeStarts
        rangeStarts = [mappedRange[0] for mappedRange in mappedRanges[-1]]
        minLocation = min(rangeStarts)
        
        print(f"The lowest location number corresponding to one of the seeds is {minLocation}")
        # ANSWER: 52510809


if __name__ == "__main__":
    part2Version2()