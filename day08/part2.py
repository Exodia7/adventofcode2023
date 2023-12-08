
from math import gcd

def lcm(n1, n2):
    """ Computes the least common multiple of n1 and n2
        Credits: https://stackoverflow.com/a/51716959
    """
    return abs(n1*n2) // gcd(n1, n2)

def computeNumStepsToFinalStateV1(startingStates, moves, transitions):
    """ Computes the number of steps needed to reach a final state for each of the starting states individually.
        Returns a list with the number of steps for each starting state.
        
        This version takes a simpler approach, performing the state transitions for one state at a time.
        However, as a consequence, it is slightly less efficient.
    """
    currentStates = [state for state in startingStates]
    numStepsToFinalState = [0 for state in startingStates]
    # for each state,
    for i in range(len(currentStates)):
        # simulate the transitions until we reach a final state
        while True:
            # take next move and perform corresponding transition
            nextMove = moves[numStepsToFinalState[i] % len(moves)]
            currentStates[i] = transitions[(currentStates[i], nextMove)]
            numStepsToFinalState[i] += 1
            
            # if the state is final, stop
            if (currentStates[i].endswith("Z")):
                break
    
    return numStepsToFinalState

def computeNumStepsToFinalStateV2(startingStates, moves, transitions):
    """ Computes the number of steps needed to reach a final state for each of the starting states individually.
        Returns a list with the number of steps for each starting state.
        
        This version takes a more efficient, but also more complex approach than V1. It performs the simulations of each non-final state simultaneously.
    """
    isStateFinal = lambda state: state.endswith("Z")
    currentStates = [state for state in startingStates]
    numStepsToFinalState = [0 for state in startingStates]
    numSteps = 0
    # keep a list of the states which have not yet reached their final state
    unfinishedStateIndices = list(range(len(startingStates)))
    while True:
        # find next move
        nextMove = moves[numSteps % len(moves)]
        numSteps += 1
        # do the state transition for all states which are not yet final
        i = 0
        while i < len(unfinishedStateIndices):
            stateIdx = unfinishedStateIndices[i]
            currentStates[stateIdx] = transitions[(currentStates[stateIdx], nextMove)]
            # check if we have now reached the final state
            if isStateFinal(currentStates[stateIdx]):
                numStepsToFinalState[stateIdx] = numSteps
                # remove the state from the list
                del unfinishedStateIndices[i]
            else:
                # go to next state only if we didn't remove a state from the list
                i += 1
        
        # stop once we reached the end for all states
        if len(unfinishedStateIndices) == 0:
            break
    
    return numStepsToFinalState
    

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
    numStepsToFinalState = computeNumStepsToFinalStateV2(startingStates, moves, transitions)
    # ALTERNATIVE:
    #numStepsToFinalState = computeNumStepsToFinalStateV1(startingStates, moves, transitions)
    
    # and the final result is then the least common multiple of these numbers
    result = lcm(numStepsToFinalState[0], numStepsToFinalState[1])
    for i in range(2, len(numStepsToFinalState)):
        result = lcm(result, numStepsToFinalState[i])
    
    # and give the result
    print(f"It takes {result} steps to reach ending states simultaneously from all states starting in 'A'")
    # ANSWER: 16342438708751