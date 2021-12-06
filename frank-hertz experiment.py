import matplotlib.pyplot as plt 
import numpy as np
import animatplot as amp
from matplotlib.animation import FuncAnimation
from scipy.signal import find_peaks
from scipy.interpolate import interp1d
from scipy.interpolate import make_interp_spline, BSpline

current_file = open('./current.txt', 'r')
voltage_file = open('./voltage.txt', 'r')

"""
expected values: 
--> 1st minimum 16.5-18.5
--> 2nd minimum 35-37 
--> 3rd minimum 54-58

"""

def compute(error):
    
    voltage = np.arange(0,81,2)

    with current_file as file:
        lines = file.readlines()
        current= np.array([float(line.rstrip())-error for line in lines])

    # with voltage_file as file:
    #     lines = file.readlines()
    #     voltage= np.array([float(line.rstrip()) for line in lines])

    fig , ax = plt.subplots()
    #line, = ax.plot(voltage,current ,'r')

    plt.title('Franck-Hertz Experiment')
    plt.xlabel('Accelerating Voltage (V)')
    plt.ylabel('collected current (nA)')

    xnew = np.linspace(voltage.min(), voltage.max(), 500) 
    spl = make_interp_spline(voltage, current, k=3)
    y_smooth = spl(xnew)

    peaks, _= find_peaks(current)
    troughs, _= find_peaks(-current)

    troughs_smooth, _= find_peaks(-y_smooth)

    # def animate(i):

    #     line.set_data(voltage[:i], current[:i])

    #     return line,

    fig = plt.gcf()
    fig.set_size_inches(12, 8)
    # animation = FuncAnimation(fig , func = animate ,interval = 50 ,blit = True)
    #plt.plot(voltage[peaks],current[peaks] ,'^')
    plt.plot(voltage[troughs],current[troughs] ,'^')

    #plt.plot(xnew[troughs_smooth],y_smooth[troughs_smooth] ,'^' )
    plt.plot(voltage, current ,'r',  label="Actual")
    plt.plot(xnew, y_smooth , 'g' , label = 'Smooth')
    plt.legend()
    plt.show()  

    final = """
            from smooth graph:
                --> 1st minimum: {} Volts
                --> 2nd minimum: {} Volts
                --> 3rd minimum: {} Volts
            """

    final2 = """
            from actual graph:
                --> 1st minimum: {} Volts
                --> 2nd minimum: {} Volts
                --> 3rd minimum: {} Volts
            """
    print(final.format(xnew[troughs_smooth][0], xnew[troughs_smooth][1] , xnew[troughs_smooth][2])) 
    print('*'*50)
    #print(final2.format(voltage[troughs][0], voltage[troughs][1] , voltage[troughs][2]))        
    
    fig.savefig('./file.png')
    #animation.save('./fig.gif',writer='imagemagick', fps=30)



compute(0)    

