## SEIR infection model to be run on contact network
### Inputs
#### 'config.txt' file
Parameters:
- input_type: Could be either 'edge_list or 'graph'
- iter: Number of iterations
- probability_upper_bound: Upper bound for edge infection probability
- initial_size: Number of initially infected nodes
- time_steps: Number of discrete time steps (days)
- latency_period: Latency period (1 for SI and SIR model)
- infection_period: Infection period (== time_steps for SI model)
- output_path: Path to output folder
- input_path: Path to input folder
- max_duration: Duration to be mapped to maximal probability

#### 'graph.gexf' or 'edge_list.csv' file:
Attributes:
- 'id1': id of the first node
- 'id2': id of the second node
- 'starttime': YYYY-MM-DD hh:mm:ss time stamp
- 'duration': duration in seconds (int)
- 'trip_id': id of the trip

### Outputs
### 'node_probabilities.npy' 
Array with probabilities of infection for nodes of the graph.
To read the array use the code below
```python
import numpy as np
array = np.load('output_path/node_probabilities.npy')
```
### 'infection_rate.txt'
Estimated infection rate