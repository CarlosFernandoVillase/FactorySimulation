# Make sure to use the command pip install simpy
# And after running the simulation it will ask you if you want to see the data of every single day, type "y" for yes and "n" for no

import numpy as np
import matplotlib.pyplot as plt
import simpy
import random
from enum import Enum
import os
from time import sleep

class Day(object):
    def __init__(self, dayNumber, TOP) -> None:
        self.dayNumber = dayNumber
        self.TOP = TOP
        self.done = 0
        self.fail = 0
        self.OLP = 0

    def count(self,products):
        W=0
        L=0
        for product in products:
          if product == "done":
            W+=1
          elif product == "fail":
            L+=1
        return W, L

    def simulate_day(self, OLP):
        x =random.choices(["done", "fail"], weights = [.97, .03], k = round(random.normalvariate(100, 5)))
        self.done, self.fail = self.count(x)
        self.OLP = OLP - self.done
        if self.OLP < 0:
          self.OLP = 0
        return self.OLP

    def calculateTotal(self,doneTot,failTot):
        doneTot += self.done
        failTot += self.fail
        return doneTot,failTot

    def getPerformance(self):
        return self.done, self.fail, self.dayNumber

    def display_status(self):
        print(f"Day {self.dayNumber}:")
        print(f"Total orders planned: {self.TOP}")
        print(f"Produced items: {self.done}")
        print(f"Failed items: {self.fail}")
        print(f"Orders left planned: {self.OLP}")
        print() 


class Factory(object):
    def __init__(self, TOP) -> None:
        self.days = []
        self.TOP = TOP


    def simulate_business(self):
        OLP = TOP
        i = 1
        while OLP > 0:
            day = Day(i, self.TOP)
            OLP = day.simulate_day(OLP)
            self.days.append(day)
            i += 1
        print("======================")
        print("Simulation Successful")
        print(f"All Orders have been completed in {i-1} days")
        print()

    def calculateTotal(self,doneTot,failTot):
        for day in self.days:
            doneTot,failTot = day.calculateTotal(doneTot,failTot)
        return doneTot,failTot

    def getPerformance(self,y1,y2,x):
        for day in self.days:
            Ry1,Ry2,Rx = day.getPerformance()
            y1.append(Ry1)
            y2.append(Ry2)
            x.append(Rx)
        return y1,y2,x
        

    def display_status(self):
        for day in self.days:
            day.display_status()
            sleep(1)

# Initial variables
TOP = 5000 # Total orders planned
array= []
doneTot=0
failTot=0

# Run the factory simulation
factory = Factory(TOP)
factory.simulate_business()

# Graphs
doneTotT,failTotT = factory.calculateTotal(doneTot,failTot)

def percentage(x,y):
  return round(((x)/(x+y))*100,2)

y1 = []
y2 = []
x = []

R1, R2, RX = factory.getPerformance(y1,y2,x)
  
# plot lines 
plt.style.use('dark_background')

plt.plot(RX, R1, color=(.1,.9,.1) ,label = "Success") 
plt.plot(RX, R2, color=(1,.2,.2),label = "Errors") 
plt.legend() 
plt.xlabel("Day")
plt.ylabel("Product Amount")
plt.title("Simulation Production Performance")
plt.show()
print()


plt.pie([doneTotT,failTotT], labels = [f"Succesful\n{percentage(doneTotT,failTotT)}%",f"Failed\n{percentage(failTotT,doneTotT)}%"], colors=[(.1,.9,.1),(1,.2,.2)])
plt.title("Simulation Error Rate")

plt.show() 
print()

print("Do you wish to see the data of every single day in the simulation? (y/n)")
inp = input()
if inp == "y":
  #Display the data from every day
  factory.display_status()
elif inp == "n":
  print("Understood")