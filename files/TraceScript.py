import matplotlib.pyplot as plt
import re
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

line_pattern = re.compile(r'(\d+\.\d+): tcp_probe: .* snd_nxt=(0x[0-9a-f]+) .* snd_cwnd=(\d+)')

def process_trace_file(file_path, output_name):
    timestamps = []
    cwnds = []
    seq_nums = []

    try:
        with open(file_path, 'r') as f:
            for line in f:
                match = line_pattern.search(line)
                if match:
                    timestamps.append(float(match.group(1)))
                    seq_nums.append(int(match.group(2), 16))
                    cwnds.append(int(match.group(3)))
    except Exception as e:
        print(f"Could not read {file_path}: {e}")
        return

    if not timestamps:
        print(f"Skipping {file_path}: No valid TCP probe data points found.")
        return

    start_time = timestamps[0]
    normalized_times = [t - start_time for t in timestamps]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    ax1.step(normalized_times, cwnds, where='post', color='blue', linewidth=1.5)
    ax1.set_ylabel('CWND (Packets)')
    ax1.set_title(f'Evolution of Congestion Window - {output_name}')
    ax1.grid(True, linestyle='--', alpha=0.7)

    ax2.plot(normalized_times, seq_nums, color='green', marker='o', markersize=1, linestyle='none')
    ax2.set_xlabel('Time (seconds)')
    ax2.set_ylabel('Sequence Number (snd_nxt)')
    ax2.set_title('TCP Sequence Number Evolution')
    ax2.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    
    save_path = f"{output_name}_Graph.png"
    plt.savefig(save_path)
    plt.close()
    print(f"Generated: {save_path}")

current_folder = os.getcwd()
script_name = os.path.basename(__file__)

for filename in os.listdir(current_folder):
    full_path = os.path.join(current_folder, filename)
    
    if os.path.isfile(full_path) and filename != script_name and not filename.endswith("_Graph.png"):
        base_name = os.path.splitext(filename)[0]
        process_trace_file(filename, base_name)