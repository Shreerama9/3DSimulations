# Import the required modules
from matplotlib import cm
import numpy as np
import os
from foamFile import FoamFile
from numpy import array
from numpy import pi, linspace, array
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define the parameters of the turbine
radius = 0.1  # in meters
speed = 60.0  # in kmph

# Define the geometry of the turbine
theta = linspace(0, 2*pi, 100)
x = radius * array([cos(t) for t in theta])
y = radius * array([sin(t) for t in theta])
z = array([0, 0.1, 0.1, 0])

# Plot the turbine geometry
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z)
plt.show()

# Define the boundary conditions for the inlet and outlet
U = speed * 1000 / 3600  # Convert kmph to m/s
inlet = {'U': ('fixedValue', [U, 0, 0])}
outlet = {'p': ('zeroGradient', [])}

# Define the rotating part of the turbine
rotating = {'type': 'rotatingWallVelocity',
            'origin': [0, 0, 0],
            'axis': [0, 0, 1],
            'omega': U/radius}

# Set up the simulation parameters
startTime = 0
endTime = 1
deltaT = 0.001
writeInterval = 100

# Write the case files

caseDict = {'application': 'icoFoam',
            'startFrom': 'startTime',
            'startTime': startTime,
            'endTime': endTime,
            'deltaT': deltaT,
            'writeControl': 'timeStep',
            'writeInterval': writeInterval}

FoamFile('system/controlDict',
         foamFileData=caseDict).write()

meshDict = {'vertices': array([x, y, z]).T,
            'cell_size': 0.01,
            'cell_type': 'hex'}

FoamFile('constant/polyMesh/blockMeshDict',
         foamFileData=meshDict).write()

bcDict = {'inlet': inlet,
          'outlet': outlet,
          'rotating': rotating}

FoamFile('0/U',
         foamFileData={'boundaryField': bcDict}).write()

# Run the simulation
os.system('icoFoam')

# Post-process the results

case = 'case'
time = '1'
data = np.genfromtxt('{}/{}'.format(case, time))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(data[:, 0], data[:, 1], data[:, 2], c='blue')
plt.show()
