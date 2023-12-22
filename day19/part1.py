
from typing import Callable, Union

INPUT_FILE = "input.txt"
OPERATORS = [">", "<"]

def parseCondition(strCondition: str) -> Callable:
    """ Given the string representing a condition, return a function that can be called and expresses that condition.
    For example, for strCondition = "m>2090",
        it would return a function which checks whether the "m" value of the input argument is above 2090
    """
    # 1) split the condition up into the variable, the operator and the value
    i = 0
    while (i < len(strCondition) and strCondition[i] not in OPERATORS):
        i += 1
    var = strCondition[:i]
    op = strCondition[i]
    value = int(strCondition[i+1:])
    
    # 2) create and return the result function based on the operator
    match op:
        case ">":
            return lambda item: item[var] > value
        case "<":
            return lambda item: item[var] < value

def parseRules(strRules: str) -> tuple[Union[Callable, str]]:
    """ Parse the given rule set to a list of tuples.
        Each tuple contains at:
        - index 0: a function to check if the rule is applicable
        - index 1: the state to transition to
    """
    rules = []
    while strRules != "":
        # 1) isolate the next rule by finding until where it goes
        j = 0
        while (j < len(strRules) and strRules[j] != "," and strRules[j] != "}"):
            j += 1
        # 2) split it into the next rule and the remaining rules
        nextRule = strRules[:j]
        strRules = strRules[min(j+1, len(strRules)):]
        # 3) split up the rule into condition and destination state
        condition = None
        destState = None
        if ":" in nextRule:
            # rules with condition
            condition, destState = nextRule.split(":")
            condition = parseCondition(condition)
        else:
            # rules without condition
            condition = lambda item: True
            destState = nextRule
        
            # set the remaining rules to empty string as any rules after this will be ignored
            strRules = ""
        
        # 4) add the transition rule to the list
        rules.append((condition, destState))
   
    # 5) once we have generated all rules, return the full list
    return rules

def parsePart(strPart: str) -> dict[str, int]:
    """ Parses the given part to a dictionary with:
        - key = part attribute ("x", "m", "a" or "s")
        - value = value of that attribute
        
        Example input:
            "{x=787,m=2655,a=1222,s=2876}"
        returns as output:
            {"x": 787, "m": 2655, "a": 1222, "s": 2876}
    """
    part = {}
    # remove opening and closing brackets
    strPart = strPart[1:-1]
    # split into the different parts
    partAttributes = strPart.split(",")
    for attribute in partAttributes:
        # extract the info from the attribute
        var, value = attribute.split("=")
        value = int(value)
        # and save it in the part dictionary
        part[var] = value
    
    return part

def parseData(data: list[str]) -> tuple[Union[dict[str, list[tuple[Union[Callable, str]]]], dict[str, int]]]:
    """ Given the input data, parse and return the transition rules and parts.
        The transition rules will be in a format such as the example below:
            ex{x>10:one,m<20:two,a>30:R,A}
        which means that:
        from state "ex", if the part's "x" value is larger than 10, transition to state "one"
        otherwise, if the part's "m" value is less than 20, transition to state "two"
        ...
        lastly, if none of the previous rules apply, transition to state "A"
        
        The parts will be in a format such as the example below:
            {x=787,m=2655,a=1222,s=2876}
        which gives the values of the "x", "m", "a" and "s" attributes of the part.
        
        In the output, the transitions will be given as a dictionary with 
        - key=current state, 
        - value=list of transition rules,
            where the list items are tuples with:
            - index 0=function corresponding to the condition
            - index 1=state to transition to
        And the parts will be given as a list of dictionaries, with each dictionary corresponding to 1 part:
        - key=part attribute ("x", "m", "a" or "s")
        - value=value of that attribute
        
        These two parts will be returned, combined together in a tuple.
    """
    # 1) parse the transitions
    transitions = {}
    i = 0
    # iterate over rules until we hit an empty line, which separates the rules and the parts
    while (i < len(data) and data[i] != ""):
        startState, rules = data[i].split("{")
        parsedRules = parseRules(rules)
        transitions[startState] = parsedRules
        
        i += 1
    
    # 2) skip the empty line
    i += 1
    
    # 3) parse the parts
    parts = []
    while (i < len(data)):
        nextPart = data[i]
        parsedPart = parsePart(nextPart)
        parts.append(parsedPart)
        
        i += 1
    
    # 4) return the result
    return (transitions, parts)

def performStateTransition(state: str, part: dict[str, int], transitions: dict[Callable, str]) -> str:
    """ Perform one state transition from the given state with the given part """
    # 1) look up the transition rules for this state
    stateTransitions = transitions[state]
    # 2) go through the rules until one applies
    for rule in stateTransitions:
        condition, destState = rule
        if condition(part):
            return destState
    # 3) sanity check: if we reach this, no rule was applicable, which should never happen,
    #   as the last rule normally has no condition
    raise Exception(f"Found no valid transition from state \"{state}\"")


with open(INPUT_FILE, 'r') as f:
    # 1) parse the data
    # 1.1) read in the input, removing leading/trailing whitespace characters
    data = [l.strip() for l in f.readlines()]
    # 1.2) parse the data to python representations
    transitionRules, parts = parseData(data)
    
    # 2) simulate the transition for each part,
    #       doing the sum of the attributes of all the accepted parts
    sumAcceptedParts = 0
    for p in parts:
        # 2.1) initialize the state to starting state
        state = "in"
        # 2.2) simulate the start until we hit a terminal state
        terminalStates = ["A", "R"]
        while state not in terminalStates:
            state = performStateTransition(state, p, transitionRules)
        # 2.3) if the terminal state was the accept state, add the part to the sum
        if state == "A":
            sumAcceptedParts += sum(list(p.values()))
    
    # 3) return result
    print(f"The sum of the attribute values of all accepted parts is {sumAcceptedParts}")
    # ANSWER: 480738