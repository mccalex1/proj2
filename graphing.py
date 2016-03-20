# Author :          Alex McCaslin
# Date Modified:    3/12/2016
# Email:            mccalex1@umbc.edu

import sys
import math
import random

import matplotlib.pyplot as plt
import numpy as np

from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

from mpl_toolkits.mplot3d import Axes3D

def main():     

     argList = sys.argv

     #command line arguments
     step_size = float(argList[1])
     xmin = float(argList[2])
     xmax = float(argList[3])
     ymin = float(argList[4])
     ymax = float(argList[5])

     if len(argList) != 6:
          print("Arguments must follow (step_size) (xmin) (xmax) (ymin) (ymax)")
          exit()

     #set restarts and temp for two functions
     num_restarts = int(input("How many restarts would you like to take for hill climbing: "))
     max_temp = float(input("Enter a max temperature: "))


     ######### matplotlib.org/examples/mplot3d/surface3d_demo.html     
     theFig = plt.figure()
     theFig1 = plt.figure()
     theFig2 = plt.figure()

     #create multiple plots
     ax0 = theFig.gca(projection='3d')
     ax1 = theFig1.gca(projection='3d')
     ax2 = theFig2.gca(projection='3d')

     #set ranges
     X = np.arange(xmin, xmax, .1)
     Y = np.arange(ymin, ymax, .1)

     X, Y = np.meshgrid(X,Y)

     #get equation for graph
     R = np.sqrt(X**2 + Y**2)
     Z = np.sin((X**2 + 3*(Y**2))) / (.1 + R**2)  +  ((X**2 + 5*(Y**2))  *  (np.exp(1-R**2) / 2))

     #set up plots
     surf = ax0.plot_surface(X, Y, Z, rstride = 1, cstride = 1, cmap=cm.autumn_r, linewidth = 0, antialiased = False)
     surf = ax1.plot_surface(X, Y, Z, rstride = 1, cstride = 1, cmap=cm.autumn_r, linewidth = 0, antialiased = False)
     surf = ax2.plot_surface(X, Y, Z, rstride = 1, cstride = 1, cmap=cm.autumn_r, linewidth = 0, antialiased = False)

     #set graph size
     ax0.set_zlim(-3,3)
     ax1.set_zlim(-3,3)
     ax2.set_zlim(-3,3)

     theFig.colorbar(surf, shrink=.5, aspect=5)
     theFig1.colorbar(surf, shrink=.5, aspect=5)
     theFig2.colorbar(surf, shrink=.5, aspect=5)
     ##########      

     #call functions
     x0, y0, z0, pathX, pathY, pathZ = hill_climb(func_to_opt, step_size, xmin, xmax, ymin, ymax)
     ax0.plot(pathX, pathY, pathZ)

     x1, y1, z1, pathX, pathY, pathZ= hill_climb_rand(func_to_opt, step_size, num_restarts, xmin, xmax, ymin, ymax)
     ax1.plot(pathX, pathY, pathZ, 'bo', markersize=1)

     x2, y2, z2, pathX, pathY, pathZ = simulated_annealing(func_to_opt, step_size, max_temp, xmin, xmax, ymin, ymax)
     ax2.plot(pathX, pathY, pathZ, 'bo', markersize=1)
     ax2.plot([pathX[-1]], [pathY[-1]], [pathZ[-1]], 'bo', markersize=5)
 
     plt.show()

     print("Min Z value for hill climbing was at " + str(x0) + " , " + str(y0) + " , " + str(z0))
     print("Min Z value for hill climbing with random restarts was at " + str(x1) + " , " + str(y1) + " , " + str(z1))
     print("Min Z value for simulated annealing was at " + str(x2) + " , " + str(y2) + " , " + str(z2))
     print()
     return 0
    
