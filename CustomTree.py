"""A method of storing the filtered Convex Hulls."""

import random

def addTwoOf(someList):
    return someList[random.choice(range(len(someList)))] + someList[random.choice(range(len(someList)))]

listStuff = [1, 2, 3]
print(sorted(listStuff, key=addTwoOf(listStuff)))
