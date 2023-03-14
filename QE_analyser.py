import numpy as np
import matplotlib.pyplot as plt
from Intensity_integral import I_integral, Gaus
from DBScan_tracks_ref import find_centers, draw_hits_dbscaned, draw_boundaries, draw_labels
from Target_centerDist import *
from sklearn.cluster import DBSCAN
import h5py



#example run script :
# python3 QE_analyser.py selftrigger_2022_08_05_00_04_09_PDT_evd.h5 78

#Pass the function these things
#Argument 1: name of selftrigger file, ex: selftrigger_2022_08_05_00_04_09_PDT_evd.h5
#Argument 2: array of tracks to scan arround, but in specific format ex: 3,5,7,9


detector_bounds = [[-150, 150], [-150, 150], [0, 300]] # mm (x, y, z)
v_drift = 1.6 # mm/us (very rough estimate)
clock_interval = 0.1 # us/tick -- 10 MHz clock rate
drift_distance = detector_bounds[2][1] - detector_bounds[2][0] 
drift_window = drift_distance/(v_drift*clock_interval) # maximum drift time
drift_direction = 1 # +/- 1 depending on the direction of the drift in z
beam_centers = {"left_beam": [-119.9,-3.82],
               "right_beam": [5.2,-3.82]}
#beam center to be used in this run 
beam_center = beam_centers["right_beam"]
#Ligth paramiters
I = 500000000
dev = 800

#f = h5py.File('selftrigger_2022_08_05_05_06_01_PDT_evd.h5')

f = h5py.File(sys.argv[1])

eventData = f['charge']['events']['data']
hitData = f['charge']['hits']['data']

# this is a list of pairs of ints
# the first is an event ID, the second is a hit ID
eventHitRefs = f['charge']['events']['ref']['charge']['hits']['ref'] 

event_num = 0
t_num = 0

#convert string from input to usable array for tracks of interest
t = sys.argv[2].split(',')
t = [eval(i) for i in t]
dist = 18.5 # pixel center to center diagonally asuming 4.4mm pixel pitch 
#Make function to do this too 
all_targets = list(locations.keys())
 
#Read centers from file and compare to centers from DBScanner
def center_dif(x_center,y_center,targets = all_targets):
    closests_targets = []
    target_dists = []
    closest_xs = []
    closest_ys = []

    for i in range(0,len(x_centers)):
        shortest_dist = 150
        closest_target = 'error'
        for target in targets:
            target_pos = np.array(locations[target]['pos'])         
            tx = target_pos[0]*27 - 6*27
            ty = target_pos[1]*27 - 6*27
            cluster_target_dist = np.sqrt((x_centers[i] - (tx))**2 + (y_centers[i]-(ty))**2) 
            #distance between cluster and target, 27 converts to mm
            
            if cluster_target_dist < shortest_dist:
                shortest_dist = cluster_target_dist
                closest_target = target
                closest_x =tx
                closest_y = ty
        closests_targets += [closest_target]
        target_dists += [shortest_dist]
        closest_xs += [closest_x]
        closest_ys += [closest_y]

    return(target_dists, closests_targets, closest_xs, closest_ys )        
             
#get target types and locations
def get_targets(targets = all_targets):
    Az_target_xs = []
    Az_target_ys = []
    VD_target_xs = []
    VD_target_ys = []   
    for target in targets:
        t_type = locations[target]['type']
        target_pos = np.array(locations[target]['pos']) 
        tx = target_pos[0]*27 - 6*27
        ty = target_pos[1]*27 - 6*27
        if  t_type == 'Az':
            Az_target_xs += [tx]
            Az_target_ys += [ty]
        elif t_type == 'VD':
            VD_target_xs += [tx]
            VD_target_ys += [ty]
    return(Az_target_xs,Az_target_ys,VD_target_xs,VD_target_ys)

def measured_QE(closests_targets,beam_center,I,dev,q_totals):
    QEs = []
    Is = []    
    for i in range(0,len(closests_targets)):
        target = closests_targets[i]
        I = I_integral(target,beam_center,I,dev)
        QEs += [q_totals[i]/I]
        Is += [I]
    return(QEs,Is)
   
   
   
