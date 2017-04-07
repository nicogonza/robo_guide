#! /bin/bash
map =[[100 100 100 100 100 100 100 100],
      [100 100 0 0 0 100 100 100],
      [100 100 0 0 100 100 100 100],
      [100 100 0 0 0 0 0 100],
      [100 100 0 0 0 0 0 100],
      [100 100 100 100 0 0 100 100],
      [100 100 100 100 0 0 0 100],
      [100 100 100 100 100 0 0 100],
      [100 100 100 100 100 0 0 100],
      [100 100 100 100 100 0 0 100],
      [100 100 100 100 100 0 0 0]]
aStarSearch(map)

def aStarSearch(map):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    visited = []
    q = util.PriorityQueue()
    q.push((problem.getStartState(), []), 0)
    directions = []
    while not q.isEmpty():
        current, path = q.pop()
        if current not in visited:
            visited.append(current)
            if problem.isGoalState(current):
                directions = path
                break
            for state, direction, step in problem.getSuccessors(current):
                if state not in visited:
                    # Access path thus far and append the successor direction.
                    updatePath = path + [direction]
                    # Push successor and updated path onto frontier
                    # Cost is cost of path + heuristic
                    q.push((state, updatePath), problem.getCostOfActions(updatePath)+heuristic(state,problem))

    return directions

