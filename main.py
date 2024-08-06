import pandas as pd
import networkx as nx
import numpy as np
import random
import time
import sys
from infestion_results import InfectionResult
import os


def initialize_graph_from_csv(edge_list):
    G = nx.Graph()
    for _, row in edge_list.iterrows():
        G.add_edge(row['id1'], row['id2'], duration=row['duration'])
    return G


def initialize_graph_from_gexf(file_path):
    print(f'Reading the graph from {file_path}')
    return nx.read_gexf(file_path)


def calculate_infection_probabilities(G, a, max_dur):
    print(f'Initializing infection probabilities')
    edge_infection_probs = {}
    for u, v, data in G.edges(data=True):
        duration = data['duration']
        infection_probability = (duration / max_dur) * a
        infection_probability = min(infection_probability, a)
        edge_infection_probs[(u, v)] = infection_probability
        edge_infection_probs[(v, u)] = infection_probability
    return edge_infection_probs


def run_simulation(G, edge_infection_probs, initial_infected_count, time_steps, latency_period, infection_period,
                   results):
    '''
    :param G: NetworkX graph
    :param edge_infection_probs: edge list of infection probabilities (dict)
    :param initial_infected_count: number of initial infected nodes (int)
    :param time_steps: number of time steps (int)
    :param latency_period: latency period (int)
    :param infection_period: infection period (int)
    :param results: InfectionResult object for saving and processing the results
    :return: None (void)
    '''
    # Initialize counters dictionary for handling latency and infection period
    counters = {node: -latency_period for node in G.nodes}
    initvert = set()
    # Initialize set of infected nodes
    initial_infected = random.sample(list(G.nodes), initial_infected_count)
    for node in initial_infected:
        initvert.add(node)
        counters[node] = 0
    # Run the simulation in discrete time steps
    current_time = 0
    while initvert and current_time < time_steps:
        newset = set()
        for node in initvert:
            if counters[node] < 0:
                counters[node] += 1
                newset.add(node)
                continue

            neighbors = list(G.neighbors(node))
            for neighbor in neighbors:
                if counters[neighbor] < 0 and random.random() <= edge_infection_probs[(node, neighbor)]:
                    counters[neighbor] += 1
                    newset.add(neighbor)

            counters[node] += 1
            if counters[node] <= infection_period:
                newset.add(node)

        initvert = newset
        current_time += 1

    # Record the results
    sample = np.array([1 if counters[node] >= 0 else 0 for node in G.nodes])
    results.add_next(sample)
    current_time += 1


def load_configuration(config_path):
    print(f'Reading configurations {config_path}')
    config = {}
    with open(config_path) as f:
        for line in f:
            name, value = line.split('=')
            if name in ['input_type', 'output_path', 'input_path']:
                config[name.strip()] = value.strip()
            elif name == 'probability_upper_bound':
                config[name.strip()] = float(value.strip())
            else:
                config[name.strip()] = int(value.strip())
    return config


def main():
    # Load configuration
    config = load_configuration('input_first_try/config.txt')
    input_folder = config['input_path']
    # Load graph
    if config['input_type'] == 'edge_list':
        edge_list = pd.read_csv(os.path.join(input_folder, 'edge_list.csv'))
        edge_list.drop_duplicates(inplace=True)
        G = initialize_graph_from_csv(edge_list)
    else:
        G = initialize_graph_from_gexf(os.path.join(input_folder, 'graph.gexf'))

    # Calculate edge infection probabilities
    edge_infection_probs = calculate_infection_probabilities(G, config['probability_upper_bound'],
                                                             config['max_duration'])

    # Run simulations
    start_time = time.time()
    num_nodes = len(G.nodes)
    results = InfectionResult(num_nodes, config['iter'])

    for i in range(config['iter']):
        print(f"Running simulation {i + 1}/{config['iter']}...")

        run_simulation(G, edge_infection_probs, config['initial_size'], config['time_steps'],
                       config['latency_period'], config['infection_period'], results)

        # Print running time
        elapsed_time = time.time() - start_time
        if elapsed_time >= 3600:
            print(f"Progress: Simulation has been running for {int(elapsed_time // 3600)} hours.")
            sys.stdout.flush()
            start_time = time.time()

    # Process results as needed
    results.calculate_expected_values()
    results.calculate_infection_rate()
    # Save the results
    results.save_results(config['output_path'])
    print("Simulation completed.")


if __name__ == "__main__":
    main()
