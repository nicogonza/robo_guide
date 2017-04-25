#!/usr/bin/env python
import csv
import numpy as np
import copy
import math


grid = []
columns = 0
with open('map.txt') as file:
    reader = csv.reader(file, delimiter=' ')
    for line in reader:
        tmp = []
        for i in line:
            if (i != "\n" and i != ""):
                tmp.append(int(i))
        grid.append(tmp)

newgrid = []
for line in grid:
    columns = len(line)

print(columns)

grid =[]
columns =0
with open('map.txt') as file:
    reader= csv.reader(file, delimiter= ' ')
    for line in reader:
	tmp = []
	for i in line:
		
		if i!="\n" and i!="":
	    		tmp.append(int(i))
	grid.append(tmp)

newgrid=[]
for line in grid:

		
	columns = len(line)
	
print columns


repulsive = copy.deepcopy(grid)
attgrid = copy.deepcopy(grid)
resultgrid = copy.deepcopy(grid)
rows = len(grid)
<<<<<<< HEAD



        

#
# grid = newgrid
# for row in range(rows+1):
#     for column in range(columns+1):
#          column
#         if grid[row][column] == 1:
#             newgrid[row][column] = 1
#             if row > 0 and column > 0 :
#                 newgrid[row][column] = 2
#         else:
#             print "in else"


def getNeighbors(grid, point, r, c):
    i = point
    c = c - 1
    neighbors = []
    if (i[0] - 1) >= 0:
        t = grid[i[0] - 1][i[1]]
        if t == 0:
            neighbors.append([i[0] - 1, i[1]])
    if (i[0] + 1) <= r:
        t = grid[i[0] + 1][i[1]]
        if t == 0:
            neighbors.append([i[0] + 1, i[1]])
    if (i[1] - 1) >= 0:
        t = grid[i[0]][i[1] - 1]
        if t == 0:
            neighbors.append([i[0], i[1] - 1])
    if (i[1] + 1) <= c:
        t = grid[i[0]][i[1] + 1]
        if t == 0:
            neighbors.append([i[0], i[1] + 1])
    minx = 999
    for a in neighbors:
        grid[a[0]][a[1]] = grid[point[0]][point[1]] + 1
    # update the current point to min of its neighbors
    return neighbors, grid


tovisit = []
for row in range(rows):
    for col in range(columns):
        if grid[row][col] == 100:
            tovisit.append([row, col])
obsLoc = copy.deepcopy(tovisit)

while len(tovisit) > 0:
    n, g = getNeighbors(grid, tovisit[0], row, columns)
    tovisit.remove(tovisit[0])
    grid = g
    if len(n) > 0:
        for l in n:
            tovisit.append(l)

with open("brushfire_result.txt", "w") as text_file:
    writer = csv.writer(text_file, delimiter=' ')
    for row in range(0, len(grid)):
        writer.writerow(grid[row])


def calcRepulsive(grid, obsloc):
    for row in range(rows):
        for col in range(columns):
            if (grid[row][col] != -1):
                if (not ([row, col] in obsLoc)):

                    mindist = 99999
                    goalLoc = [0, 0]
                    for obs in obsloc:
                        dist = getDist(obs, [row, col])
                        if dist <= mindist:
                            mindist = dist
                            goalLoc = obs
                            # get degree to a point
                    grid[row][col] = mindist
                    print(str(row) + " " + str(col) + " " + str(mindist))


                else:
                    grid[row][col] = 0.0
    return grid


def getDist(loc1, loc2):
    return math.sqrt(math.pow(loc1[0] - loc2[0], 2) + math.pow(loc1[1] - loc2[1], 2))


getgrid = calcRepulsive(grid, obsLoc)

with open('repulsive_result.txt', 'w') as text:
    write = csv.writer(text, delimiter=' ')
    for row in range(0, len(getgrid)):
        write.writerow(getgrid[row])

