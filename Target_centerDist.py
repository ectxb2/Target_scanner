import numpy as np
import sys
import matplotlib.pyplot as plt

#Edit to make everythin dict with material spec

#The first position in the comand line is the one considered the center


locations = {"A1": {'pos':[1,1],'type':'Az'}, "A2": {'pos':[2,1],'type':'VD'},
          "A3": {'pos':[3,1],'type':'Az'},"A4": {'pos':[4,1],'type':'VD'},
          "A5": {'pos':[5,1],'type':'Az'},"A6": {'pos':[6,1],'type':'VD'},
          "A7": {'pos':[7,1],'type':'Az'},"A8": {'pos':[8,1],'type':'VD'},
          "A9": {'pos':[9,1],'type':'Az'},"A10": {'pos':[10,1],'type':'VD'},
          "A11": {'pos':[11,1],'type':'Az'},
          
          "B1":{'pos':[1,2],'type':'VD'},"B2":{'pos':[2,2],'type':'Az'},
          "B3":{'pos':[3,2],'type':'VD'},"B4":{'pos':[4,2],'type':'Az'},
          "B5":{'pos':[5,2],'type':'VD'},"B6":{'pos':[6,2],'type':'Az'},
          "B7":{'pos':[7,2],'type':'VD'},"B8":{'pos':[8,2],'type':'Az'},
          "B9":{'pos':[9,2],'type':'VD'},"B10":{'pos':[10,2],'type':'Az'},
          "B11":{'pos':[11,2],'type':'VD'},
          
          "C1":{'pos':[1,3],'type':'Az'},"C2":{'pos':[2,3],'type':'VD'},
          "C3":{'pos':[3,3],'type':'Az'},"C4":{'pos':[4,3],'type':'VD'},
          "C5":{'pos':[5,3],'type':'Az'},"C6":{'pos':[6,3],'type':'VD'},
          "C7":{'pos':[7,3],'type':'Az'},"C8":{'pos':[8,3],'type':'VD'},
          "C9":{'pos':[9,3],'type':'Az'},"C10":{'pos':[10,3],'type':'VD'},
          "C11":{'pos':[11,3],'type':'Az'},
          
          "D1":{'pos':[1,4],'type':'VD'},"D2":{'pos':[2,4],'type':'Az'},
          "D3":{'pos':[3,4],'type':'VD'},"D4":{'pos':[4,4],'type':'Az'},
          "D5":{'pos':[5,4],'type':'VD'},"D6":{'pos':[6,4],'type':'Az'},
          "D7":{'pos':[7,4],'type':'VD'},"D8":{'pos':[8,4],'type':'Az'},
          "D9":{'pos':[9,4],'type':'VD'},"D10":{'pos':[10,4],'type':'Az'},
          "D11":{'pos':[11,4],'type':'VD'},
          
          "E1":{'pos':[1,5],'type':'Az'},"E2":{'pos':[2,5],'type':'VD'},
          "E3":{'pos':[3,5],'type':'Az'},"E4":{'pos':[4,5],'type':'VD'},
          "E5":{'pos':[5,5],'type':'Az'},"E6":{'pos':[6,5],'type':'VD'},
          "E7":{'pos':[7,5],'type':'Az'},"E8":{'pos':[8,5],'type':'VD'},
          "E9":{'pos':[9,5],'type':'Az'},"E10":{'pos':[10,5],'type':'VD'},
          "E11":{'pos':[11,5],'type':'Az'},
          
          "F1":{'pos':[1,6],'type':'VD'},"F2":{'pos':[2,6],'type':'Az'},
          "F3":{'pos':[3,6],'type':'VD'},"F4":{'pos':[4,6],'type':'Az'},
          "F5":{'pos':[5,6],'type':'VD'},"F6":{'pos':[6,6],'type':'Az'},
          "F7":{'pos':[7,6],'type':'VD'},"F8":{'pos':[8,6],'type':'Az'},
          "F9":{'pos':[9,6],'type':'VD'},"F10":{'pos':[10,6],'type':'Az'},
          "F11":{'pos':[11,6],'type':'VD'},
          
          "G1":{'pos':[1,7],'type':'Az'},"G2":{'pos':[2,7],'type':'VD'},
          "G3":{'pos':[3,7],'type':'Az'},"G4":{'pos':[4,7],'type':'VD'},
          "G5":{'pos':[5,7],'type':'Az'},"G6":{'pos':[6,7],'type':'VD'},
          "G7":{'pos':[7,7],'type':'Az'},"G8":{'pos':[8,7],'type':'VD'},
          "G9":{'pos':[9,7],'type':'Az'},"G10":{'pos':[10,7],'type':'VD'},
          "G11":{'pos':[11,7],'type':'Az'},
          
          "H1":{'pos':[1,8],'type':'VD'},"H2":{'pos':[2,8],'type':'Az'},
          "H3":{'pos':[3,8],'type':'VD'},"H4":{'pos':[4,8],'type':'Az'},
          "H5":{'pos':[5,8],'type':'VD'},"H6":{'pos':[6,8],'type':'Az'},
          "H7":{'pos':[7,8],'type':'VD'},"H8":{'pos':[8,8],'type':'Az'},
          "H9":{'pos':[9,8],'type':'VD'},"H10":{'pos':[10,8],'type':'Az'},
          "H11":{'pos':[11,8],'type':'VD'},
          
          "I1":{'pos':[1,9],'type':'Az'},"I2":{'pos':[2,9],'type':'VD'},
          "I3":{'pos':[3,9],'type':'Az'},"I4":{'pos':[4,9],'type':'VD'},
          "I5":{'pos':[5,9],'type':'Az'},"I6":{'pos':[6,9],'type':'VD'},
          "I7":{'pos':[7,9],'type':'Az'},"I8":{'pos':[8,9],'type':'VD'},
          "I9":{'pos':[9,9],'type':'Az'},"I10":{'pos':[10,9],'type':'VD'},
          "I11":{'pos':[11,9],'type':'Az'},
          
          "J1":{'pos':[1,10],'type':'VD'},"J2":{'pos':[2,10],'type':'Az'},
          "J3":{'pos':[3,10],'type':'VD'},"J4":{'pos':[4,10],'type':'Az'},
          "J5":{'pos':[5,10],'type':'VD'},"J6":{'pos':[6,10],'type':'Az'},
          "J7":{'pos':[7,10],'type':'VD'},"J8":{'pos':[8,10],'type':'Az'},
          "J9":{'pos':[9,10],'type':'VD'},"J10":{'pos':[10,10],'type':'Az'},
          "J11":{'pos':[11,10],'type':'VD'},
          
          "K1":{'pos':[1,11],'type':'Az'},"K2":{'pos':[2,11],'type':'VD'},
          "K3":{'pos':[3,11],'type':'Az'},"K4":{'pos':[4,11],'type':'VD'},
          "K5":{'pos':[5,11],'type':'Az'},"K6":{'pos':[6,11],'type':'VD'},
          "K7":{'pos':[7,11],'type':'Az'},"K8":{'pos':[8,11],'type':'VD'},
          "K9":{'pos':[9,11],'type':'Az'},"K10":{'pos':[10,11],'type':'VD'},
          "K11":{'pos':[11,11],'type':'Az'}}

'''
print(sys.argv[1])

x = float(sys.argv[1])
y = float(sys.argv[2])
dist = np.sqrt(x*x+y*y)*27

print(dist)
'''
'''
dists = []
cent = locations[sys.argv[1]]['pos']
for i in range(1,len(sys.argv)):   #1 because 0 is script name
    c = locations[sys.argv[i]]['pos']
    d = np.sqrt((c[0]-cent[0])**2+(c[1]-cent[1])**2)*27
    dists += [d]
    
counts, bins = np.histogram(dists,bins = 100)
plt.stairs(counts, bins)
plt.title("Distance of Targets from Central Target: "+ str(sys.argv[1]))
plt.ylabel('Targets')
plt.xlabel('Distance (mm)')
plt.show()
'''

