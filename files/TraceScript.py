import matplotlib.pyplot as plt
import re
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Define the regex pattern for parsing trace lines
# Matches TIMESTAMP, snd_nxt (hex), and snd_cwnd (decimal) 
line_pattern = re.compile(r'(\d+\.\d+): tcp_probe: .* snd_nxt=(0x[0-9a-f]+) .* snd_cwnd=(\d+)')

def process_trace_file(file_path, output_name):
    timestamps = []
    cwnds = []
    seq_nums = []

    with open(file_path, 'r') as f:
        for line in f:
            match = line_pattern.search(line)
            if match:
                timestamps.append(float(match.group(1)))
                seq_nums.append(int(match.group(2), 16))
                cwnds.append(int(match.group(3)))

    if not timestamps:
        print(f"Skipping {file_path}: No valid data points found.")
        return

    # Normalize time to start at 0
    start_time = timestamps[0]
    normalized_times = [t - start_time for t in timestamps]

    # Create the visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    # Plot 1: Congestion Window 
    ax1.step(normalized_times, cwnds, where='post', color='blue', linewidth=1.5)
    ax1.set_ylabel('CWND (Packets)')
    ax1.set_title(f'Evolution of Congestion Window - {output_name}')
    ax1.grid(True, linestyle='--', alpha=0.7)

    # Plot 2: Sequence Numbers (Stevens Map) 
    ax2.plot(normalized_times, seq_nums, color='green', marker='o', markersize=1, linestyle='none')
    ax2.set_xlabel('Time (seconds)')
    ax2.set_ylabel('Sequence Number (snd_nxt)')
    ax2.set_title('TCP Sequence Number Evolution')
    ax2.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    
    # Save to current folder with requested naming convention
    save_path = f"{output_name}_Graph.png"
    plt.savefig(save_path)
    plt.close()
    print(f"Generated: {save_path}")

# Main execution loop
current_folder = os.getcwd()
for filename in os.listdir(current_folder):
    # Only process files named 'VBRScenario...' that end in .txt
    if filename.startswith("VBRScenario") and filename.endswith(".txt"):
        # Strip '.txt' to get the base name for the output
        base_name = os.path.splitext(filename)[0]
        process_trace_file(filename, base_name)