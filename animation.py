import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

filename = "datos.txt"

theta = []
phi = []
dtheta = []
dphi = []
t = []


with open(filename,"r") as file:
    lines = file.readlines()
    for line in lines:
        #print(line.split(" "))
        a,b,c,d,e,_ = line.split(" ")
        theta.append(float(a))
        phi.append(float(b))
        dtheta.append(float(c))
        dphi.append(float(d))
        t.append(float(e))

assert len(theta) == len(phi) == len(dtheta) == len(dphi) == len(t)

steps = len(theta)

theta = np.array(theta)
phi = np.array(phi)
x1 = np.sin(theta)
y1 = -np.cos(theta)

x2 = x1 + np.sin(phi)
y2 = y1 - np.cos(phi)



fig = plt.figure()
ax = fig.add_subplot()

def animation(i):
    ax.clear()
    
    ax.plot(x1[:i+1],y1[:i+1])
    ax.plot(x2[:i+1],y2[:i+1])
    ax.plot([0,x1[i],x2[i]],[0,y1[i],y2[i]])
    ax.scatter([0,x1[i],x2[i]],[0,y1[i],y2[i]])


func = FuncAnimation(fig,animation,steps,interval=0.01)
plt.show()