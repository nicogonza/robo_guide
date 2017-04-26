#! /bin/bash
from Queue import PriorityQueue
import math
class World(object):
    def __init__(self,grid):
        self.rows = len(grid)
        self.cols= len(grid[0])
        self.obs= []
        self.grid = grid
        self.getObs()


    def getObs(self):
        tovisit=[]
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == 100 or self.grid[row][col] == -1:
                    self.grid[row][col] = 1
                    tovisit.append([row, col])
        self.obs=tovisit

class Cell(object):
    def __init__(self,location,wall):
        self.children=[]
        self.parent=None
        self.location=location
        self.value = 0
        self.wall=wall


class AStar(object):
    def __init__(self,grid,start,goal):
        self.opened=PriorityQueue()
        self.closed=[]
        self.world = World(grid)
        self.cells=[]
        self.init_world(start,goal)

    def init_world(self,start,goal):
        for row in range(self.world.rows):
            for col in range(self.world.cols):
                if [row,col] in self.world.obs:
                    wall=True
                else:
                    wall=False
                self.cells.append(Cell([row,col],wall))
        self.start=self.get_cell([start[0],start[1]])
        self.goal= self.get_cell([goal[0],goal[1]])

    def get_cell(self,location):
        print location[0]
        x= location[0]
        y=location[1]
        return self.cells[x * self.world.rows + y]


    def get_neighbors(self,cell):
        neighbors = []
        location = cell.location
        if (location[0] - 1) >= 0:
            t = self.world.grid[location[0] - 1][location[1]]
            if t != 1:
                neighbors.append(self.get_cell([location[0] - 1, location[1]]))
        if (location[0] + 1) < self.world.rows:
            t = self.world.grid[location[0] + 1][location[1]]
            if t != 1:
                neighbors.append(self.get_cell([location[0] + 1, location[1]]))
        if (location[1] - 1) >= 0:
            t = self.world.grid[location[0]][location[1] - 1]
            if t!= 1:
                neighbors.append(self.get_cell([location[0], location[1] - 1]))
        if (location[1] + 1) < self.world.cols:
            t = self.world.grid[location[0]][location[1] + 1]
            if t != 1:
                neighbors.append(self.get_cell([location[0], location[1] + 1]))
        cell.children=neighbors
        return neighbors
    def update_cell(self,next,current):
        next.value = current.value+10
        next.value += self.get_huristic(next)
        next.parent = current

    def get_huristic(self,cell):
        return math.sqrt(math.pow(cell.location[0] - self.goal.location[0], 2) + math.pow(cell.location[1] - self.goal.location[1], 2))
    def save_path(self):
        cell = self.goal
        while cell.parent.location is not self.start.location:
            cell = cell.parent
            print 'path: cell: ', cell.location
    def main(self):
        self.opened.put((0,self.start))
        while len(self.opened.queue)>0:
            value, cell = self.opened.get()
            self.closed.append(cell)
            if cell.location is self.goal.location:
                self.save_path()
                print "done"
                break
            neighbors = self.get_neighbors(cell)
            for neighbor in neighbors:
                if neighbor not in self.closed:
                    if (neighbor.value,neighbor.location) in self.opened.queue:
                        if neighbor.value > cell.value + 10:
                            self.update_cell(neighbor,cell)
                    else:
                        self.update_cell(neighbor,cell)
                        self.opened.put((neighbor.value,neighbor))


grid = [[0, 0, 0, 0, 0, 100],
        [100, 100, 0, 0, 0, 100],
        [0, 0, 0, 100, 0, 0],
        [0, 100, 100, 0, 0, 100],
        [100, 100, 0, 0, 100, 0],
        [0, 0, 0, 0, 0, 0]]
a = AStar(grid,[0,0],[5,0])
a.main()
