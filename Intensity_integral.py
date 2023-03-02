import numpy
from Target_centerDist import *

def Gaus(x,y,beamcenter,I,dev):
    [bx,by] = beamcenter                                         #center needs to be defined in mm
    num = I*np.exp(-(x-bx)^2/(2*dev)-(y-by)^2/(2*dev))
    return num

def I_integral(target,beamcenter,I,dev):
    [tx,ty] = locations[target]['pos']*27.0         #27 converts grid location to mm
    if locations[target]['type'] == 'Az':
        radius = 25.4/2                                           #1in diamiter to mm
    elif locations[target]['type'] == 'VD':
        radius = 25.4/8                                           #quarter in diamiter  to mm
    
    
    Xvals = np.linspace((tx - radius),(tx - radius),num = 100)
    Yvals = np.linspace((ty - radius),(ty - radius),num = 100)
    area = (Xvals[0] - Xvals[1])^2 
    integral = 0
    for x in Xvals:
        for y in Yvals:
            if (x^2 + y^2) <= radius^2:
                val = Gaus(x,y,beamcenter,I,dev)
                integral += val*area
            
    return integral


