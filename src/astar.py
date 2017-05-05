#! /bin/bash
import math
import csv
import time
class Cell(object):
    def __init__(self,location,wall=False):
        self.children=[]
        self.parent=None
        self.location=location
        self.g = 9999999999
        self.f = 9999999999
        self.wall=wall


class priorityQueue(object):
    def __init__(self):
        self.empty = True
        self.queue=[]

    def push(self,cell):
        self.empty = False;
        self.queue.append(cell)
        #sort by value
        self.queue.sort(key=lambda cell: cell.f, reverse=True)
    def pop(self):
        if not self.empty:
            elem =  self.queue.pop(len(self.queue)-1)
            if len(self.queue)==0:
                self.empty =True
            return elem
        else:
            return False



class AStar(object):
    def __init__(self,cells):
        self.opened=priorityQueue()
        self.closed=[]
        self.cells=cells
        self.rows=0
        self.cols=0
        self.init = False

    def init_world(self,start,goal,rows,cols):
        print "in init world"
        self.rows=rows
        self.cols=cols
        self.goal= self.get_cell([goal[0],goal[1]])
        self.start=self.get_cell([start[0],start[1]])
        self.start.g=0
        self.start.f=self.get_huristic(self.start)

        if self.start.wall:
            print "start loc is a wall"
            return False
        if self.goal.wall:
            print "goal loc is a wall"
            return False
        self.init= True

        print "done with world world"

    def get_cell(self,location):
        x= location[0]
        y=location[1]
        loc = x * self.cols+ y
        return self.cells[loc]

    def get_neighbors(self,cell):
        neighbors = []
        location = cell.location
        if (location[0] - 1) >= 0:
                n = self.get_cell([location[0] - 1, location[1]])
                if not n.wall:
                    neighbors.append(n)
        if (location[0] + 1) < self.rows:
            n = self.get_cell([location[0] + 1, location[1]])
            if not n.wall:
                neighbors.append(n)
        if (location[1] - 1) >= 0:
            n = self.get_cell([location[0], location[1]-1])
            if not n.wall:
                neighbors.append(n)
        if (location[1] + 1) < self.cols:
            n = self.get_cell([location[0] , location[1]+1])
            if not n.wall:
                neighbors.append(n)
        cell.children=neighbors
        return neighbors

    def get_huristic(self,cell):
        return math.sqrt(math.pow(cell.location[0] - self.goal.location[0], 2) + math.pow(cell.location[1] - self.goal.location[1],2))

    def get_distance(selfs, cell1, cell2):
        return math.sqrt(math.pow(cell1.location[0] - cell2.location[0], 2) + math.pow(cell1.location[1] - cell2.location[1], 2))


    def save_path(self):
        steps=[]
        cell = self.goal
        while cell.parent != None:
            steps.append(cell.location)
            cell = cell.parent
        return list(reversed(steps))

    def main(self):
        self.opened.push(self.start)

        while not self.opened.empty:
            current = self.opened.pop()
            self.closed.append(current)
            if current == self.goal:
                print "done getting directions"
                print time.localtime(time.time()), "finished finding path"
                return  self.save_path()
            neighbors = self.get_neighbors(current)
            for neighbor in neighbors:
                if neighbor in self.closed:
                    continue
                t_g = current.g+self.get_distance(current,neighbor)
                if (neighbor) not in self.opened.queue:
                    self.opened.push(neighbor)
                elif (t_g>neighbor.g):
                    continue
                neighbor.parent=current
                neighbor.g=t_g
                neighbor.f = neighbor.g + self.get_huristic(neighbor)

#
#
# start = [72, 41]
# goal = [133, 56]
# cells = []
# tmp = []
# # rows = msg.info.height
# cells = []
# rows=0
# cols = 0
# with open('map_map(1).txt') as file:
# 	reader = csv.reader(file, delimiter=' ')
# 	rows = 0;
# 	for line in reader:
# 		if len(line) > cols:
# 			cols = len(line)
# 		for col in range(len(line)):
# 			data = int(line[col])
# 			if data == -1 or data == 1:
# 				wall = True
# 			else:
# 				wall = False
# 			cell = Cell([rows, col], wall)
# 			cells.append(cell)
#
# 		rows += 1
# rows -= 1
# a = AStar(cells)
# a.init_world(start, goal,rows,cols)
# directions = []
# if a.init:
#     print "getting directions"
#     directions = a.main()
#
#     for direction in directions:
#         print direction[0],direction[1],
#
# else:
#     print "no init"