for event in eventData:
    if event_num == t[t_num]:
        
        
        t0 = event['ts_start']
        tf = event['ts_end']
        eventMask = ( t0 <= hitData['ts']) & (hitData['ts'] < tf ) 
        eventHits = hitData[eventMask]
        px = eventHits['px']
        py = eventHits['py']
        ts = eventHits['ts']
        q = eventHits['q'] 
            
        fig = plt.figure()
        ax = fig.add_subplot(111)
        xy_tracks = np.array([px,py]).T 
        db = DBSCAN(eps = dist, min_samples=4).fit(xy_tracks)
        x_centers , y_centers , q_totals = find_centers(db,px,py,q)
        #Draw cluster center, target and write QE
        #ax = draw_hits_dbscaned(event)
        draw_boundaries(ax)
        draw_labels(ax)  
        #plot cluster centers
        plt.scatter(x_centers,y_centers, s=30, c='k') 
        target_dists, closests_targets, closest_xs, closest_ys = center_dif(x_centers,y_centers,targets = all_targets)
        #plt.scatter(closest_xs, closest_ys, s = 30, c='b')
        QEs,Is = measured_QE(closests_targets,beam_center,I,dev,q_totals)
        Az_target_xs,Az_target_ys,VD_target_xs,VD_target_ys = get_targets()
        #plot all target centers
        plt.scatter(Az_target_xs,Az_target_ys,s = 60, c='b')
        plt.scatter(VD_target_xs,VD_target_ys,s = 30, c='b')
        
        for i in range(0,len(x_centers)):
            plt.text(x_centers[i],y_centers[i],' QE ~ '+str((QEs[i])))
            pairx = [x_centers[i],closest_xs[i]]
            pairy = [y_centers[i],closest_ys[i]]
            plt.plot(pairx, pairy, color='r', linewidth=1)
        
        plt.show()
        
        
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        xy_tracks = np.array([px,py]).T 
        db = DBSCAN(eps = dist, min_samples=4).fit(xy_tracks)
        x_centers , y_centers , q_totals = find_centers(db,px,py,q)
        #Draw cluster center, target and write QE
        #ax = draw_hits_dbscaned(event)
        draw_boundaries(ax)
        draw_labels(ax)  
        plt.title('Target Centroid Change')
        #plot cluster centers
        #plt.scatter(x_centers,y_centers, s=30, c='k') 
        #target_dists, closests_targets, closest_xs, closest_ys = center_dif(x_centers,y_centers,targets = all_targets)
        #plot target centers
        #plt.scatter(closest_xs, closest_ys, s = 30, c='b')
        
        #add light contours
        x = np.linspace(-150,150, num = 30)
        y = np.linspace(-150,150, num = 30)
        [X,Y] = np.meshgrid(x,y)
        z_intensity = Gaus(X,Y,beam_center,I,dev)
        plt.contour(x,y,z_intensity)
        
        plt.scatter(Az_target_xs,Az_target_ys,s = 60, c='b')
        plt.scatter(VD_target_xs,VD_target_ys,s = 30, c='b')  
              
        for i in range(0,len(x_centers)):
            pairx = [x_centers[i],closest_xs[i]]
            pairy = [y_centers[i],closest_ys[i]]
            plt.plot(pairx, pairy, color='r', linewidth=1.5)        
        plt.show()
        
        QE_fit, b = np.polyfit(Is,q_totals,1)
        QE_line_label = 'Q = '+ str(QE_fit) + '* I + ' + str(b)
        fitline = QE_fit*np.array(Is)+b
        
        plt.scatter(Is,q_totals)
        plt.plot(Is, fitline, label = QE_line_label)
        
        plt.title('Intensity vs Charge Measured')
        plt.ylabel('Total cluster charge')
        plt.xlabel('Light on target')
        plt.legend()
        plt.show()
        
        t_num += 1
        event_num +=1
    else : 
        event_num +=1
        










