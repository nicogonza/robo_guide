#!/usr/bin/env python
from matplotlib import pyplot as plt
import numpy as np
import csv

grid=[]
tmp = []
x=0
y=0
with open('brushfire_result.txt') as file:
    reader = csv.reader(file, delimiter=' ')
    for line in reader:
        
        for i in line:
            	if (i != "\n" and i != ""):
			if(i!="-1"):
                		tmp.append(y)
				grid.append(x)
		y=y+1
		
   	x=x+1
	

plt.plot(960,704)
plt.plot(grid,tmp)
plt.show()

