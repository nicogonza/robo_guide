import csv
import math


grid=[]
columns=0
with open("repulsive_result.txt") as file:
    reader = csv.reader(file, delimiter=' ')

    for line in reader:
        tmp = []
        for i in line:
            if(i!='\n' and i!='' and len(i)!=0):
                tmp.append(float(i))

        if(len(tmp)!=0):
            grid.append(tmp)



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
resultgrid = []
for r in range(len(grid)):
    temp = []
    result = 0.0
    temp2 = []
    for k in range(len(grid[r])):
        d = round(math.sqrt(math.pow(int(userGoalX) - r, 2) + math.pow(int(userGoalY) - k, 2)), 2)
        temp.append(d)
        if (grid[r][k] != -1 and grid[r][k] != 100):
            result = d - float(grid[r][k])
        else:
            result = grid[r][k]
        temp2.append(result)

    resultgrid.append(temp2)
    newGrid.append(temp)

# this will output the newGrid to a .txt file
with open('attractive_result.txt', 'w') as text:
    write = csv.writer(text, delimiter=' ')
    for row in range(0, len(newGrid)):
        write.writerow(newGrid[row])
    text.close()

with open('combined_result.txt', 'w') as text:
    write = csv.writer(text, delimiter=' ')
    for row in range(0, len(resultgrid)):
        write.writerow(resultgrid[row])
    text.close()
start=[307,209]
print(str(resultgrid[userGoalX][userGoalY]))

def getPath(start,goal,grid,stepsize):

    current=start
    path=[current]
    row = grid[start[0]]
    elem = row[start[1]]

    looper=0

    while(current[0]!=goal[0] or current[1]!=goal[1]):
        surroundings = []
        for i in range(0, stepsize):
            point1 = [current[0] + i, current[1]]
            point2 = [current[0] - i, current[1]]
            point3 = [current[0], current[1] + i]
            point4 = [current[0], current[1] - i]
            point5=[current[0]-i, current[1] - i]
            point6 = [current[0] - i, current[1] + i]
            point7 = [current[0] + i, current[1] - i]
            point8 = [current[0] + i, current[1] + i]
            surroundings.append(point1)
            surroundings.append(point2)
            surroundings.append(point3)
            surroundings.append(point4)
            surroundings.append(point5)
            surroundings.append(point6)
            surroundings.append(point7)
            surroundings.append(point8)
        min=100000
        directions=[]
        for p in surroundings:
            if(min>grid[p[0]][p[1]] and grid[p[0]][p[1]]!=-1.0):

                current=p
                min=grid[p[0]][p[1]]
        path.append(current)


        looper=looper+1
        if (looper>980):
            break
    return path

i=1
road= getPath(start,userGoal,resultgrid,i)

while(road[len(road)-1]!=userGoal):
    road = getPath(start, userGoal, resultgrid, i)
    i=i+1


with open('Path.txt', 'w') as text:
    #text.write('Start '+str(start)+' goal: '+str(userGoal)+'\n')
    #text.write('Step Size: '+str(i)+'\n')
    for row in range(0, len(road)):
        text.write(str(road[row][0])+' '+str(road[row][1]))
        text.write('\n')

    text.close()



