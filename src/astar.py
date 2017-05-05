#! /bin/bash
import math
import csv
import time
class Cell(object):
    def __init__(self,location,wall=False):
        self.children=[]
        self.parent=None
        self.location=location
        self.value = 0
        self.wall=wall


class priorityQueue(object):
    def __init__(self):
        self.empty = True
        self.queue=[]

    def push(self,value,cell):
        self.empty = False;
        self.queue.append([value,cell])
        #sort by value
        self.queue.sort(key=lambda tup: tup[0])
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
        self.start=self.get_cell([start[0],start[1]])
        self.goal= self.get_cell([goal[0],goal[1]])

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
        loc = x * self.cols + y
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
    def update_cell(self,next,current):
        next.value = current.value+10
        next.value += self.get_huristic(next)
        next.parent = current

    def get_huristic(self,cell):
        return math.sqrt(math.pow(cell.location[0] - self.goal.location[0], 2) + math.pow(cell.location[1] - self.goal.location[1], 2))
    def save_path(self):
        steps=[]
        cell = self.goal
        while cell.parent != None:
            cell = cell.parent
            steps.append(cell.location)
        return steps
    def main(self):
        self.opened.push(0,self.start)
        self.opened.queue[0]
        while not self.opened.empty:
            value, cell = self.opened.pop()
            self.closed.append(cell)
            if cell.location == self.goal.location:
                print "done getting directions"
                print time.localtime(time.time()), "finished finding path"
                return  self.save_path()
            neighbors = self.get_neighbors(cell)
            for neighbor in neighbors:
                if neighbor not in self.closed:
                    if not neighbor.wall:
                        if (neighbor.value,neighbor) in self.opened.queue:
                            if neighbor.value > cell.value + 10:
                                self.update_cell(neighbor,cell)
                        else:
                            self.update_cell(neighbor,cell)
                            self.opened.push(neighbor.value,neighbor)

