import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, ImageMagickWriter
from math import sin, cos, pi

#from matplotlib import rcParams
#rcParams['text.usetex'] = True

def matrix_t(A, house = None, save = ""):
    A = np.array(A).astype(np.float64)
    d = np.linalg.det(A)
    if house == None:
        wall = np.array([[0,0], [1,0], [1,1], [0,1]]).T
        roof = np.array([[-0.1,1], [0.1, 1.2], [0.1, 1.5], [0.3, 1.5], [0.3, 1.4], [0.5,1.6], [1.1,1]]).T
        door =  np.array([[0.1,0], [0.4,0], [0.4,0.6], [0.1,0.6]]).T
        window =  np.array([[0.6,0.3], [0.9,0.3], [0.9,0.6], [0.6,0.6]]).T
        house = [(wall, 'cadetblue'), (roof, 'orangered'), (door, 'tan'), (window, 'white')]
    
    fig = plt.figure(figsize = (12,4))
    fig.patch.set_alpha(0)
    plt.tight_layout()
    plt.style.use('seaborn')
    
    #ms = (r"A = [[ "
    #      + "{:.3f}".format(A[0,0]).rstrip('0').rstrip('.') + ",   " 
    #      + "{:.3f}".format(A[0,1]).rstrip('0').rstrip('.') + " ], [ " 
    #      + "{:.3f}".format(A[1,0]).rstrip('0').rstrip('.') + ",   " 
    #      + "{:.3f}".format(A[0,0]).rstrip('0').rstrip('.') + " ]]" 
    #     )
    #plt.suptitle(ms)
    ax1 = plt.axes([0.05, 0.05, 0.35, 0.9])
    ax1.axis('equal')
    ax2 = plt.axes([0.6, 0.05, 0.35, 0.9])
    ax2.axis('equal')
    ax2.yaxis.tick_right()
    ax3 = plt.axes([0.45, 0.05, 0.1, 0.9])
    ax3.arrow(0,0, 0.75,0, width = 0.02, head_width = 0.06, head_length = 0.2, fc = 'k')
    ax3.set_ylim(-1, 1)
    ax3.axis('off')
    xmax, ymax = 1.5, 1.5
    xmin, ymin = -1.5, -1.5
    nhouse = []
    for (s, c) in  house: 
        ns = np.dot(A, s)
        nhouse.append((ns, c))
        xmax = max(np.max(ns[0]), np.max(s[0]), xmax)
        ymax = max(np.max(ns[1]), np.max(s[1]), ymax)
        xmin = min(np.min(ns[0]), np.min(s[0]), xmin)
        ymin = min(np.min(ns[1]), np.min(s[1]), ymin)
        ax1.fill(*list(s), c)
        if np.array_equal(A, np.zeros((2,2))):
            ax2.plot(*list(ns), 'o', color='orangered', ms = 10)
        elif d == 0:   
            ax2.plot(*list(ns), c, lw = 4)
        else:
            ax2.fill(*list(ns), c)        
    ax1.plot([0, 0], [ymin, ymax], 'k')
    ax1.plot([xmin, xmax], [0, 0], 'k')
    ax2.plot([0, 0], [ymin, ymax], 'k')
    ax2.plot([xmin, xmax], [0, 0], 'k')
    if save:
        plt.savefig(save, pad_inches = 0.5)
    plt.show() 
    
    return nhouse 




def animated_house(delay = 40):
    '''
    animation of matrix tranformations
    delay = frame interval
    
    Note: the return value must to be assigned to a variable 
    so that the animation object persists.
    '''
    wall = np.array([[0,0], [1,0], [1,1], [0,1]]).T
    roof = np.array([[-0.1,1], [0.1, 1.2], [0.1, 1.5], [0.3, 1.5], [0.3, 1.4], [0.5,1.6], [1.1,1]]).T
    door =  np.array([[0.1,0], [0.4,0], [0.4,0.6], [0.1,0.6]]).T
    window =  np.array([[0.6,0.3], [0.9,0.3], [0.9,0.6], [0.6,0.6]]).T
    house = [(wall, 'cadetblue'), (roof, 'orangered'), (door, 'tan'), (window, 'white')]

    fig = plt.figure(figsize = (5,5))
    fig.patch.set_alpha(0)
    plt.tight_layout()
    plt.style.use('seaborn')

    ax1 = plt.gca()
    ax1.axis('equal')
    xmax, ymax = 2.5, 2.5
    xmin, ymin = -2.5, -2.5
    house_fills = []
    for (s, c) in  house: 
        shape, = ax1.fill(*list(s), c) 
        house_fills.append(shape)
    ax1.plot([0, 0], [ymin, ymax], 'k')
    ax1.plot([xmin, xmax], [0, 0], 'k')

    def update_plot(t):
        A = np.array([[cos(t)**3, (1+t/(2*pi))*sin(t)**3], [(1-2*t/(2*pi))*sin(t)**3, cos(t)**3]])  
        for i in range(len(house)):
            nshape = np.dot(A, house[i][0]).T
            house_fills[i].set_xy(nshape)
        return house_fills

    ani = FuncAnimation(fig, func = update_plot, frames=np.linspace(0, 2*pi, 100), interval=delay, blit=True, repeat=True)

    plt.show() 
    return ani