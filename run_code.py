import os
import subprocess
import sys

# Max run time
TIME_OUT = 3600

# Program to be executed
code_file = os.path.abspath(sys.argv[1])

# Get all the entry file
entry_folder = sys.argv[2]
filenames = sorted(os.listdir(entry_folder), key=lambda x: int(x[7:-4]))

# Run code for each entry
for entry in filenames:
    
    # Create full file path
    full_path = os.path.join(entry_folder, entry)
    
    # Construct command
    comand_run = [code_file, full_path]
    
    print("----------------------------------------")
    print(f"Running for entry: '{entry}'")
    
    try:
        # Run the code 
        result = subprocess.run(
            comand_run, 
            timeout=TIME_OUT, 
            check=True,
            capture_output=True,
            text=True
        )
        
        # Print the result
        if result.stdout:
            print(f"Time: {result.stdout}")
        print("----------------------------------------\n")
    
    # Stop runing if there is a time out
    except subprocess.TimeoutExpired:
        print(f"!!! TIMEOUT for entry '{entry}'. Process was terminated.")
        print("----------------------------------------\n")
        break
    
    # Stop runing if there is a time out
    except subprocess.CalledProcessError as e:
        # This block executes if the C++ program runs but returns an error code.
        print(f"Error: The C++ program failed for entry '{entry}' with exit code {e.returncode}.")
        print("----------------------------------------\n")