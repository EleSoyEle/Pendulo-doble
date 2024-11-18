import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation,FFMpegWriter,writers
import argparse

#Los argumentos seran colocados automaticamente desde c
argp = argparse.ArgumentParser()
argp.add_argument("-d","--path",type=str,default="")
args = argp.parse_args()

filename = args.path

#Creamos las listas con los datos
inf_filename = "info.txt"
theta = []
phi = []
dtheta = []
dphi = []
t = []

#Cargamos la longitud de cada pendulo desde el archivo info.txt
with open(inf_filename,"r") as file:
    txt = file.read()
    l1,l2 = txt.split(",")
    l1 = float(l1)
    l2 = float(l2)

#Abrimos el archivo de datos y cargamos toda la informacion a las listas antes creadas
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

#Para evitar errores en la animacion, verificamos que la longitud de cada lista sea igual
#En caso contrario se va a terminar la ejecucion
assert len(theta) == len(phi) == len(dtheta) == len(dphi) == len(t)

#Cargamos el numero de pasos
steps = len(theta)

#Volvemos las listas a formato numpy
theta = np.array(theta)
phi = np.array(phi)

#Pasamos de coordenadas polares a cartesianas para facilitar la graficacion
x1 = l1*np.sin(theta)
y1 = -l1*np.cos(theta)

x2 = x1 + l2*np.sin(phi)
y2 = y1 - l2*np.cos(phi)



plt.style.use("dark_background")
fig = plt.figure()
ax = fig.add_subplot()

def animation(i):
    ax.clear()
    ax.axis("off")
    ax.set_xlim(-l1-l2-0.1,l1+l2+0.1)
    ax.set_ylim(-l1-l2-0.1,1)
    ax.plot(x1[:i+1],y1[:i+1],c="w",linewidth=0.7,alpha=0.7)
    ax.plot(x2[:i+1],y2[:i+1],c="w",linewidth=0.7,alpha=0.7)
    ax.plot([0,x1[i],x2[i]],[0,y1[i],y2[i]],c="w")
    ax.scatter([0,x1[i],x2[i]],[0,y1[i],y2[i]],c="w")


func = FuncAnimation(fig,animation,steps,interval=0.01)
opt = input("¿Quieres guardar el video?[y/n]")
if opt=="y":
    name = input("Ingresa el nombre[mp4]: ")
    if name.find(".mp4")==-1:
        name = name+".mp4"
    print("El video se esta creando, espera un poco...")
    ffmpeg_writer = writers['ffmpeg']
    writer = ffmpeg_writer(fps=32, codec='mpeg4')
    func.save(name, writer=writer,dpi=400)
plt.show()