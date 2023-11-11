import matplotlib.pyplot as plt

# Function to parse the bandwidth values from the file
def parse_bandwidth(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Extracting bandwidth values
    print(lines[6].split())
    bandwidth_values=[]
    for line in lines[8:]:
        if float(line.split()[6])<200:
            bandwidth_values.append(float(line.split()[6])*1000)
        else:
            bandwidth_values.append(float(line.split()[6]))
    #bandwidth_values = [float(line.split()[6]) for line in lines[8:] if float(line.split()[6])<200]

    return bandwidth_values

# File path
file_path = 'resulth1.txt'

# Parsing bandwidth values
bandwidth_values = parse_bandwidth(file_path)

# Creating time intervals for plotting (assuming intervals of 10 seconds)
time_intervals = [i * 5 for i in range(len(bandwidth_values))]

# Plotting
plt.plot(time_intervals, bandwidth_values, label='Throughput')
plt.title('Throughput over Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Throughput (Mbits/sec)')
plt.legend()
plt.grid(True)
plt.show()