def hill_climb(func_to_opt, step_size, xmin, xmax, ymin, ymax):
     x = xmax
     y = ymax
     z = func_to_opt(x, y)

     pathX = []
     pathY = []
     pathZ = []

     #flag allows me to end whenever theres nowhere to move down
     flag = True

     while flag:

          pathX.append(x)
          pathY.append(y)
          pathZ.append(z)

          #makes sure x is within bounds
          if(x - step_size > xmin):
               tempX = x - step_size
          else:
               tempX = x

          #makes sure y is within bounds
          if(y - step_size > ymin):
               tempY = y - step_size
          else:
               tempY = y

          #checks values around current x and y
          if(func_to_opt(tempX, y) < func_to_opt(x, y)) and (func_to_opt(tempX, y) <= func_to_opt(x, tempY)):
               x = tempX
               z = func_to_opt(tempX, y)
               
          elif(func_to_opt(x, tempY) < func_to_opt(x, y)) and (func_to_opt(x, tempY) < func_to_opt(tempX, y)):
               y = tempY
               z = func_to_opt(x, tempY)
               
          else:
               flag = False



     return x, y, z, pathX, pathY, pathZ

def hill_climb_rand(func_to_opt, step_size, num_restarts, xmin, xmax, ymin, ymax):

     
     x = random.uniform(xmin, xmax)
     y = random.uniform(ymin, ymax)

     #account for first case
     xLow , yLow, zLow, tempx, tempy, tempz = hill_climb(func_to_opt, step_size, xmin, x, ymin, y)

     count = 0

     pathX = []
     pathY = []
     pathZ = []
     
     #append each value to list
     for i in range(len(tempx)):
          pathX.append(tempx[i])
          pathY.append(tempy[i])
          pathZ.append(tempz[i])

     #do it num_restarts amount of times more
     while count < num_restarts:
          x = random.uniform(xmin, xmax)
          y = random.uniform(ymin, ymax)
          
          x1,y1,z1, tempx, tempy, tempz = hill_climb(func_to_opt, step_size, xmin, x, ymin, y)
          
          if(z1 < zLow):
               xLow = x1
               yLow = y1
               zLow = z1


          count += 1
          
          for i in range(len(tempx)):
               pathX.append(tempx[i])
               pathY.append(tempy[i])
               pathZ.append(tempz[i])
          
     return xLow, yLow, zLow, pathX, pathY, pathZ

def simulated_annealing(func_to_opt, step_size, max_temp, xmin, xmax, ymin, ymax):
     x = xmax
     y = ymax
     z = func_to_opt(x, y)

     multiplier= .99

     pathX = []
     pathY = []
     pathZ = []

     #pick random spot on graph
     x = random.uniform(xmin, xmax)
     y = random.uniform(ymin, ymax)
     pathX.append(x)
     pathY.append(y)

     z = func_to_opt(x,y)

     pathZ.append(z)
     tempX = x
     tempY = y
     tempZ = z

     #http://katrinaeg.com/simulated-annealing.html

     #temperature can't ever reach 0
     while max_temp > .00001:
          tempX = random.uniform(xmin, xmax)
          tempY = random.uniform(ymin, ymax)
          tempZ = func_to_opt(tempX, tempY)

          changeZ = -1 * (tempZ - z) 

          annealing = math.exp(changeZ / max_temp)
          
          #compare to probability
          if random.uniform(0, 1) < annealing:
               x = tempX
               y = tempY
               z = tempZ

               pathX.append(x)
               pathY.append(y)
               pathZ.append(z)

          max_temp *= multiplier


     return x , y, z, pathX, pathY, pathZ


#takes function given and returns a z value
def func_to_opt(x, y):

     r = math.sqrt(math.pow(x,2) + math.pow(y,2))
     
     #split up equation
     stepA = math.sin(math.pow(x,2) + (3 * math.pow(y,2)))  /  (.1 + math.pow(r,2))
     stepB = math.pow(x,2) + (5 * math.pow(y,2))
     stepC = math.exp(1 - math.pow(r, 2))  /  2
     
     z = stepA + stepB * stepC

     return z 

main()
