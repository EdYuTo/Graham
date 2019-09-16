# EDSON YUDI TOMA - 9791305 #

import numpy as np
import matplotlib.pyplot as plt
import sys

class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # this is called by the str() method
    def __str__(self):
        return str("(" + str(self.x) + ", " + str(self.y) + ")")

    # this is used when calling the print() method on an array of point
    def __repr__(self):
        return str(self)
    
    # this is used by the min() method to find the leftmost/downmost point
    def __lt__(self, other):
        return self.y < other.y or (self.y == other.y and self.x < other.x)

    def dx(self, P1):
        return P1.x - self.x

    def dy(self, P1):
        return P1.y - self.y

    def distance(self, P1):
        return np.sqrt(self.dx(P1)**2 + self.dy(P1)**2)

    def polar_angle(self, P1):
        return np.arctan2(self.dy(P1), self.dx(P1))

    @staticmethod
    def orientation(P0, P1, P2):
        return (P1.y - P0.y) * (P2.x - P1.x) - (P1.x - P0.x) * (P2.y - P1.y)
        # =0: collinear
        # >0: clockwise
        # <0: counterclockwise

class graham:
    def __init__(self, array):
        if type(array[0]) == point: # if you want to process the data by yourself...
            self.points = array
        elif type(array) == str:
            try:
                with open(array) as file:
                    self.points = []
                    data = file.read()
                    file.close()
                    data = data.split(";")
                    for tuples in data:
                        coords = tuples.split(",")
                        if len(coords) > 1:
                            self.points.append(point(float(coords[0]), float(coords[1])))
            except:
                print("Could not open file.")

        try:        
            self.leftmost = min(self.points) # the lowest and leftmost point of the inputs
            self.vector = [self.leftmost]
            self.vector.extend(self.__sort_points()) # ordered array with points to process
            if len(self.vector) < 3:
                print("It's not possible to create convex hull.")
            else:
                stack = [self.vector[0], self.vector[1], self.vector[2]]
                for i in range(3, len(self.vector)):
                    while (point.orientation(stack[-2], stack[-1], self.vector[i]) >= 0): # while not counterclockwise
                        stack.pop() # eleimination of unnecessary points
                    stack.append(self.vector[i]) # add following point to process
                #print(self.leftmost) # uncomment to see the values
                #print(self.vector)   # uncomment to see the values
                #print(stack)         # uncomment to see the values
                self.vector = stack
        except:
            print("Invalid data input.")

    def __sort_points(self):
        dic = {}
        for point in self.points:
            if point == self.leftmost:  # skip itself
                continue
            polar_angle = self.leftmost.polar_angle(point) # avoid recalculations
            try:
                if self.leftmost.distance(dic[polar_angle]) < self.leftmost.distance(point): # if the value exists get the farthest
                    dic[polar_angle] = point
            except:
                dic[polar_angle] = point # if it doesn't exist, create it
        dic = sorted(dic.items()) # sort by polar angle with the leftmost point
        return [y for (x, y) in dic] # return the points only, excluding the polar_angles

    def plot(self):
        try:
            x, y = [], []
            a, b = [], []
            # matplotlib takes an array of xs follwed by an array of ys
            # therefore we need to transform our data to this format
            for point in self.points:
                x.append(point.x)
                y.append(point.y)
            for vec in self.vector:
                a.append(vec.x)
                b.append(vec.y)
            a.append(self.leftmost.x) # add the 1st point to close the image (hull)
            b.append(self.leftmost.y) # add the 1st point to close the image (hull)
            plt.plot(x, y, "ro") # points
            plt.plot(a, b) # lines
            plt.show()
        except:
            print("Could not plot.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python", sys.argv[0], "[INPUTFILE]")
        print("\tWhere [INPUTFILE] has the 2D points as follow:")
        print("\t0.0, 0.0; 10.0, 5.0; ...")
    else:
        graham = graham(sys.argv[1]) # sys.argv[1] contains the filename
        graham.plot()