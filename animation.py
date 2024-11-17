import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation,FFMpegWriter,writers

filename = "datos.txt"
inf_filename = "info.txt"
theta = []
phi = []
dtheta = []
dphi = []
t = []

with open(inf_filename,"r") as file:
    txt = file.read()
    l1,l2 = txt.split(",")
    l1 = float(l1)
    l2 = float(l2)


with open(filename,"r") as file:
    lines = file.readlines()
    for line in lines:
        spl = line.split(" ")
        a,b,c,d,e = spl if len(spl)==5 else spl[:-1]
        theta.append(float(a))
        phi.append(float(b))
        dtheta.append(float(c))
        dphi.append(float(d))
        t.append(float(e))

assert len(theta) == len(phi) == len(dtheta) == len(dphi) == len(t)

steps = len(theta)

theta = np.array(theta)
phi = np.array(phi)
x1 = l1*np.sin(theta)
y1 = -l1*np.cos(theta)

x2 = x1 + l2*np.sin(phi)
y2 = y1 - l2*np.cos(phi)



plt.style.use("dark_background")
fig = plt.figure()
ax = fig.add_subplot()

def animation(i):
    ax.clear()
    ax.set_xlim(-l1-l2-0.1,l1+l2+0.1)
    ax.set_ylim(-l1-l2-0.1,1)
    ax.plot(x1[:i+1],y1[:i+1],c="w",linewidth=0.7,alpha=0.7)
    ax.plot(x2[:i+1],y2[:i+1],c="w",linewidth=0.7,alpha=0.7)
    ax.plot([0,x1[i],x2[i]],[0,y1[i],y2[i]],c="w")
    ax.scatter([0,x1[i],x2[i]],[0,y1[i],y2[i]],c="w")


func = FuncAnimation(fig,animation,steps,interval=0.01)
#ffmpeg_writer = writers['ffmpeg']
#writer = ffmpeg_writer(fps=32, codec='mpeg4')
#func.save("video.mp4", writer=writer,dpi=500)
plt.show()