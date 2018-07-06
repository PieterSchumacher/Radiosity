import numpy as np


def subdivide_loop(start_index, last_possible_index, max_interval_length, nb_processes):
    """ Calculate the most optimal way of subdividing a loop of interval length end - start
    into a given number of parallel processes.
    """
    if start_index > last_possible_index:
        print(" START IS LARGER THAN END ")
        return
    if nb_processes < 1:
        print(" NUMBER OF PROCESSES IS SMALLER THAN 1 ")
        return
    if start_index < 1 or last_possible_index < 1 or max_interval_length < 1:
        print(" INDICES OR MAX LENGTH ARE SMALLER THAN 1 ")
        return

    # Calculate the number of iterations a full set of processes can do
    current_number_of_iterations = 0
    while (last_possible_index - start_index) // (nb_processes * (current_number_of_iterations + 1)) > 0:
        if last_possible_index - start_index > max_interval_length:
            if ((current_number_of_iterations + 2) * nb_processes) > max_interval_length:
                last_possible_index = max_interval_length + start_index
                current_number_of_iterations += 1
                break
        current_number_of_iterations += 1

    # Create the current intervals
    intervals = []
    for i in range(nb_processes):
        intervals.append(np.array([start_index + current_number_of_iterations * i, start_index +
                                   current_number_of_iterations * (i+1)]))
    intervals = np.array(intervals)

    # Calculate how the set of processes handle the residue
    if current_number_of_iterations != 0:
        residue = (last_possible_index - start_index) % (current_number_of_iterations * nb_processes)
    else:
        residue = last_possible_index - start_index
    for k in range(residue):
        intervals[k][1] += 1
        for i in range(k+1, len(intervals)):
            for j in range(2):
                intervals[i][j] += 1
    return intervals
