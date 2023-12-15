
from typing import Union

INPUT_FILE = "input.txt"
ADD_OP = "="    # the symbol of the operation to add a new item
REMOVE_OP = "-" # the symbol of the operation to remove an item
OPERATION_CHARS = [ADD_OP, REMOVE_OP]

DEBUG = False

def HASH(s : str) -> int:
    """ Holiday ASCII String Helper:
        Transforms any string into a number in the range 0-255
    """
    currentVal = 0
    for char in s:
        asciiCode = ord(char)
        currentVal = (17 * (currentVal + asciiCode)) % 256
        ''' # STEP BY STEP ALTERNATIVE:
        asciiCode = ord(char)
        currentVal += asciiCode
        currentVal *= 17
        currentVal = currentVal % 256
        '''
    return currentVal

def findEntryWithLabel(entries: list[tuple[Union[str, int]]], label: str) -> int:
    """ Given a list of entries in a given box,
        search for the entry with the given label.
        
        Returns the index at which that entry was found,
        or -1 if no entry with this label was found
    """
    foundLabel = False
    i = 0
    while (i < len(entries) and not foundSameLabel):
        if (entries[i][0] == label):
            foundLabel = True
        else:
            i += 1
    
    if not foundLabel:  # to return -1 if it was not found
        i = -1
    
    return i

def HASHMAPAddOperation(label : str, focalLength : int, hashmap: dict[int, list[tuple[Union[str, int]]]]):
    """ Performs the ADD operation on the hashmap
    """
    # check if the hashmap already has an entry for this HASH value
    hashValue = HASH(label)
    if hashValue in hashmap:
        # the box is not empty
        # --> check if there is already an entry with the same label
        entries = hashmap[hashValue]
        foundSameLabel = False
        i = 0
        while (i < len(entries) and not foundSameLabel):
            if (entries[i][0] == label):
                foundSameLabel = True
            else:
                i += 1
        
        if foundSameLabel:
            # replace the entry with the same label
            entries[i] = (label, focalLength)
        else:
            # add a new entry to the end
            entries.append((label, focalLength))
    else:
        # the box with this number is empty
        # --> create the box and add this element
        hashmap[hashValue] = [(label, focalLength)]

def HASHMAPRemoveOperation(label : str, hashmap: dict[int, list[tuple[Union[str, int]]]]):
    """ Performs the remove operation on the hashmap,
        i.e. remove the entry with the given label if 
            there is an entry with the given label
    """
    # make sure that the box of this label is not empty
    HashValue = HASH(label)
    if HashValue in hashmap:
        # then, check if the box contains an item with this label
        entries = hashmap[HashValue]
        foundSameLabel = False
        i = 0
        while (i < len(entries) and not foundSameLabel):
            if (entries[i][0] == label):
                foundSameLabel = True
            else:
                i += 1
        
        if foundSameLabel:
            # remove the entry with the label
            del entries[i]

def HASHMAP(step: str, hashmap: dict[int, list[tuple[Union[str, int]]]]):
    """ Holiday ASCII String Helper Manual Arrangement Procedure
        Takes in a step to perform and modifies the given hashmap 
        according to the operation described in the step.
        
        The hashmap will be as follows:
        - keys = box numbers
        - values = lists of entries, with each entry being a tuple with:
                    - index 0 = label
                    - index 1 = focal length of the lens
    """
    # 1) extract the info from the step
    i = 0
    while (i < len(step) and step[i] not in OPERATION_CHARS):
        # increase i up to the operation character
        i += 1
    # split the info up
    label = step[:i]
    operationChar = step[i]
    remainder = step[i+1:]
    
    # 2) perform the correct operation
    match operationChar:
        case "=":   # = ADD_OP
            # extract the focal length
            focalLength = int(remainder)
            # call the method to perform this operation
            HASHMAPAddOperation(label, focalLength, hashmap)
        case "-":   # = REMOVE_OP
            # call the method to perform this operation
            HASHMAPRemoveOperation(label, hashmap)

def printHashMap(hashmap: dict[int, list[tuple[Union[str, int]]]]):
    """ Prints the given hashmap in the format as described in the problem
    """
    orderedKeys = sorted(list(hashmap.keys()))
    for key in orderedKeys:
        print(f"Box {key}: ", end="")
        entries = hashmap[key]
        for label, focalLength in entries:
            print(f"[{label} {focalLength}] ", end="")
        print()




with open(INPUT_FILE, 'r') as f:
    # parse the input data
    data = f.readline().strip().split(",")
    
    # apply the HASHMAP operation for each step
    hashmap = {}
    for step in data:
        HASHMAP(step, hashmap)
        
        if (DEBUG):
            print(f"After \"{step}\":")
            printHashMap(hashmap)
            print()
    
    # compute the focusing power of all lenses
    totalFocusingPower = 0
    for boxNum in hashmap.keys():
        lenses = hashmap[boxNum]
        for slotNum, lens in enumerate(lenses):
            focalLength = lens[1]
            
            totalFocusingPower += (boxNum + 1) * (slotNum + 1) * focalLength
    
    # return the total focusing power
    print(f"The total focusing power of the lenses is: {totalFocusingPower}")
    # ANSWER: 230462