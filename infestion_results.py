import numpy as np
import os


class InfectionResult:
    def __init__(self, vnum, snum):
        '''
        :param vnum: number of vertices (int)
        :param snum: number of simulations (int)
        '''
        self.vnum = vnum
        self.snum = snum
        self.samples = np.zeros((snum, vnum))
        self.expected_values = np.zeros(vnum)
        self.infection_rate = 0
        self.currentindex = 0

    def is_full(self):
        return self.currentindex == self.snum

    def add_next(self, sample):
        if self.is_full():
            print("Error: Samples are full")
            return False
        if len(sample) != self.vnum:
            print("Error: Sample size mismatch")
            return False
        self.samples[self.currentindex, :] = sample
        self.currentindex += 1
        return True

    def calculate_expected_values(self):
        self.expected_values = np.mean(self.samples, axis=0)

    def calculate_infection_rate(self):
        self.infection_rate = (np.sum(self.expected_values)) / self.vnum

    def save_results(self, output_path):
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        np.save(os.path.join(output_path, 'node_probabilities.npy'), self.expected_values)
        with open(os.path.join(output_path, 'infection_rate.txt'), 'w') as file:
            file.write(f'Global infection rate {self.infection_rate}')
