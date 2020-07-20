import matplotlib.pyplot as plt

# Variables
x_axis_variables = [20, 50, 75, 100, 125, 150]
array_1_y = [8.6123046875, 49.1171875, 163.0078125, 281.125, 3889.15625, 19814.875]
array_2_y = [8.0380859375, 40.84375, 124.3046875, 261.859375, 2364.125, 10798.875]
array_3_y = [8.640625, 47.22265625, 147.125, 273.875, 2753.8125, 14255.4375]
array_4_y = [8.0458984375, 39.2734375, 117.734375, 214.234375, 2017.125, 10919.625]
array_5_y = [8.5888671875, 46.27734375, 157.8515625, 329.28125, 3868.625, 20706.625]
array_6_y = [8.5810546875, 47.50390625, 181.265625, 341.921875, 3803.4375, 24459.4375]

# Number of steps of unit propagation
plt.plot(x_axis_variables, array_1_y, color="red", label='JeroslowWangOneSided')
plt.plot(x_axis_variables, array_2_y, color="green", label='JeroslowWangTwoSided')
plt.plot(x_axis_variables, array_3_y, color="yellow", label='JeroslowWangOneSidedDynamic')
plt.plot(x_axis_variables, array_4_y, color="purple", label='JeroslowWangTwoSidedDynamic')
plt.plot(x_axis_variables, array_5_y, color="cyan", label='VSIDS')
plt.plot(x_axis_variables, array_6_y, color="black", label='eVSIDS')
plt.title('Number of decisions')
plt.xlabel('Number of variables')
plt.ylabel('Number of decisions')
plt.legend(loc="upper left")
plt.show()