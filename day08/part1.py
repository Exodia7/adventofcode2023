
INPUT_FILE = "input.txt"

with open(INPUT_FILE, 'r') as f:
    lines = [l.strip() for l in f.readlines()]
    
    # parse the moves to do
    moves = [c for c in lines[0]]
    # and parse the state transitions
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
    
    # then, perform the state transitions, 
    startState = "AAA"
    destState = "ZZZ"
    currentState = startState
    numSteps = 0
    while (currentState != destState):
        nextMove = moves[numSteps % len(moves)]
        currentState = transitions[(currentState, nextMove)]
        numSteps += 1
    
    # and give the result
    print(f"It takes {numSteps} steps to go from state {startState} to state {destState}")
    # ANSWER: 19951