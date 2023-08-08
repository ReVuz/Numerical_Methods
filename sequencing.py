import ast
import json

# Ask the user to enter the processing times for each job on machine 1 as a dictionary
T_input = input(
    "Enter the processing times for each job on machine 1 as a dictionary (e.g. {1: 15, 2: 10, ...}): ")
T1 = ast.literal_eval(T_input)

# Ask the user to enter the processing times for each job on machine 2 as a dictionary
K_input = input(
    "Enter the processing times for each job on machine 2 as a dictionary (e.g. {1: 10, 2: 20, ...}): ")
K1 = ast.literal_eval(K_input)

# Copy the original processing times to new variables
T = T1.copy()
K = K1.copy()

# Initialize the sequence list
S = []

# Loop until all jobs are sequenced
while T or K:
    # Find the job with the smallest time on machine 1
    j1 = min(T, key=T.get, default=None)
    # Find the job with the smallest time on machine 2
    j2 = min(K, key=K.get, default=None)

    # If there are no more jobs on one machine, assign the remaining jobs from the other machine
    if j1 is None:
        S.extend(K.keys())
        K.clear()
    elif j2 is None:
        S.extend(T.keys())
        T.clear()
    else:
        # Assign the job with the smallest time to the sequence
        if T[j1] <= K[j2]:
            S.append(j1)  # Append the job at the end of the sequence
            del T[j1]  # Remove the job from machine 1
        else:
            S.append(j2)  # Append the job at the end of the sequence
            del K[j2]  # Remove the job from machine 2

# Print the optimal sequence
print("The optimal sequence is:", S)

# Calculate the total elapsed time and idle time for each machine
T_total = T_idle = K_total = K_idle = 0

for j in S:
    # Add the processing time on machine 1 to the total time using T1
    T_total += T1.get(j, 0)
    # Add the maximum of previous total times and the processing time on machine 2 to the total time using K1
    K_total = max(T_total, K_total) + K1.get(j, 0)

    # Calculate the idle time on machine 1 and machine 2
    # Add the idle time on machine 1 if any
    T_idle += max(0, K_total - T_total)
    # Add the idle time on machine 2 if any
    K_idle += max(0, T_total - K_total)

# Print the total elapsed time and idle time for each machine
print("The total elapsed time on machine 1 is:", T_total)
print("The total elapsed time on machine 2 is:", K_total)
print("The idle time on machine 1 is:", T_idle)
print("The idle time on machine 2 is:", K_idle)
