import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# Safely loads run times from a file
def load_run_times(filepath):
    try:
        with open(filepath, 'r') as f:
            return [float(line.strip()) for line in f.readlines()]
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found. Exiting.")
        exit()
    except ValueError:
        print(f"Error: The file '{filepath}' contains non-numeric data. Exiting.")
        exit()

# Gets sorted character counts from filenames in a directory
def get_char_counts(directory):
    try:
        filenames = os.listdir(directory)
        txt_files = [f for f in filenames if f.endswith('.txt')]
        char_counts = [int(filename[7:-4]) for filename in txt_files]
        char_counts.sort()
        return char_counts
    except (FileNotFoundError, IndexError, ValueError):
        print(f"Error reading or parsing files in '{directory}'. Check directory and filenames. Exiting.")
        exit()

def create_plot(x_data, datasets, title, ylabel, output_filename):
    plt.figure(figsize=(10, 6))

    for ds in datasets:
        plt.plot(x_data, ds['data'], ds['style'], label=ds['label'], linewidth=2, markersize=8)

    if len(datasets) > 1:
        plt.legend()

    plt.xlabel('Number of Elements', fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title(title, fontsize=14)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Plot saved as '{output_filename}'")


# Main Execution Block
if __name__ == "__main__":
    
    # Define paths
    file_path_dp = 'dp_result.txt'
    file_path_rec = 'rec_result.txt'
    entradas_dir = "./entradas"

    # Load all data once
    run_times_dp = load_run_times(file_path_dp)
    run_times_rec = load_run_times(file_path_rec)
    char_num = get_char_counts(entradas_dir)
    
    # Synchronize data lengths to prevent errors
    min_len = min(len(char_num), len(run_times_dp), len(run_times_rec))
    if len(char_num) > min_len or len(run_times_dp) > min_len or len(run_times_rec) > min_len:
        print(f"Warning: Data lengths are inconsistent. Truncating all plots to {min_len} points.")

    char_num = char_num[:min_len]
    run_times_dp = run_times_dp[:min_len]
    run_times_rec = run_times_rec[:min_len]
    
    # Define the datasets for plotting
    dp_dataset = {'data': run_times_dp, 'label': 'Dynamic Programming', 'style': 'bo-'}
    rec_dataset = {'data': run_times_rec, 'label': 'Recursion', 'style': 'rs-'}

    # Generate all three graphs using the single, flexible function
    
    # Create DP-only graph
    create_plot(
        x_data=char_num, 
        datasets=[dp_dataset], 
        title='LCS With Dynamic Programming', 
        ylabel='Execution Time (milliseconds)',
        output_filename='execution_time_dp.png'
    )

    # Create Recursion-only graph
    create_plot(
        x_data=char_num, 
        datasets=[rec_dataset], 
        title='LCS With Recursion', 
        ylabel='Execution Time (milliseconds)',
        output_filename='execution_time_rec.png'
    )

    # Create comparison graph
    create_plot(
        x_data=char_num, 
        datasets=[dp_dataset, rec_dataset], 
        title='LCS: Dynamic Programming vs. Recursion', 
        ylabel='Execution Time (milliseconds)',
        output_filename='comparison.png'
    )