##    print grid

userGoalX = len(grid) + 2
userGoalY = len(grid[0]) + 2

while (int(userGoalX) > len(grid)):
    userGoalX = input("Enter your x value here: ")
    userGoalX = int(userGoalX)

while (int(userGoalY) > len(grid[0])):
    userGoalY = input("Enter your y value here: ")
    userGoalY = int(userGoalY)

userGoal = [userGoalX, userGoalY]

newGrid = []

for r in range(len(getgrid)):
    temp = []
    result = 0.0
    temp2 = []
    for k in range(len(getgrid[r])):
        d = round(math.sqrt(math.pow(int(userGoalX) - r, 2) + math.pow(int(userGoalY) - k, 2)), 2)
        temp.append(d)
        if (getgrid[r][k] != -1 and getgrid[r][k] != 100):
            result = d - float(getgrid[r][k])
        else:
            result = getgrid[r][k]
        temp2.append(result)

    resultgrid.append(temp2)
    newGrid.append(temp)

# this will output the newGrid to a .txt file
with open('attractive_result.txt', 'w') as text:
    write = csv.writer(text, delimiter=' ')
    for row in range(0, len(newGrid)):
        write.writerow(newGrid[row])

with open('combined_result.txt', 'w') as text:
    write = csv.writer(text, delimiter=' ')
    for row in range(0, len(newGrid)):
        write.writerow(resultgrid[row])

gradGrid = []

for r in range(0, len(newGrid)):
    temp = []
    for k in range(0, len(newGrid[r])):

        N = math.pow(2, 31)
        E = math.pow(2, 31)
        S = math.pow(2, 31)
        W = math.pow(2, 31)

        if (r - 1 >= 0):
            N = newGrid[r - 1][k]

        if (r + 1 < len(newGrid)):
            S = newGrid[r + 1][k]

        if (k + 1 < len(newGrid[r])):
            E = newGrid[r][k + 1]

        if (k - 1 >= 0):
            W = newGrid[r][k - 1]

        G = min(N, S, E, W)

        if (G == N):
            temp.append('N')
        elif (G == S):
            temp.append('S')
        elif (G == E):
            temp.append('E')
        else:
            temp.append('W')

    gradGrid.append(temp)

print(np.matrix(gradGrid))


def calcAttractive(grid, goalLoc):
    for row in range(rows):
        for col in range(columns):
            if not (row == goalLoc[0] and col == goalLoc[1]):
                b = abs(goalLoc[0] - row)
                b = b / getDist([row, col], goalLoc)
                angle = math.asin(b)
                angle = math.degrees(angle)

                if row < goalLoc[0]:
                    if col < goalLoc[1]:
                        angle = 360 - angle
                    if col > goalLoc[1]:
                        angle = angle + 180
                    if col == goalLoc[1]:
                        angle = angle + 180
                if row > goalLoc[0]:
                    if col < goalLoc[1]:
                        angle = angle
                    if col > goalLoc[1]:
                        angle = 180 - angle
                    if col == goalLoc[1]:
                        angle = angle
                if row == goalLoc[0]:
                    if col < goalLoc[1]:
                        angle = angle
                    if col > goalLoc[1]:
                        angle = 180 - angle
                grid[row][col] = int(round(angle))

    return grid


print("printing attraction\n")
print(np.matrix(calcAttractive(attgrid, [userGoalX, userGoalY])))
getgrid = calcAttractive(attgrid, [userGoalX, userGoalY])
for r in range(rows):
    for c in range(columns):
        if getgrid[r][c] == 100:

            print(str((r, c)) + "repulsive direction: obstacle")
        else:
            print(str((r, c)) + "attractive direction: " + str(getgrid[r][c]) + " degrees")
=======
            print str((r, c)) + "repulsive direction: obstacle"
        else:
            print str((r,c)) + "attractive direction: "+str(getgrid[r][c])+" degrees"

