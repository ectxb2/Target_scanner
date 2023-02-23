import numpy as np
import matplotlib.pyplot as plt
import h5py
import sys
from sklearn.cluster import DBSCAN

#ex:
# python3 DBScan_tracks.py selftrigger_2022_08_05_00_04_09_PDT_evd.h5 3,6,8,78




#Pass the fenction these things
#Argument 1: name of selftrigger file, ex: selftrigger_2022_08_05_00_04_09_PDT_evd.h5
#Argument 2: array of tracks to scan arround, but in specific format ex: 3,5,7,9


detector_bounds = [[-150, 150], [-150, 150], [0, 300]] # mm (x, y, z)

v_drift = 1.6 # mm/us (very rough estimate)
clock_interval = 0.1 # us/tick -- 10 MHz clock rate
drift_distance = detector_bounds[2][1] - detector_bounds[2][0] 

drift_window = drift_distance/(v_drift*clock_interval) # maximum drift time

drift_direction = 1 # +/- 1 depending on the direction of the drift in z

#f = h5py.File('selftrigger_2022_08_05_05_06_01_PDT_evd.h5')
#output_name=sys.argv[1] 
f = h5py.File(sys.argv[1])

eventData = f['charge']['events']['data']

hitData = f['charge']['hits']['data']

# this is a list of pairs of ints
# the first is an event ID, the second is a hit ID
eventHitRefs = f['charge']['events']['ref']['charge']['hits']['ref']  

def drift_distance(dt):
    """
    Estimate the z-position of a drifting electron
    """
    return detector_bounds[2][0] + drift_direction*dt*clock_interval*v_drift

def draw_hits_in_event_window_by_timestamp(event):
    """
    Given a t0, plot all hits that would be within a 
    drift window within the detector timeline
    """
    t0 = event['ts_start']
    tf = event['ts_end']
    
    eventMask = ( t0 <= hitData['ts']) & (hitData['ts'] < tf ) 

    eventHits = hitData[eventMask]

    px = eventHits['px']
    py = eventHits['py']
    ts = eventHits['ts']

    z = drift_distance(ts - t0)

    q = eventHits['q']

    fig = plt.figure()
    #ax = fig.add_subplot(111, projection = '3d')
    ax = fig.add_subplot(111)

    #points = ax.scatter(px, py, z,c = q)
    points = ax.scatter(px, py,c = q)

    cb = fig.colorbar(points)
    cb.set_label(r'Charge')
    
    return ax


def draw_boundaries(ax):
    """
    Draw the detector boundaries as a wireframe
    not needed, but pretty
    """
    boundKwargs = {'color': 'black',
                   'ls': '--'}
    
    ax.plot([detector_bounds[0][0], detector_bounds[0][1]],
            [detector_bounds[1][0], detector_bounds[1][0]],
            [detector_bounds[2][0], detector_bounds[2][0]],
            **boundKwargs)
    ax.plot([detector_bounds[0][0], detector_bounds[0][1]],
            [detector_bounds[1][1], detector_bounds[1][1]],
            [detector_bounds[2][0], detector_bounds[2][0]],
            **boundKwargs)
    ax.plot([detector_bounds[0][0], detector_bounds[0][0]],
            [detector_bounds[1][0], detector_bounds[1][1]],
            [detector_bounds[2][0], detector_bounds[2][0]],
            **boundKwargs)
    ax.plot([detector_bounds[0][1], detector_bounds[0][1]],
            [detector_bounds[1][0], detector_bounds[1][1]],
            [detector_bounds[2][0], detector_bounds[2][0]],
            **boundKwargs)
    return ax


def draw_labels(ax):
    ax.set_xlabel(r'x [mm]')
    ax.set_ylabel(r'y [mm]')
    #ax.set_zlabel(r'z (drift) [mm]')

    plt.tight_layout()
    

'''
for event in eventData:
    ax = draw_hits_in_event_window_by_timestamp(event)
    # ax = draw_hits_in_event_window_by_reference(event)
    draw_boundaries(ax)
    draw_labels(ax)

    plt.show()'''
    
event_num = 0
t_num = 0
#convert string from input to usable array
t = sys.argv[2].split(',')
t = [eval(i) for i in t]

#plot tracks:
'''
for event in eventData:
    if event_num == t[t_num]:
        print(event_num)
        ax = draw_hits_in_event_window_by_timestamp(event)
        # ax = draw_hits_in_event_window_by_reference(event)
        draw_boundaries(ax)
        draw_labels(ax)
        plt.show()
        t_num += 1
        event_num +=1
    else :
        event_num +=1
        #print(event_num)
'''

#xseed = sys.argv[3].split(',')
#xseed = [eval(i) for i in t]

#yseed = sys.argv[4].split(',')
#yseed = [eval(i) for i in t]

#dist = 18.5 # pixel center to center diagonally asuming 4.4mm pixel pitch 
dist = 25
def make_colors(array):
    out = []
    for i in array:
        cluster = i
        #while cluster > 4:
        #    cluster = cluster - 5        
        if cluster == -1:
            out += ['k'] #noise is black
        elif cluster == 0:
            out += ['b']
        elif cluster == 1:
            out += ['g']
        elif cluster == 2:
            out += ['r']
        elif cluster == 3:
            out += ['c']
        elif cluster == 4:
            out += ['m']
    return out
         

def draw_hits_dbscaned(event):
    """
    Given a t0, plot all hits that would be within a 
    drift window within the detector timeline
    """
    t0 = event['ts_start']
    tf = event['ts_end']
    
    eventMask = ( t0 <= hitData['ts']) & (hitData['ts'] < tf ) 

    eventHits = hitData[eventMask]

    px = eventHits['px']
    py = eventHits['py']
    ts = eventHits['ts']

    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    eventID = event['id']
    eventMask = eventHitRefs[:,0] == eventID
    eventHits = hitData[eventMask]
    px = np.array(eventHits['px'])
    py = np.array(eventHits['py'])  
    
    #xy_tracks = np.append(px,py,axis = 0)
    xy_tracks = np.array([px,py]).T
        
    db = DBSCAN(eps = dist, min_samples=4).fit(xy_tracks)
    labels = db.labels_
    #core_samples = db.core_sample_indices_
    #n_clusters = len(set(labels)) - (1 if -1 in labels else 0) 
    color_array = make_colors(labels)
    points = ax.scatter(px, py,c=color_array)
    
    return ax


for event in eventData:
    if event_num == t[t_num]:

        ax = draw_hits_in_event_window_by_timestamp(event)
        draw_boundaries(ax)
        draw_labels(ax)
        plt.show()
        
        ax = draw_hits_dbscaned(event)
        draw_boundaries(ax)
        draw_labels(ax)    
        plt.show()
        t_num += 1
        event_num +=1
    else :
        event_num +=1
        #print(event_num)


