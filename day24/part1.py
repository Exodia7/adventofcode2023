
INPUT_FILE = "input.txt"

MIN_X = MIN_Y = 200000000000000 # 7 for test.txt
MAX_X = MAX_Y = 400000000000000 # 27 for test.txt

DEBUG = False

def moveOneStep(pos: list[int], velocity: list[int]) -> list[int]:
    """ Computes the position one step further in time """
    return [pos[dim] + velocity[dim] for dim in range(len(pos))]

def computePosAtTime(pos: list[int], velocity: list[int], time: int) -> list[int]:
    """ Computes the position of the trajectory at the given time in the future """
    return [pos[dim] + velocity[dim] * time for dim in range(len(pos))]

def doTrajectoriesIntersect(posA: list[int], velocA: list[int], posB: list[int], velocB: list[int]) -> bool:
    """ Compute whether given objects A and B intersect on their trajectories exactly once.
        Note that if A and B have the exact same position and velocity, 
        they would have an infinite number of intersections, so that case leads to an Exception.
        
        Otherwise, the trajectories intersect if, given 
        - posA = [x_A, y_A, z_A], velocA = [vx_A, vy_A, vz_A]
        - posB = [x_b, y_B, z_B], velocB = [vx_B, vy_B, vz_B]
        
        the following system of equations has a solution for t:
        { x_A + vx_A * t1 = x_B + vx_B * t2
        { y_A + vy_A * t1 = y_B + vy_B * t2
        Equation 1: 
            { x_A + vx_A * t1 = x_B + vx_B * t2
            <=> { t1 * vx_A = x_B - x_A + vx_B * t2
            <=> { t1 = (x_B - x_A + vx_B * t2)/vx_A
        Insert into equation 2:
            { y_A + vy_A * t1 = y_B + vy_B * t2
            <=> { y_A + vy_A/vx_A * (x_B - x_A + vx_B * t2) = y_B + vy_B * t2
            <=> { t2 * (vy_A * vx_B)/vx_A - t2 * vy_B = y_B - y_A - vy_A/vx_A * (x_B - x_A)
            <=> { t2 * (vy_A * vx_B - vy_B * vx_A)/vx_A = y_B - y_A - vy_A/vx_A * (x_B - x_A)
            <=> { t2 = (vx_A * (y_B - y_A) - vy_A * (x_B - x_A))/(vy_A * vx_B - vy_B * vx_A)
        
        Note also that the position of A and B at those times need to be within the allowed range of X and Y positions.
    """
    if posA == posB and velocA == velocB:
        raise ValueError("Trajectories of the same object intersect an infinite number of times")
    else:
        # 1) extract all interesting values
        xA, yA, _ = posA
        vxA, vyA, _ = velocA
        xB, yB, _ = posB
        vxB, vyB, _ = velocB
        # 2) check if the lines are parallel or not
        if (vyA * vxB - vyB * vxA == 0):
            if (DEBUG): print("Trajectories are parallel")
            return False
        # 3) compute the times of intersection on X and on Y
        #   based on equations from the docstring.
        #   t2 = intersectTimeB  ,  t1 = intersectTimeA
        intersectTimeB = (vxA * (yB - yA) - vyA * (xB - xA))/(vyA * vxB - vyB * vxA)
        intersectTimeA = (xB - xA + vxB * intersectTimeB)/vxA
        # 4) check if both of those times are in the future
        if intersectTimeB < 0 or intersectTimeA < 0:
            if (DEBUG): print("Intersection is in the past")
            return False
        # 5) compute positions at which A and B intersect
        #   and check that both are within the allowed range
        intersectPos = computePosAtTime(posA, velocA, intersectTimeA)
        intersectX, intersectY, _ = intersectPos
        if (MIN_X <= intersectX <= MAX_X and MIN_Y <= intersectY <= MAX_Y):
            if (DEBUG): print(f"Trajectories intersect at x={intersectX}, y={intersectY}!")
            return True
        else:
            if (DEBUG): print("Intersection is out of the test area")
            return False
        
        '''
        timeOfIntersect = None
        if vxA != vxB and vyA != vyB:
            # Case 2.1) neither of the velocities are the same, so we can safely compute intersections
            intersectTimeOnX = (xB - xA)/(vxA - vxB)
            intersectTimeOnY = (yB - yA)/(vyA - vyB)
            
            if intersectTimeOnX != intersectTimeOnY or intersectTimeOnX < 0:
                # there is no intersection in the future
                if (DEBUG):
                    if intersectTimeOnX != intersectTimeOnY:
                        print("No intersection of trajectories")
                    else:
                        print("Intersection of trajectories is in the past #1")
                return False
            else:
                # save the time of intersection
                timeOfIntersect = intersectTimeOnX
        elif vxA == vxB and xA == xB:
            # Case 2.2) x always intersects, we just need to find intersect on y
            intersectTimeOnY = (yB - yA)/(vyA - vyB)
            
            if intersectTimeOnY < 0:
                # intersection would be in the past
                if (DEBUG): print("Intersection of trajectories is in the past #2")
                return False
            else:
                # save the time of intersection
                timeOfIntersect = intersectTimeOnY
        elif vyA == vyB and yA == yB:
            # Case 2.3) y always intersects, we just need to find intersect on x
            intersectTimeOnX = (xB - xA)/(vxA - vxB)
            
            if intersectTimeOnX < 0:
                # intersection would be in the past
                if (DEBUG): print("Intersection of trajectories is in the past #3")
                return False
            else:
                # save the time of intersection
                timeOfIntersect = intersectTimeOnX
        else:
            # Case 2.4) impossible to intersect, lines run in parallel
            if (DEBUG): print("Trajectories are parallel - no intersection")
            return False
        
        # 3) check that the positions at which A and B intersect are within the allowed range
        # NOTE: only need to check once, as both A and B will be at the same position at this time
        intersectX = xA + timeOfIntersect * vxA
        if intersectX < MIN_X or intersectX > MAX_X:
            print(f"X of intersection is outside of test area")
            return False
        intersectY = yA + timeOfIntersect * vyA
        if intersectY < MIN_Y or intersectY > MAX_Y:
            if (DEBUG): print(f"Y of intersection is outside of test area")
            return False
        
        # 4) if we reach this, we passed all checks and we do intersect
        return True
        '''




with open(INPUT_FILE, 'r') as f:
    # 1) parse data
    data = [[[int(n) for n in nums.split(",")] for nums in l.strip().split("@")] for l in f.readlines()]
    
    if (DEBUG):
        print("HAILSTONES:")
        for i in range(len(data)):
            print(f"{i} - {data[i]}")
        print()
    
    # 2) for every pair of datapoints, check if their trajectories intersect, counting the total number of intersecting pairs
    numIntersections = 0
    for p1 in range(len(data)):
        pos1, veloc1 = data[p1]
        for p2 in range(p1+1, len(data)):
            pos2, veloc2 = data[p2]
            if (DEBUG): print(f"For hailstones #{p1} and #{p2}: ", end='')
            
            if doTrajectoriesIntersect(pos1, veloc1, pos2, veloc2):
                numIntersections += 1
    
    if (DEBUG): print("\n")
    
    # 3) return result
    print(f"There are {numIntersections} intersections of hailstones in the test area from {MIN_X} to {MAX_X}")
    # ANSWER: 