
INPUT_FILE = "input.txt"

def listsAreTheSame(lst1 : [str], lst2: [str]) -> bool:
    """ Returns whether the two given lists are the same 
        for the part they have in common (i.e. one list is 
        allowed to be larger than the other, as long as both 
        have the same elements in the rest)
    """
    for i in range(min(len(lst1), len(lst2))):
        if (lst1[i] != lst2[i]):
            return False
    
    return True


with open(INPUT_FILE, 'r') as f:
    # 1) parse the input
    lines = [l.strip() for l in f.readlines()]
    # --> separate each map into its own list
    maps = []
    nextMap = []
    for i in range(len(lines)):
        if (lines[i] == ""):
            # empty lines separate maps
            maps.append(nextMap)
            nextMap = []
        else:
            nextMap.append(lines[i])
    # add the last map
    if (len(nextMap) != 0):
        maps.append(nextMap)
    
    # 2) for each map, check if it is reflected vertically or horizontally
    total = 0
    for mapIdx in range(len(maps)):
        # try each possible horizontal separation
        foundHorizontalReflection = False
        row = 1
        while (not foundHorizontalReflection and row < len(maps[mapIdx])):
            rowsAbove = maps[mapIdx][:row]
            rowsAbove.reverse()     # before row (in inverted order)
            rowsBelow = maps[mapIdx][row:]      # after row (including row itself)
            
            if listsAreTheSame(rowsAbove, rowsBelow):
                # the map has a horizontal split
                total += 100 * len(rowsAbove)
                foundHorizontalReflection = True
            
            row += 1
        # then, if we didn't find a horizontal reflection, search a vertical one
        if not foundHorizontalReflection:
            foundVerticalReflection = False
            col = 1
            while (not foundVerticalReflection and col < len(maps[mapIdx][0])):
                colsLeft = ["".join([maps[mapIdx][rowIdx][colIdx] for rowIdx in range(len(maps[mapIdx]))]) for colIdx in range(col-1, -1, -1)]
                # the columns left of col (in inverted order)
                colsRight = ["".join([maps[mapIdx][rowIdx][colIdx] for rowIdx in range(len(maps[mapIdx]))]) for colIdx in range(col, len(maps[mapIdx][0]))]
                # the columns right of col (including col)
                
                if listsAreTheSame(colsLeft, colsRight):
                    # the map has a vertical split here
                    total += len(colsLeft)
                    foundVerticalReflection = True
                
                col += 1
            
            # sanity check: if we didn't find any reflection at all, raise an error
            if not foundVerticalReflection:
                raise ValueError(f"Did not find any reflection at all for map with index {mapIdx}")
    
    # 3) return result
    print(f"The summary of the pattern notes is equal to {total}")
    # ANSWER: 32723