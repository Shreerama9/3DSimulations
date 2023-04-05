import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define the radius of the compressor in meters
radius = 10

# Define the speed of the compressor in km/h
speed = 60

# Define the angle of attack in degrees
angle_of_attack = 15

# Convert the angle of attack to radians
alpha = angle_of_attack * np.pi / 180

# Calculate the area of the compressor in square meters
area = np.pi * radius ** 2

# Calculate the mass flow rate of air in kg/s
density = 1.225  # kg/m^3
volumetric_flow_rate = speed / 3.6 * area  # m^3/s
mass_flow_rate = density * volumetric_flow_rate

# Calculate the inlet pressure assuming an exit pressure of 0 Pa
exit_pressure = 0
gamma = 1.4
inlet_pressure = exit_pressure + 0.5 * density * speed ** 2 * \
    (1 + (gamma - 1) / 2 * (speed / (gamma * 287 * 273.15))
     ** 2) ** (gamma / (gamma - 1))

# Define the number of points in the path
num_points = 100

# Create an array of angles
angles = np.linspace(0, 2 * np.pi, num_points)

# Calculate the x, y, and z coordinates of the path
x_coords = radius * np.cos(angles)
y_coords = radius * np.sin(angles)
z_coords = np.zeros(num_points)

# Calculate the x, y, and z components of the velocity vector
velocity_magnitude = speed / 3.6
velocity_x = velocity_magnitude * np.cos(alpha)
velocity_y = 0
velocity_z = velocity_magnitude * np.sin(alpha)

# Define the distance from the center of the compressor to the tip of the blade
blade_length = 5

# Calculate the x, y, and z coordinates of the blade tip
blade_x = (radius - blade_length) * np.cos(angles)
blade_y = (radius - blade_length) * np.sin(angles)
blade_z = np.zeros(num_points)

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the path and blade tip
ax.plot(x_coords, y_coords, z_coords, '-k', linewidth=2)
ax.plot(blade_x, blade_y, blade_z, '-r', linewidth=2)

# Set the limits of the plot
ax.set_xlim([-radius - blade_length, radius + blade_length])
ax.set_ylim([-radius - blade_length, radius + blade_length])
ax.set_zlim([-radius - blade_length, radius + blade_length])

# Add labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Path of Air Flow for Compressor')

# Set the aspect ratio of the plot
ax.set_box_aspect([1, 1, 1])

# Add a vector indicating the velocity
ax.quiver(0, 0, 0, velocity_x, velocity_y, velocity_z,
          color='blue', length=1, normalize=True)

# Display the plot
plt.show()
