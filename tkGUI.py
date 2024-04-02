# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 11:22:01 2024

A script to display a matplotlib in a Tkinter GUI, as acquired from 
https://www.geeksforgeeks.org/how-to-embed-matplotlib-charts-in-tkinter-gui/

@author: CM
"""


from tkinter import *
from tkinter import ttk

from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk) 

import networkx as nx
import matplotlib.pyplot as plt

def makeAGraphToShow():
    
    
    # nx.draw() is documented at
    # https://networkx.org/documentation/stable/reference/generated/networkx.drawing.nx_pylab.draw.html
    
    tG = nx.tutte_graph()
    
    subax1 = plt.subplot(121)
    nx.draw(tG, with_labels='True', font_weight='bold')
    
    plt.draw()
    # return tG

# plot function is created for 
# plotting the graph in 
# tkinter window 
def plot(): 

    # the figure that will contain the plot 
    fig = Figure(figsize = (5, 5), 
                 dpi = 100) 
    
    # list of squares 
    y = [i**2 for i in range(101)] 
    
    # adding the subplot 
    plot1 = fig.add_subplot(111) # https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure.add_subplot
    
    # plotting the graph 
    # plot3 = fig.add_subplot(2,1,1)
    # plot3.plot(y)
    
    tG = nx.tutte_graph()
    nx.draw(tG, ax=plot1, with_labels='True', font_weight='bold')


    # pG = nx.petersen_graph()
    # subax1 = fig.add_subplot(121) #plt.subplot(121)
    # nx.draw(pG, ax=subax1, with_labels='True', font_weight='bold')
    
    # creating the Tkinter canvas 
    # containing the Matplotlib figure 
    canvas = FigureCanvasTkAgg(fig, master = window) 
    canvas.draw() 
    
    # placing the canvas on the Tkinter window 
    canvas.get_tk_widget().pack() 
    
    # creating the Matplotlib toolbar 
    toolbar = NavigationToolbar2Tk(canvas, window) 
    toolbar.update() 
    
    # placing the toolbar on the Tkinter window 
    canvas.get_tk_widget().pack() 

# the main Tkinter window 
window = Tk(screenName='HAZOP Copilot') 

# setting the title 
window.title('HAZOP Copilot') 

# dimensions of the main window 
window.geometry("1000x800") 

frame = ttk.Frame(window, padding=10, borderwidth=1, relief='groove')

frame.pack()


plotFrame = ttk.Frame(window, padding=20, borderwidth=1, relief='groove')
plotFrame.pack()

# button that displays the plot 
plot_button = Button(master = frame, 
                     command = plot, 
                     height = 2, 
                     width = 15, 
                     text = "Plot Graph") 
# plot_button.grid(column=0, row=0)

exit_button = Button(master = frame,
                     command = window.destroy,
                     height = 2,
                     width = 15, 
                     text = "Exit")
# exit_button.grid(column=1, row=0)


# place the button 
# in main window 
plot_button.pack() 
exit_button.pack()


# run the gui 
window.mainloop() 
