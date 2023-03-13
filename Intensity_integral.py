import numpy as np
from Target_centerDist import *

def Gaus(x,y,beamcenter,I,dev):
    bx = beamcenter[0]
    by = beamcenter[1]                                        #center needs to be defined in mm
    num = I*np.exp(-(x-bx)**2/(2*dev)-(y-by)**2/(2*dev))
    return num

def I_integral(target,beamcenter,I,dev):
    [tx,ty] = np.array(locations[target]['pos'])        #27 converts grid location to mm
    tx = tx*27 - 6*27
    ty = ty*27 - 6*27
    if locations[target]['type'] == 'Az':
        radius = 25.4/2                                           #1in diamiter to mm
    elif locations[target]['type'] == 'VD':
        radius = 25.4/8                                           #quarter in diamiter  to mm
    
    
    Xvals = np.linspace((tx - radius),(tx + radius),num = 10)
    Yvals = np.linspace((ty - radius),(ty + radius),num = 10)
    area = (Xvals[0] - Xvals[1])**2 
    integral = 0
    for x in Xvals:
        for y in Yvals:
            if ((x-tx)**2 + (y-ty)**2) <= radius**2:
                val = Gaus(x,y,beamcenter,I,dev)
                integral += val*area
                
                #integral += val       #I dont think this is correct 
    return integral


