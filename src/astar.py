#! /bin/bash
from Queue import PriorityQueue
import math

class Cell(object):
    def __init__(self,location,wall=False):
        self.children=[]
        self.parent=None
        self.location=location
        self.value = 0
        self.wall=wall


class AStar(object):
    def __init__(self,cells):
        print "initliazing astar"
        self.opened=PriorityQueue()
        self.closed=[]
        self.cells=cells
        self.rows=0
        self.cols=0

    def init_world(self,start,goal,rows,cols):
        print "in init world"
        self.start=self.get_cell([start[0],start[1]])
        self.goal= self.get_cell([goal[0],goal[1]])
        self.rows=rows
        self.cols=cols
        print "done with world world"

    def get_cell(self,location):
        print location[0]
        x= location[0]
        y=location[1]
        return self.cells[x * self.rows + y]


    def get_neighbors(self,cell):
        neighbors = []
        location = cell.location
        if (location[0] - 1) >= 0:
                neighbors.append(self.get_cell([location[0] - 1, location[1]]))
        if (location[0] + 1) < self.rows:
                neighbors.append(self.get_cell([location[0] + 1, location[1]]))
        if (location[1] - 1) >= 0:
                neighbors.append(self.get_cell([location[0], location[1] - 1]))
        if (location[1] + 1) < self.cols:
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
        steps=[]
        cell = self.goal
        while cell.parent.location is not self.start.location:
            cell = cell.parent
            steps.append(cell.location)
            print 'path: cell: ', cell.location
        return steps
    def main(self):
        print "inside main"
        self.opened.put((0,self.start))
        while len(self.opened.queue)>0:
            print "in while"
            value, cell = self.opened.get()
            self.closed.append(cell)
            if cell.location is self.goal.location:
                return  self.save_path()
            neighbors = self.get_neighbors(cell)
            for neighbor in neighbors:
                if neighbor not in self.closed:
                    if (neighbor.value,neighbor.location) in self.opened.queue:
                        if neighbor.value > cell.value + 10:
                            self.update_cell(neighbor,cell)
                    else:
                        self.update_cell(neighbor,cell)
                        self.opened.put((neighbor.value,neighbor))



# grid = [[0, 0, 0, 0, 0, 100],
#         [100, 100, 0, 0, 0, 100],
#         [0, 0, 0, 100, 0, 0],
#         [0, 100, 100, 0, 0, 100],
#         [100, 100, 0, 0, 100, 0],
#         [0, 0, 0, 0, 0, 0]]
# a = AStar(grid,[0,0],[5,0])
# a.main()
