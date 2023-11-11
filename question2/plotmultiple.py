import matplotlib.pyplot as plt

# Function to parse the bandwidth values from the file
def parse_bandwidth(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Extracting bandwidth values
    bandwidth_values = [float(line.split()[6]) for line in lines[7:]]

    return bandwidth_values

# Function to plot bandwidth values from multiple files
def plot_multiple_files(file_paths, labels):
    plt.figure(figsize=(10, 6))

    for file_path, label in zip(file_paths, labels):
        # Parsing bandwidth values
        bandwidth_values = parse_bandwidth(file_path)

        # Creating time intervals for plotting (assuming intervals of 10 seconds)
        time_intervals = [i * 10 for i in range(len(bandwidth_values))]

        # Plotting
        plt.plot(time_intervals, bandwidth_values, label=label)

    plt.title('Throughput over Time')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Throughput (Gbits/sec)')
    plt.legend()
    plt.grid(True)
    plt.show()

# File paths and corresponding labels
file_paths = ['resulth1.txt', 'resulth2.txt', 'resulth3.txt']
labels = ['host 1', 'host 2', 'host 3']

# Plotting multiple files
plot_multiple_files(file_paths, labels)

