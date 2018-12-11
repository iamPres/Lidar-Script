
#RPLidar Implimentation
#Preston Willis

from networktables import NetworkTables as net
from rplidar import RPLidar
import numpy as np
import math
import time

ip = '10.15.12.2'
net.initialize(server=ip)
data = net.getTable("datatable")
lidar = RPLidar('/dev/ttyUSB0') #Initialize lidar to ttyUSB0
info = lidar.get_info()
print(info)
time.sleep(5) #wait until lidar starts spinning to record measurments

def StopMotor():
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()

def record():
        input1 = 0
        input2 = 0
        for i, scan in enumerate(lidar.iter_scans()): #Scans environment and enumerates results by rotation
            for i in range(0,len(scan)): #Loop through the returned values of one rotation (0-360)
                #print (angle)
                if scan[i][1] > 350 and scan[i][1] < 360: #Find desired input vector
                    #print("ANGLE FOUND")
                    input1 = scan[i][2]
                    #print("     1 = "+str(scan[i][2])) 
                    
                if scan[i][1] > 175 and scan[i][1] < 185: #Find desired input vector
                    #print("ANGLE FOUND")
                    input2 = scan[i][2]
                    #print("2 = "+str(scan[i][2]))
                
            print("OUTPUT = "+str(neuralNet(input1,input2)))
            data.putNumber("turn", neuralNet(input1,input2))        
                 
                #if i >= 0: #One rotation max
                    #break
def neuralNet(in1, in2):
    weights = [-0.01,0.01]
    output = math.tanh((in1 * weights[0]) + (in2 * weights[1]))
    
    return output

try:
	record()

except Exception as e:
	print(e)
	if str(e) == "Wrong body size":
	    record()
	else:
            StopMotor()
except KeyboardInterrupt:
        StopMotor()



