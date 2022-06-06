#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import pyglet
import imageio
import os
import cv2
import PIL
from PIL import Image,ImageSequence,ImageTk
import tkinter as tk
import time


# In[2]:


#function for constructing getting value from entries and construct "2dheatequation.gif"
def getvalue():
    #getting temp. values from entry 1~4
    T_top = entry1.get()
    T_left = entry2.get()
    T_right = entry3.get()
    T_bottom = entry4.get()
    
    #dimensions of x,y and t
    width = 100
    length = 100
    total_time = 300
    
    #constant in heat equation(take cement as example)
    k = 1.01 #thermal conductivity
    rho = 1.44 #density
    cp = 3.15 #specific heat
    α = k/(rho * cp) #alpha(3.2)
    
    #unit step size and unit time length
    h = 1 #step size(delta x = delta y = h)
    delta_t = (h ** 2)/(4 * α) #unit time length(3.12)
    
    #initialize boundary condition and matrix for temp. distribution T(k,i,j)
    T = np.empty((total_time, width, length)) #matrix for temp. distribution T(k,i,j) (maximum = 1000,minimum = 0)
    T[:, (width-1):, :] = T_top #initialize boundary condition
    T[:, :, :1] = T_left
    T[:, :1, 1:] = T_bottom
    T[:, :, (length-1):] = T_right
    
    #heat equation discussed in 3.文獻回顧與探討
    for k in range(0, total_time-1, 1):
        for i in range(1, width-1, h):
            for j in range(1, length-1, h):
                #heat equation(3.11)
                T[k + 1, i, j] = ((α*delta_t)/(h**2))*(T[k][i+1][j] + T[k][i-1][j] + T[k][i][j+1] + T[k][i][j-1]) + (((α*delta_t)/(h**2))*(-4)+1) * T[k][i][j]

    #construct multiple plt images from time = 0 to time = total_time
    filenames = []
    for i in range(0,total_time-1):
        plt.clf()
        plt.title(f"Temperature at t = {i*delta_t:.3f} unit time")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.pcolormesh(T[i], cmap=plt.cm.jet, vmin=0, vmax=1000)
        plt.colorbar()
        
        file = f'{i}.png'
        filenames.append(file)
        plt.savefig(file)
        plt.close()
    
    #mix all the plt images together to get 2dheatequation.gif
    with imageio.get_writer("2dheatequation.gif", mode='I') as writer:
        for file in filenames:
            image = imageio.imread(file)
            writer.append_data(image)
        
    #delete all the plt images constructed in the previous section of the code
    for filename in set(filenames):
        os.remove(filename)

#function for showing 2dheatequation.gif in GUI tkinter
def pick(event):
    global a,flag   
    while 1:
        image = Image.open("2dheatequation.gif")
        iter = ImageSequence.Iterator(image)
        for frame in iter:
            picture=ImageTk.PhotoImage(frame)
            canvas1.create_image((260,150), image=picture)
            time.sleep(0.1)
            win.update_idletasks()
            win.update()


# In[3]:


#code for tkinter GUI
win = tk.Tk()
win.title("2-Dimensional Heat Equation")
win.geometry("500x580")

#frame for temp. input
frame1 = tk.Frame(win)
frame1.grid()
#label for top temp.
label1 = tk.Label(frame1,text = "top temperature: ",font = ("Arial",10))
label1.grid(row = 1,column = 2,pady = 5)
#entry for top temp.
entry1 = tk.Entry(frame1)
entry1.grid(row = 2,column = 2,pady = 10)
#label for left temp.
label2 = tk.Label(frame1,text = "left temperature: ",font = ("Arial",10))
label2.grid(row = 5,column = 0,pady = 5)
#entry for left temp.
entry2 = tk.Entry(frame1)
entry2.grid(row = 6,column = 0,pady = 10)
#label for right temp.
label3 = tk.Label(frame1,text = "right temperature: ",font = ("Arial",10))
label3.grid(row = 5,column = 10,pady = 5)
#entry for right temp.
entry3 = tk.Entry(frame1)
entry3.grid(row = 6,column = 10,pady = 10)
#label for bottom temp.
label4 = tk.Label(frame1,text = "bottom temperature: ",font = ("Arial",10))
label4.grid(row = 9,column = 2,pady = 5)
#entry for bottom station
entry4 = tk.Entry(frame1)
entry4.grid(row = 10,column = 2,pady = 10)

#frame for button
frame2 = tk.Frame(win)
frame2.grid()
#button for temp. input
button1 = tk.Button(frame2,text = "get temperature",command = getvalue,height = 2,font = ("Arial",10))
button1.grid(row = 1)

#frame for 2dheatequation.gif
frame3 = tk.Frame(win)
frame3.grid()
canvas1 = tk.Canvas(frame3,width=500, height=500,bg='white')
canvas1.grid(row = 0,column = 10,sticky = tk.E)
canvas1.bind("<Enter>",pick)

win.mainloop()


# In[ ]:




