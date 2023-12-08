
from math import gcd

def lcm(n1, n2):
    """ Computes the least common multiple of n1 and n2
        Credits: https://stackoverflow.com/a/51716959
    """
    return abs(n1*n2) // gcd(n1, n2)

INPUT_FILE = "input.txt"

with open(INPUT_FILE, 'r') as f:
    lines = [l.strip() for l in f.readlines()]
    
    # parse the moves to do
    moves = [c for c in lines[0]]
    # and parse the state transitions
    # while parsing the state transitions, we also add any starting states to a list
    startingStates = []
    transitions = {}
    for data in lines[2:]:
        # parse the input data
        sourceState, destStates = data.split("=")
        sourceState = sourceState.strip()
        stateLeft, stateRight = [x.strip() for x in destStates.split(",")]
        stateLeft = stateLeft[1:]       # remove the "("
        stateRight = stateRight[:-1]    # remove the ")"
        
        # add the transition in the dictionary
        transitions[(sourceState, "L")] = stateLeft
        transitions[(sourceState, "R")] = stateRight
        
        # and add the source state to the starting states if it ends with an "A"
        if sourceState.endswith("A"):
            startingStates.append(sourceState)
    
    # then, perform the state transitions for each separate state
    currentStates = [state for state in startingStates]
    numStepsToFinalState = [0 for state in startingStates]
    for i in range(len(currentStates)):
        while True:
            nextMove = moves[numStepsToFinalState[i] % len(moves)]
            currentStates[i] = transitions[(currentStates[i], nextMove)]
            numStepsToFinalState[i] += 1
            
            if (currentStates[i].endswith("Z")):
                break
    
    # and the final result is then the least common multiple of these numbers
    result = lcm(numStepsToFinalState[0], numStepsToFinalState[1])
    for i in range(2, len(numStepsToFinalState)):
        result = lcm(result, numStepsToFinalState[i])
    
    # and give the result
    print(f"It takes {result} steps to reach ending states simultaneously from all states starting in 'A'")
    # ANSWER: 16342438708751